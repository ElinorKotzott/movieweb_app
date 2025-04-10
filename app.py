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
    movies = data_manager.get_all_movies()
    return render_template('index.html', movies=movies)


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('list_users.html', users=users)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    user = data_models.User.query.get(user_id)
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_movies=user_movies, user=user)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
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


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        birthday_str = request.form.get('birthday')
        birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
        new_user = data_models.User(name=name, birthday=birthday)
        flash(data_manager.add_user(new_user))
        return redirect('/')
    return render_template('add_user.html')


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie_from_favs(user_id, movie_id):
    flash(data_manager.delete_user_movie(user_id, movie_id))
    return redirect(f'/users/{user_id}')


@app.route('/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(movie_id):
    flash(data_manager.delete_movie(movie_id))
    return redirect('/')


@app.route('/update_movie', methods=['GET', 'POST'])
def update_movie():
    all_movies = data_models.Movie.query.all()
    selected_movie = None
    if request.method == 'POST':
        movie_id = request.form.get('title')

        if movie_id and not request.form.get('year'):
            selected_movie = data_models.Movie.query.filter_by(id=movie_id).first()

        elif movie_id and request.form.get('year'):
            selected_movie = data_models.Movie.query.filter_by(id=movie_id).first()
            selected_movie.year = int(request.form.get('year'))
            selected_movie.director = request.form.get('director')
            selected_movie.rating = float(request.form.get('rating'))
            flash(data_manager.update_movie(selected_movie))
        return redirect('/')

    return render_template('update_movie.html', movies=all_movies, selected_movie=selected_movie)


if __name__ == '__main__':
    app.run(debug=True)
