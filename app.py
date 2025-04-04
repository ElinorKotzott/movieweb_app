import os
from data_models import db, User, Movie
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies_users.sqlite')
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db.init_app(app)

with app.app_context():
    db.create_all()