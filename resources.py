from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, 
                                    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,
                                    set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from models import UserModel, RevokedTokenModel
from flask_restful import Resource
from flask_restful import Resource, reqparse
from models import UserModel, DataModel
from flask import Response, json, jsonify
import smtplib
from smtplib import SMTPException
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

parser5 = reqparse.RequestParser()
parser5.add_argument('username', help = 'This field cannot be blank', required = True)
parser5.add_argument('password', help = 'This field cannot be blank', required = True)
parser5.add_argument('security-question', help = 'This field cannot be blank', required = True)
parser5.add_argument('security-answer', help = 'This field cannot be blank', required = True)
class UserRegistration(Resource):
    def post(self):
        data = parser5.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 400

        q = data['security-question']
        ques = [
            "What is your hometown's name?",
            "What is/was your first pet's name?",
            "Who is your favorite author?",
            "Who is your favorite character in your favorite show?"
        ]

        sec_q = -1
        for i, el in enumerate(ques):
            if el == q:
                sec_q = i
                break
        
        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            question = sec_q,
            answer = data['security-answer']
        )
        
        try:
            new_user.save_to_db()
            ___id__ = new_user.find_by_username(data['username']).id
            new_user_data = DataModel(
                user_id=___id__,
                username=data['username'],
                todo="")
            new_user_data.save_to_db()
            access_token = create_access_token(identity = data['username'])
            #refresh_token = create_refresh_token(identity = data['username'])
            resp = jsonify({'user': data['username']})
            set_access_cookies(resp, access_token)
            #set_refresh_cookies(resp, refresh_token)
            resp.status_code = 200
            return resp
        except:
            res = {'message': "Something went wrong"}
            return res, 500

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 400
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            #refresh_token = create_refresh_token(identity = data['username'])
            resp = jsonify({
                            'message': 'User {} was created'.format(data['username']),
                            'user': data['username']
                    })
            set_access_cookies(resp, access_token)
            #set_refresh_cookies(resp, refresh_token)
            resp.status_code = 200
            return resp
        else:
            return {'message': "Credentials not correct."}, 500
      

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            resp = jsonify({'message': 'Access token has been revoked'})
            unset_jwt_cookies(resp)
            resp.status_code = 200
            return resp
        except:
            return {'message': "Something went wrong"}, 500


parser2 = reqparse.RequestParser()
parser2.add_argument('new_todo', help = 'This field cannot be blank', required = True)
class UserDataRes(Resource):
    @jwt_required
    def post(self):
        try:
            todo = parser2.parse_args()["new_todo"]
            user = get_raw_jwt()['identity']
            DataModel.update_todo(user, todo)
            return {"message": "Success"}, 200
        except:
            return {"Error": "Something went wrong"}, 500
    
    @jwt_required
    def get(self):
        try:
            user = get_raw_jwt()['identity']
            todo_list = DataModel.get_todo(user)
            resp = {
                "todo_list": todo_list,
                "message": "Success"
            }
            return resp, 200
        except:
            return {"Error": "Something went wrong"}, 500

parser3 = reqparse.RequestParser()
parser3.add_argument('extra_content')
parser3.add_argument('to', help = 'This field cannot be blank', required = True)
class MailRes(Resource):
    @staticmethod
    def __get_pri__(s):
        if s == "hig": return "High"
        elif s == "mod": return "Moderate"
        elif s == "low": return "Low"
    
    @jwt_required
    def post(self):
        extra = parser3.parse_args()['extra_content']
        from_ = os.environ["MY_MAIL"]
        to = parser3.parse_args()['to']
        if(to == "user_self"):
            to = get_raw_jwt()['identity']
        data = DataModel.get_todo(get_raw_jwt()['identity'])
        lst = data.split(".:::.")
        for i in range(len(lst)):
            pri = self.__get_pri__(lst[i][10:13])
            if lst[i][14:23] == "completed":
                 lst[i] = f"Priority {pri} (Completed): {lst[25:-4]}"
            else:
                lst[i] = f"Priority {pri}: {lst[15:-4]}"
        data = "\n    ".join(lst)
        data = "ToDo List:\n" + data + "\n\n"
        h = f"Mail (SMTP)\nFROM: {from_}\nTO: {to}\nSubject: Your ToDo List\n\n\n"
        data = h + data + extra
        message = Mail(
                from_email=from_,
                to_emails=to,
                subject='Your ToDo list',
                html_content=data)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            return response.status_code
        except:
            return {"Error": "Somthing went wrong."}, 500

parser4 = reqparse.RequestParser()
parser4.add_argument('email', help = 'This field cannot be blank', required = True)
parser4.add_argument('security-question', help = 'This field cannot be blank', required = True)
parser4.add_argument('security-answer', help = 'This field cannot be blank', required = True)
parser4.add_argument('new-password', help = 'This field cannot be blank', required = True)
class ForgotPass(Resource):
    def post(self):
        name = parser4.parse_args()['email']
        q = parser4.parse_args()['security-question']
        sec_a = parser4.parse_args()['security-answer']
        password = parser4.parse_args()['new-password']

        ques = [
            "What is your hometown's name?",
            "What is/was your first pet's name?",
            "Who is your favorite author?",
            "Who is your favorite character in your favorite show?"
        ]

        sec_q = -1
        for i, el in enumerate(ques):
            if el == q:
                sec_q = i
                break


        try:
            if UserModel.check_security_qa(name, sec_q, sec_a):
                UserModel.update_password(name, UserModel.generate_hash(password))
            else:
                return {"res": "Failed Check"}, 404
        except:
            return {"res": "Something went wrong"}, 500


"""
# class UserLogoutRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedTokenModel(jti = jti)
#             revoked_token.add()
#             resp = jsonify({'message': 'Access token has been revoked'})
#             unset_jwt_cookies(resp)
#             resp.status_code = 200
#             return resp
#         except:
#             res = json.dumps({'message': "Something went wrong"})
#             return Response(res, status=500, mimetype='application/json')
      
      
# class TokenRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         current_user = get_jwt_identity()
#         access_token = create_access_token(identity = current_user)
#         resp = jsonify({'refresh': True})
#         set_access_cookies(resp, access_token)
#         resp.status_code = 200
#         return resp

      
      
# class AllUsers(Resource):
#     def get(self):
#         return UserModel.return_all()
    
#     def delete(self):
#         return UserModel.delete_all()
      

"""