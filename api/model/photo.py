import pymongo
from pymongo import MongoClient
from dao.mongoflask import MongoJSONEncoder, ObjectIdConverter
import json
from bson import json_util
from bson.json_util import dumps
import uuid
from dao.mongo_utils import db
from .user import User
from dao.aws import Storage
from bson.objectid import ObjectId
import jwt

photos = db['photos']
storage = Storage()

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
            photos_result.append(Photo(str(p['_id']), p['path'], storage.url(p['path']), p['status']))
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
