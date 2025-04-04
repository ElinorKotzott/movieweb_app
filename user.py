class User:
    _id_counter = 0

    def __init__(self, name):
        self.name = name
        self.user_id = User._id_counter
        User._id_counter =+ 1

