from abc import ABC, abstractmethod
from data_models import db


class DataManager:
    from abc import ABC, abstractmethod

    class DataManagerInterface(ABC):

        @abstractmethod
        def get_all_users(self):
            pass


        @abstractmethod
        def get_user_movies(self, user_id):
            pass


