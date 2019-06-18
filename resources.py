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

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 400
        
        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
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
        except Exception as e:
            res = {'message': str(e)}
            return res, 500


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
        except Exception as e:
            return {'message': str(e)}, 500


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
        except Exception as e:
            return {"Error": str(e)}, 500
    
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
        except Exception as e:
            return {"Error": str(e)}, 500

parser3 = reqparse.RequestParser()
parser3.add_argument('extra_content', help = 'This field cannot be blank', required = True)
parser3.add_argument('to', help = 'This field cannot be blank', required = True)
class MailRes(Resource):
    @staticmethod
    def __get_pri__(s):
        if s == "hig": return "High"
        elif s == "mod": return "Moderate"
        elif s == "low": return "Low"
    
    @jwt_required
    def post(self):
        extra = get_raw_jwt()['extra_content']
        from_ = os.environ["MY_MAIL"]
        to = get_raw_jwt()['to']
        if(to == "user_self"):
            to = get_raw_jwt()['identity']
        data = DataModel.get_todo(get_raw_jwt()['identity'])
        lst = data.split(".:::.")
        for i in len(lst):
            pri = self.__get_pri__(lst[i][10:13])
            if lst[i][14:23] == "completed":
                 lst[i] = f"Priority {pri} (Completed): {lst[25:-4]}"
            else:
                lst[i] = f"Priority {pri}: {lst[15:-4]}"
        data = lst.join("\n    ")
        data = "ToDo List:\n" + data + "\n\n"
        h = f"Mail (SMTP)\nFROM: {from_}\nTO: {to}\nSubject: Your ToDo List\n\n\n"
        data = h + data + extra
        try:
            with smtplib.SMTP('localhost') as smtpObj:
                smtpObj.sendmail(from_, to, data)
            return {"res": "Mail Sent."}, 200
        except SMTPException as e:
            return {"Error": str(e)}, 500


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
#         except Exception as e:
#             res = json.dumps({'message': str(e)})
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