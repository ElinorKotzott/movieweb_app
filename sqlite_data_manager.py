from flask_sqlalchemy import SQLAlchemy
from data_manager import DataManager
from data_models import User, Movie, UserMovie, db


class SQLiteDataManager(DataManager):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)


    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        """getting all movies of one user based on user id. first, we're filtering users_movies, searching for all
        movie ids that have our user id. then, returning all movies (instances of movie) associated with that user"""
        user_movies = UserMovie.query.filter_by(user_id=user_id).all()
        return [Movie.query.get(entry.movie_id) for entry in user_movies]


    def add_user(self, user):
        """this method takes a user object as an argument and adds it to the database"""
        db.session.add(user)
        db.session.commit()


    def add_movie(self, movie):
        """the movie object sent in will be added to the database"""
        db.session.add(movie)
        db.session.commit()
