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
import time
from dao.mongo_utils import db


comments_api = Blueprint('comments', __name__)
CORS(comments_api)
comments = db["comments"]

@comments_api.route("/comments/list/<photo_id>", methods=["GET"])
def find_comments(photo_id):
    all_comments = list(comments.find({'photo_id':photo_id}).sort('_id', pymongo.DESCENDING))
    comments_result = []
    for p in all_comments:
        comment = {"id":str(p['_id']), "author":p['author'], "photo_id":p['photo_id'], "content":p['content'], "date":p['date']} 
        comments_result.append(comment)
    json_return = json.dumps(comments_result, default=json_util.default)
    return  make_response(json_return, 200)

@comments_api.route("/comments/list_page/<filter>", methods=["GET"])
def page(filter):
    
    limit = 4
    offset =  3 
    
    starting_id = comments.find().sort('_id',pymongo.ASCENDING)
    last_id = starting_id[offset]['_id']
    
    cursor = comments.find({'_id':{'$gte':last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)
    json_return = json.dumps(list(cursor), default=json_util.default)
    return  make_response(json_return, 200)

@comments_api.route("/comments/add", methods =["POST"])
def add():
    data = request.json
    print (data)
    author = data['author']
    content = data['content']
    photo_id = data['photo_id']

    id = ObjectId()
    comment = {"_id":id, "author":author, "photo_id":photo_id, "content":content, "date":time.time()} 
    comments.insert_one(comment)
    return  make_response(comment, 200)

@comments_api.route("/comments/get/<id>", methods =["GET"])
def get(id):
    comment = comments.find_one({"_id":ObjectId(id)})
    return make_response(jsonify(comment), 200)

@comments_api.route("/comments/delete/<id>", methods =["DELETE"])
def delete(id):
    comment_db = comments.find_one({"_id":ObjectId(id)})
    comments.delete_one({"_id":ObjectId(id)})
    return make_response(jsonify(comment_db), 200)

@comments_api.route("/comments/deleteall", methods =["GET"])
def delete_all():
    comments.remove({})
    return make_response(jsonify('ok'), 200)
