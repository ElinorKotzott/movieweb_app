from movieweb_app.datamanager.data_manager import DataManager


class SQLiteDataManager(DataManager):

    def __init__(self, models):
        self.models = models

    def get_all_movies(self):
        movies = self.models.Movie.query.all()
        return movies


    def get_all_users(self):
        users = self.models.User.query.all()
        names = [user.name for user in users]
        return names


    def get_user_movies(self, user_id):
        """getting all movies of one user based on user id. first, we're filtering users_movies, searching for all
        movie ids that have our user id. then, returning all movies (instances of movie) associated with that user"""
        user_movies = self.models.UserMovie.query.filter_by(user_id=user_id).all()
        return [user_movie.title for user_movie in user_movies]


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
        """if movie with the provided movie_id exists: deletes the movie"""
        to_delete = self.models.Movie.query.get(movie_id)
        if to_delete:
            self.models.db.session.delete(to_delete)
            self.models.db.session.commit()
