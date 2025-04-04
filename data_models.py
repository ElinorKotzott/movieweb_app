from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Date, Integer, Float

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birthday = Column(Date)


    def __str__(self):
        """represents instance of user as a string"""
        return f"Name: {self.name}, id: {self.id}, birthday: {self.birthday}"


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    director = Column(String)
    year = Column(Integer)
    rating = Column (Float)


    def __str__(self):
        """represents instance of movie as a string"""
        return f"Movie title: {self.name}, id: {self.id}, director: {self.director}, published in: {self.year}, rating: {self.rating}"

    with app.app_context():
        db.create_all()
