from flask import Blueprint, request, Response, jsonify,make_response
import pymongo
from pymongo import MongoClient
from dao.mongoflask import MongoJSONEncoder, ObjectIdConverter
import json
from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps
import uuid
from flask_cors import CORS
import uuid
from dao.aws import Storage
from dao.mongo_utils import db
from .model import Photo

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
        photos_result.append(Photo(str(p['_id']), p['path'], storage.url(p['path'])))
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
    f = request.files['file']
    id = ObjectId()
    file_format = f.filename.split('.')[1]
    path = str(id)+'.'+file_format
    photo = {"_id":id, "path":path}
    photos.insert_one(photo)
    storage.save(path, f)
    
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
