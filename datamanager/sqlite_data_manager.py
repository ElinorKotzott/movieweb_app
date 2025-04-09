from movieweb_app.datamanager.data_manager import DataManager


class SQLiteDataManager(DataManager):

    def __init__(self, models):
        self.models = models

    def get_all_movies(self):
        movies = self.models.Movie.query.all()
        return movies


    def get_all_users(self):
        users = self.models.User.query.all()
        return users


    def get_user_movies(self, user_id):
        """getting all movies of one user based on user id: first, filtering users_movies, searching for all
        rows that have the user_id. then, extracting movie ids from these results. then, checking for these
        movie ids in the movies table and returning the whole movie objects"""
        user_movie_instances = self.models.UserMovie.query.filter_by(user_id=user_id).all()
        movie_ids = [instance.movie_id for instance in user_movie_instances]
        all_movies = self.models.Movie.query.all()
        user_movies = [movie for movie in all_movies if movie.id in movie_ids]
        return user_movies


    def add_user(self, user):
        """this method takes a user object as an argument and adds it to the database"""
        self.models.db.session.add(user)
        self.models.db.session.commit()


    def add_movie(self, movie):
        """the movie object sent in will be added to the database"""
        self.models.db.session.add(movie)
        self.models.db.session.commit()


    def update_movie(self, movie, new_rating):
        """allows user to update a movie rating. user input for new rating
        and movie instance to update will be sent in"""
        movie.rating = new_rating
        self.models.db.session.commit()


    def delete_movie(self, movie_id):
        """this method is for the manager of the database: it deletes a movie entirely from the database.
        if movie with the provided movie_id exists: deletes the movie"""
        to_delete = self.models.Movie.query.get(movie_id)
        if to_delete:
            self.models.db.session.delete(to_delete)
            self.models.db.session.commit()

        #TODO what happens if the deleted movie was part of a user's favorites list?
        # will those rows be deleted automatically? can we tell the users that movies
        # have been deleted from their lists because they weren't available any more?


    def delete_user_movie(self, user_id, movie_id):
        to_delete = self.models.UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if to_delete:
            self.models.db.session.delete(to_delete)
            self.models.db.session.commit()
