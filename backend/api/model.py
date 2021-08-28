from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

class Photo():
    def __init__(self, _id, path, url=''):
        self.id = _id
        self.path = path
        self.url = url

class User():

    engaged = 'ENGAGED'
    friend = 'FRIEND'

    def __init__(self, _id, login, password, typee=friend):
        self.id = _id
        self.login = login
        self.password = generate_password_hash(password, method='sha256')
        self.type = typee
    
    @classmethod
    def authenticate(cls, user, password):
        if not password:
            return None
        if not user or not check_password_hash(user['password'], password):
            return None
        return user

class Like():
    def __init__(self, _id, photo_id, user_id):
        self.id = _id
        self.photo_id = photo_id
        self.user_id = user_id

class Comment():
    def __init__(self, _id, photo_id, content, date=None):
        self.id = _id
        self.photo_id = photo_id
        self.content = content
        self.data = date