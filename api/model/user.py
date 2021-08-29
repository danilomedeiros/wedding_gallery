from dao.mongo_utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import jwt
import json

users = db['users']

class User():

    engaged = 'engaged'
    friend = 'friend'

    def __init__(self, _id, name,  email, login=None, password=None, typee=friend):
        self.id = _id
        self.login = login
        self.password = generate_password_hash(password, method='sha256')
        self.type = typee
        self.email = email
        self.name = name


    @classmethod
    def authenticate(cls, login, password):
        if not login:
            return None
        
        user = users.find_one({"login":login})
        
        if not password:
            return None
        if not user or not check_password_hash(user['password'], password):
            return None
        return user

    @classmethod
    def find_one(cls, obj):
        return users.find_one(obj)

    @classmethod
    def find_by_jwt_token(cls, token):
        payload = jwt.decode(token, '123',  algorithms=["HS256"])
        login = payload['sub']
        return User.find_by_login(login)
    
    @classmethod
    def find_by_login(cls, login):
        if(login):
            return users.find_one({'login': login})
        return None

    @classmethod
    def find_by_email(cls, email):
        if(email):
            return users.find_one({'email': email})
        return None
        
    @classmethod
    def add(cls, email, type, login, password):
        user_json =  {"_id": ObjectId(), "login":user.login, "password": user.password, }
        users.insert_one(user_json)
        return user_json

        
    @classmethod
    def add_friend(cls, email):
        user_json =  {"_id": ObjectId(), "login":'', "password": '', "email": email, "typee": User.friend }
        users.insert_one(user_json)
        return user_json

    @classmethod
    def update(cls, email, name, login, password):
        cripo_pass = generate_password_hash(password, method='sha256')
        u = users.find_one_and_update(
            {"email" : email},
            {"$set":
                {"name": name, "login": login, "password": cripo_pass}
            },upsert=True )  
        return u