from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from dao.mongo_utils import db
from bson.objectid import ObjectId
from dao.aws import Storage
import jwt
import json

storage = Storage()

users = db['users']
photos = db['photos']

class Photo():
    status_pending = 'pending'
    status_on = 'on'
    status_off = 'off' 

    def __init__(self, _id, path, url, status):
        self.id = _id
        self.path = path
        self.url = url
        self.status = status
 
    @classmethod
    def build(cls, file, format, user_id):
        id = ObjectId()
        path = str(id)+'.'+format
        user = User.find_one({'_id':ObjectId(user_id)})
        status = Photo.status_pending
        if(user and user['typee']==User.engaged):
            status = Photo.status_on
        p = {"_id":id, "path":path, "status":status}
        photos.insert_one(p)
        storage.save(path, file)
        return p

    @classmethod
    def update(cls, photo_id, status):
        p = photos.find_one_and_update(
            {"_id" : ObjectId(photo_id)},
            {"$set":
                {"status": status}
            },upsert=True )  
        return p

    @classmethod
    def page(cls, page, page_size, user):
        if(not user or user['typee'] == User.friend ):
            query = {'status':'on'}
        else:
            query = {}
        skips = page_size * (page - 1)
        cursor = photos.find(query).skip(skips).limit(page_size)
        
        all_photos = list(cursor)
        photos_result = []
        for p in all_photos:
            photos_result.append(Photo(3, p['path'], storage.url(p['path']), p['status']))
        json_photos = json.dumps(photos_result, default=vars)

        total = cursor.count();
        
        total_pages = (total + page_size - 1) // page_size
        pagination = {
            "totalItems": total,
            "photos": json_photos,
            "totalPages": total_pages,
            "currentPage": page
        }
        return pagination


class User():

    engaged = 'engaged'
    friend = 'friend'

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