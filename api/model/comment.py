from dao.mongo_utils import db
from bson.objectid import ObjectId
import jwt
import json


class Comment():
    def __init__(self, _id, photo_id, content, date=None):
        self.id = _id
        self.photo_id = photo_id
        self.content = content
        self.data = date