from dao.mongo_utils import db
from bson.objectid import ObjectId
import jwt
import json

likes = db["likes"]

class Like():
    def __init__(self, _id, photo_id, user_id):
        self.id = _id
        self.photo_id = photo_id
        self.user_id = user_id

    @classmethod
    def build(cls, user_id, photo_id):
        id = ObjectId()
        like = {"_id":id, "user_id":user_id, "photo_id":photo_id} 
        likes.insert_one(like)
        return like

    @classmethod
    def delete(cls, user_id, photo_id):
        likes.delete_many({'photo_id':photo_id, 'user_id': user_id})
        return True

    @classmethod
    def statistic(cls, user_id, photo_id):
        total_likes_photo_user = likes.find({'photo_id':photo_id, 'user_id': user_id}).count()
        total_likes_photo      = likes.find({'photo_id':photo_id}).count()
        totals = [total_likes_photo, total_likes_photo_user]
        return totals;  