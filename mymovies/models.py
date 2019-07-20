from datetime import datetime
from mymovies import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f"User ('{self.username}')"

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    imdb_rating = db.Column(db.String(100), nullable=False)
    self_rating = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Movie ('{self.title}', '{self.genre}', '{self.imdb_rating}', '{self.self_rating}', '{self.duration}', '{self.release_date}')"