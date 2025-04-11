from datetime import datetime
import os

from datamanager import data_models
from datamanager.sqlite_data_manager import SQLiteDataManager
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies_users.sqlite')
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
data_models.db.init_app(app)
app.secret_key = 'incredibly_secret_key_wow'

data_manager = SQLiteDataManager(data_models)


@app.route('/')
def home():
    """getting all movies via data_manager and listing them on our home page"""
    movies = data_manager.get_all_movies()
    return render_template('index.html', movies=movies)


@app.route('/users')
def list_users():
    """getting all users via data_manager and listing them on a page"""
    users = data_manager.get_all_users()
    return render_template('list_users.html', users=users)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    """showing all favorites of a specific user using the user_id"""
    user = data_models.User.query.get(user_id)
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_movies=user_movies, user=user)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    """renders add movie template (get). allows adding of a movie to the database
    using a form (post) and shows message upon redirect"""
    current_year = datetime.now().year
    if request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = int(request.form.get('year'))
        rating = float(request.form.get('rating'))
        new_movie = data_models.Movie(name=name, director=director, year=year, rating=rating)
        flash(data_manager.add_movie(new_movie))
        return redirect('/')
    return render_template('add_movie.html', current_year=current_year)


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie_to_favorites(user_id):
    """allows an app user to add a movie that already exists in the database
    to their personal favorites list"""
    # getting all movies in the user's favorites list
    user_movies = data_models.UserMovie.query.filter_by(user_id=user_id).all()
    # getting all movie ids of those movies
    user_movie_ids = [user_movie.movie_id for user_movie in user_movies]
    # getting all ids of movies NOT in user's favorites list by comparing to all movies in the database
    ids_not_in_favorites_list = [movie.id for movie in data_models.Movie.query.all() if movie.id not in user_movie_ids]
    # getting all movies not in user's favorites list by querying using the ids
    movies_not_in_favorites_list = data_models.Movie.query.filter(
        data_models.Movie.id.in_(ids_not_in_favorites_list)).all()

    user = data_models.User.query.get(user_id)

    if request.method == 'POST':
        movie_id = request.form['movie_id']
        flash(data_manager.add_user_movie(user_id, movie_id))
        return redirect(f'/users/{user_id}')

    return render_template('add_movie_to_favorites.html', user=user, movies=movies_not_in_favorites_list)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """allows adding a user to the database. renders add_user upon get request,
    shows a success message upon redirect to home"""
    if request.method == 'POST':
        name = request.form.get('name')
        birthday_str = request.form.get('birthday')
        birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
        new_user = data_models.User(name=name, birthday=birthday)
        flash(data_manager.add_user(new_user))
        return redirect('/users')
    return render_template('add_user.html')


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie_from_favs(user_id, movie_id):
    """allows user to delete a movie from their personal list. takes user_id and movie_id
    and deletes movie based on that. shows a success message on the user's personal page
    upon redirect"""
    flash(data_manager.delete_user_movie(user_id, movie_id))
    return redirect(f'/users/{user_id}')


@app.route('/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(movie_id):
    """allows deletion of a movie from the database based on movie_id.
    shows a success message upon redirect to home"""
    flash(data_manager.delete_movie(movie_id))
    return redirect('/')


@app.route('/update_movie', methods=['GET'])
def get_selected_movie_information():
    """first renders update movie template with dropdown menu. when user selected something,
    then refreshes (onchange in html). sets user's title selection to selected"""
    selected_movie = None
    all_movies = data_models.Movie.query.all()
    movie_id = request.args.get('movie_id_select')
    if movie_id is not None:
        selected_movie = data_models.Movie.query.filter_by(id=movie_id).first()
    return render_template('update_movie.html', movies=all_movies, selected_movie=selected_movie)


@app.route('/update_movie', methods=['POST'])
def update_movie():
    """gets id of user's selection (id is hidden in html). gets the input from the form. user
    can choose how many values to change. the desired values for each category are
    sent in to update_movie which commits the changes. redirects to home with a
    flash message"""
    movie_id = request.form.get('movie_id')
    if movie_id is not None:
        year = int(request.form.get('year'))
        director = request.form.get('director')
        rating = float(request.form.get('rating'))
        flash(data_manager.update_movie(movie_id, year, director, rating))
        return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    """renders 404 html template if error 404 occurs"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    """renders 500 html template if error 500 occurs"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
