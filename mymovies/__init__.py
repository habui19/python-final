from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xRZgiO5v5OgSszuo7dME6A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lkawrazylcwjbn:06ee2fea72e90f0ee40a7687f2ff61c54e2b4c030a60798565311397d38bccad@ec2-107-20-173-2.compute-1.amazonaws.com:5432/dbgc6u09n5vnrk'
heroku = Heroku(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mymovies import routes