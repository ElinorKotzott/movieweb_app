import os

from datamanager import data_models
from datamanager.sqlite_data_manager import SQLiteDataManager
from flask import Flask, jsonify, request

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies_users.sqlite')
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
data_models.db.init_app(app)


data_manager = SQLiteDataManager(data_models)


@app.route('/')
def home():
    return 'Welcome to MovieWeb App!'


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return users

@app.route('/users/<user_id>')
def list_user_movies(user_id):
    user_id = request.args.get(user_id)
    user_movies = data_manager.get_user_movies(user_id)
    return user_movies




if __name__ == '__main__':
    app.run(debug=True)

