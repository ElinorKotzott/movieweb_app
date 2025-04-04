from flask_sqlalchemy import SQLAlchemy
from data_manager import DataManager

class SQLiteDataManager(DataManager):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)