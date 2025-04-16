from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float, Date

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birthday = Column(Date)
    movies = db.relationship('UserMovie', backref='user', lazy=True)


    def __str__(self):
        """represents instance of user as a string"""
        return f"Name: {self.name}, id: {self.id}, birthday: {self.birthday}"


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    user_movies = db.relationship('UserMovie', backref='movie', lazy=True)


    def __str__(self):
        """represents instance of movie as a string"""
        return f"Movie title: {self.name}, id: {self.id}, director: {self.director}, published in: {self.year}, rating: {self.rating}"


class UserMovie(db.Model):
    __tablename__ = "users_movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
