# Simple-ToDo

About:

1. ToDo App;  A simple and flexible ToDo app
1. Flask-RESTful; Using RESTful API for communications
1. Flask-jwt-extended; Using secured jwt cookies with token blacklisting for user authentication
1. bcrypt; Using BCrypt for password encryption
1. Heroku Ready!

How to run:

1. `pip install requirements.txt`,
1. `python manage.py db init`,
1. `python manage.py db migrate`,
1. `python manage.py db upgrade`,
1. `flask run`

For Heroku app and your local app too:

Set environment varibales for your instant: `APP_SETTINGS`, `DATABASE_URL`, `FLASK_ENV`, `JWT_SECRET_KEY`, `MAIL_ID`, `PORT` and `SECRET_KEY`

For Development environment:

1. `APP_SETTINGS` : `config.DevelopmentConfig`,
1. `FLASK_ENV` : `development`
