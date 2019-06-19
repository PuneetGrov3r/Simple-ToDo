from app import db, bcrypt
from sqlalchemy.dialects.postgresql import JSON
from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    admin = db.Column(db.Integer, nullable=False)
    security_question = db.Column(db.Integer, nullable=False)
    security_answer = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, question, answer):
        self.username = username
        self.password = password
        self.admin = 0
        self.security_question = question
        self.security_answer = answer

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @staticmethod
    def generate_hash(password):
        # return sha256.hash(password)
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    @staticmethod
    def verify_hash(password, hash):
        # return sha256.verify(password, hash)
        return bcrypt.check_password_hash(hash, password)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def check_security_qa(cls, username, question, answer):
        p = cls.query.filter_by(username=username).first()
        if p.security_question==question and p.security_answer==answer: return True
        else: return False

    @classmethod
    def update_password(cls, username, new_password):
        cls.query.filter_by(username=username).update({"password": new_password})
        db.session.commit()

    
    #@classmethod
    #def return_all(cls):
    #    def to_json(x):
    #        return {
    #            'username': x.username,
    #            'password': x.password
    #        }
    #    return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    #@classmethod
    #def delete_all(cls):
    #    try:
    #        num_rows_deleted = db.session.query(cls).delete()
    #        db.session.commit()
    #        return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
    #    except:
    #        return {'message': 'Something went wrong'}



class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


class DataModel(db.Model):
    __tablename__ = 'user_data'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(120), nullable = False)
    todo_list = db.Column(db.String(50000), nullable=False)

    def __init__(self, user_id, username, todo):
        self.user_id = user_id
        self.username = username
        self.todo_list = todo
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update_todo(cls, name, new_todo):
        ___id__ = UserModel.find_by_username(name).id
        cls.query.filter_by(user_id=___id__).update({"todo_list": new_todo})
        db.session.commit()

    @classmethod
    def get_todo(cls, name):
        ___id__ = UserModel.find_by_username(name).id
        todo_list = cls.query.filter_by(user_id=___id__).first().todo_list
        return todo_list
