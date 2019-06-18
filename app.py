from flask import Flask, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__, static_folder="assets")
api = Api(app)

#
# Setting up Database 
#
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

#
# Adding JWT authorization
#
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']#, 'refresh']
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
#app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
#app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_COOKIE_SECURE'] = False
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

#
# Using BCrypt hashing
#
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
bcrypt.init_app(app)

#
# Adding API endpoints for GET, POST etc requests
#
import resources
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserDataRes, '/list')
api.add_resource(resources.MailRes, '/mail')
#api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
#api.add_resource(resources.TokenRefresh, '/token/refresh')
#api.add_resource(resources.AllUsers, '/users')
#api.add_resource(resources.SecretResource, '/secret')

import views, models

if __name__ == '__main__':
    port = os.environ['PORT']
    app.run(host="0.0.0.0", port=port)