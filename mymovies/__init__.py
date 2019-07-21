from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xRZgiO5v5OgSszuo7dME6A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://idboceavpzxbop:2f4d8dc270a11a0fb423c103679f78d5634709f9a8111cbe7f5d29126dac63e4@ec2-54-83-1-101.compute-1.amazonaws.com:5432/dd9kj62lqu6bu7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mymovies import routes