from flask import Blueprint, request, Response, jsonify,make_response
import pymongo
import json
from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps
import uuid
from flask_cors import CORS
import uuid
from dao.aws import Storage
import time
from dao.mongo_utils import db

#add photo, user_id
#delete photo, user_id

likes_api = Blueprint('likes', __name__)
CORS(likes_api)

likes = db["likes"]
storage = Storage()

@likes_api.route("/likes/add", methods =["POST"])
def add():
    print('likes.add')
    data = request.json
    print (data)
    user_id = data['user_id']
    photo_id = data['photo_id']
    id = ObjectId()
    like = {"_id":id, "user_id":user_id, "photo_id":photo_id} 
    likes.insert_one(like)
    return  make_response(like, 200)

@likes_api.route("/likes/delete", methods =["POST"])
def delete():
    data = request.json
    user_id = data['user_id']
    photo_id = data['photo_id']
    likes.delete_many({'photo_id':photo_id, 'user_id': user_id})
    return  make_response('deleted', 200)

@likes_api.route("/likes/count/<photo_id>/<user_id>", methods=["GET"])
def count(photo_id, user_id):
    total_likes_photo_user = likes.find({'photo_id':photo_id, 'user_id': user_id}).count()
    total_likes_photo      = likes.find({'photo_id':photo_id}).count()
    totals = [total_likes_photo, total_likes_photo_user]
    return make_response(jsonify(totals), 200)


@likes_api.route("/likes/get/<id>", methods =["GET"])
def get(id):
    like = likes.find_one({"_id":ObjectId(id)})
    return make_response(jsonify(like), 200)

@likes_api.route("/likes/deleteall", methods =["GET"])
def delete_all():
    likes.remove({})
    return make_response(jsonify('ok'), 200)

@likes_api.route("/likes/list/<photo_id>/<user_id>", methods=["GET"])
def find_likes(photo_id, user_id):
    all_likes = list(likes.find({'photo_id':photo_id, 'user_id': user_id}).sort('_id', pymongo.DESCENDING))
    likes_result = []
    for p in all_likes:
        like = {"id":str(p['_id']), "user_id":p['user_id'], "photo_id":p['photo_id'], "type":p['type']} 
        likes_result.append(like)
    json_return = json.dumps(likes_result, default=json_util.default)
    return  make_response(json_return, 200)
