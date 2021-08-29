from flask import Blueprint, request, Response, jsonify,make_response
from bson import json_util
from flask_cors import CORS
from .model.like import Like

likes_api = Blueprint('likes', __name__)
CORS(likes_api)

@likes_api.route("/likes/add", methods =["POST"])
def add():
    data = request.json
    print (data)
    user_id = data['user_id']
    photo_id = data['photo_id']
    like = Like.build(user_id, photo_id)
    return  make_response(like, 200)

@likes_api.route("/likes/delete", methods =["POST"])
def delete():
    data = request.json
    user_id = data['user_id']
    photo_id = data['photo_id']
    Like.delete(user_id, photo_id)
    return  make_response('deleted', 200)

@likes_api.route("/likes/count/<photo_id>/<user_id>", methods=["GET"])
def count(photo_id, user_id):
    totals = Like.statistic(user_id, photo_id)
    return make_response(jsonify(totals), 200)
