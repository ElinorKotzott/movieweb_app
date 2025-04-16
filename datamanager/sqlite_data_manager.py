
from sqlalchemy.exc import SQLAlchemyError
from datamanager.data_manager import DataManager



class SQLiteDataManager(DataManager):

    def __init__(self, models):
        """instantiating every sqlite data manager with the
        data models that it is supposed to be using"""
        self.models = models


    def get_all_movies(self):
        """finding all movies in the database by querying the movies table
        in the database, then returning all movie instances"""
        movies = self.models.Movie.query.all()
        return movies


    def get_all_users(self):
        """getting all users by querying the users table in the database,
        then returning the whole user instances"""
        users = self.models.User.query.all()
        return users


    def get_user_movies(self, user_id):
        """getting all movies in a user's favorites list: first, getting
         user_movies with a certain user_id and then returning the whole movie objects"""
        user_movies = self.models.User.query.get(user_id).movies
        for user_movie in user_movies:
            print(user_movie.movie_id)
        actual_movies = [um.movie for um in user_movies]

        return actual_movies


    def add_user(self, user):
        """this method takes a user object as an argument and tries to add it to
        the database. returns a string on whether it was successful"""
        try:
            self.models.db.session.add(user)
            self.models.db.session.commit()
            return 'User added successfully!'
        except SQLAlchemyError:
            self.models.db.session.rollback()
            return 'An error occurred, user could not be added!'


    def add_movie(self, movie):
        """takes in a movie instance that will be added to the database. returns
        a string on whether it was successful"""
        try:
            self.models.db.session.add(movie)
            self.models.db.session.commit()
            return 'Movie added successfully!'
        except SQLAlchemyError:
            self.models.db.session.rollback()
            return 'An error occurred, movie could not be added!'


    def add_user_movie(self, user_id, movie_id):
        """creates a new instance of user_movie using user_id and movie_id and
        saves it to the database. returns a string on whether that was successful"""
        new_user_movie = self.models.UserMovie(user_id=user_id, movie_id=movie_id)
        try:
            self.models.db.session.add(new_user_movie)
            self.models.db.session.commit()
            return 'Movie added successfully!'
        except SQLAlchemyError:
            self.models.db.session.rollback()
            return 'An error occurred, movie could not be added!'


    def update_movie(self, movie_id, year, director, rating):
        """updates the movie with the id movie_id using the year, director and rating
        that are sent in via arguments. returns a string depending on whether it was successful"""
        movie_to_update = self.models.Movie.query.filter_by(id=movie_id).first()
        movie_to_update.year = year
        movie_to_update.director = director
        movie_to_update.rating = rating
        try:
            self.models.db.session.commit()
            return 'Movie rating updated successfully!'
        except SQLAlchemyError:
            return 'An error occurred, rating could not be updated!'


    def delete_movie(self, movie_id):
        """this method is for the manager of the database: it deletes a movie entirely from the database.
        if movie with the provided movie_id exists: deletes the movie. returns a string depending on
        whether it was successful or not"""
        to_delete = self.models.Movie.query.get(movie_id)
        if to_delete:
            return self.delete_movie_from_database_or_favorites_list(to_delete)
        else:
            return 'This movie doesn''t exist!'


    def delete_user_movie(self, user_id, movie_id):
        """deletes a movie from a user's favorites list. takes in user_id of the relevant user
        and movie_id of the movie that is to be deleted. returns a string depending on whether
        it was successful or not"""
        to_delete = self.models.UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if to_delete:
            return self.delete_movie_from_database_or_favorites_list(to_delete)
        else:
            return 'This movie doesn''t exist!'


    def delete_movie_from_database_or_favorites_list(self, movie):
        """helper method to delete movie either from our whole database or only from a user's favorites
        to avoid duplicate code. returns a string depending on whether it was successful or not"""
        try:
            self.models.db.session.delete(movie)
            self.models.db.session.commit()
            return 'Movie deleted successfully!'
        except SQLAlchemyError:
            self.models.db.session.rollback()
            return 'An error occurred, movie could not be deleted!'
