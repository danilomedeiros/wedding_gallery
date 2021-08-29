from flask import Blueprint, request, Response, jsonify,make_response
import pymongo
from pymongo import MongoClient
from dao.mongoflask import MongoJSONEncoder, ObjectIdConverter
import json
from bson import json_util
from bson.json_util import dumps
import uuid
from flask_cors import CORS
import uuid
from dao.mongo_utils import db
from .model import Photo,User
from dao.aws import Storage
from bson.objectid import ObjectId

photos_api = Blueprint('photos', __name__)
CORS(photos_api)

photos = db["photos"]
storage = Storage()

@photos_api.route("/photos/list/<filter>", methods=["GET"])
def find_photos(filter):
    print(filter)
    all_photos = list(photos.find({}).sort('_id', pymongo.DESCENDING))
    photos_result = []
    for p in all_photos:
        photos_result.append(Photo(str(p['_id']), p['path'], storage.url(p['path']), p['status']))
    json_return = json.dumps(photos_result, default=vars)
    return  make_response(json_return, 200)

@photos_api.route("/photos/list_page/<filter>", methods=["GET"])
def page(filter):
    print(filter)
    
    limit = 4
    offset =  3 
    
    starting_id = photos.find().sort('_id',pymongo.ASCENDING)
    last_id = starting_id[offset]['_id']
    
    cursor = photos.find({'_id':{'$gte':last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)
    json_return = json.dumps(list(cursor), default=json_util.default)
    return  make_response(json_return, 200)

@photos_api.route("/photos/add", methods =["POST"])
def add():
    print(request)
    f = request.files['file']
    file_format = f.filename.split('.')[1]
    user_id = request.form['user_id']
    
    Photo.build(f, file_format, user_id);
    return make_response(jsonify('ok'), 200)

@photos_api.route("/photos/get/<id>", methods =["GET"])
def get(id):
    print(id)
    photo = photos.find_one({"_id":ObjectId(id)})
    return make_response(jsonify(photo), 200)

@photos_api.route("/photos/delete/<id>", methods =["DELETE"])
def delete(id):
    photo_db = photos.find_one({"_id":ObjectId(id)})
    photos.delete_one({"_id":ObjectId(id)})
    return make_response(jsonify(photo_db), 200)

@photos_api.route("/photos/deleteall", methods =["GET"])
def delete_all():
    photos.remove({})
    return make_response(jsonify('ok'), 200)

@photos_api.route("/photos/changestatus", methods =["POST"])
def change_status():
    data = request.get_json()
    photo_id = data['photo_id']
    status = data['status']
    Photo.update(photo_id, status)
  
    return make_response(jsonify('ok'), 200)
