import os
from movieweb_app.datamanager.data_models import db
from flask import Flask

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'movies_users.sqlite')
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db.init_app(app)

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

if __name__ == '__main__':
    app.run(debug=True)



#with app.app_context():
#    db.create_all()