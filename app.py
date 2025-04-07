import os

from datamanager import data_models
from datamanager.sqlite_data_manager import SQLiteDataManager
from flask import Flask, jsonify, request, render_template, redirect

from movieweb_app.datamanager.data_models import Movie

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies_users.sqlite')
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
data_models.db.init_app(app)

data_manager = SQLiteDataManager(data_models)


@app.route('/')
def home():
    movies = data_manager.get_all_movies()
    return render_template('index.html', movies=movies)


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return users


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    user_id = request.args.get(user_id)
    user_movies = data_manager.get_user_movies(user_id)
    return user_movies


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = int(request.form.get('year'))
        rating = float(request.form.get('rating'))
        new_movie = Movie(name=name, director=director, year=year, rating=rating)
        data_manager.add_movie(new_movie)
        return redirect('/')

    return render_template('add_movie.html')



if __name__ == '__main__':
    app.run(debug=True)
