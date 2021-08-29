from flask import Blueprint, request, Response, jsonify,make_response
from dao.mongoflask import MongoJSONEncoder, ObjectIdConverter
import json
from bson import json_util
from flask_cors import CORS
import uuid
from .model.photo import Photo
from .model.user import User

photos_api = Blueprint('photos', __name__)
CORS(photos_api)

@photos_api.route("/photos/list_page/<page_num>", methods=["GET"])
def page(page_num):
    page_size = 6
    page = int(page_num)

    auth_header = request.headers.get('Authorization')
    
    user = None
    if auth_header:
        user = User.find_by_jwt_token(auth_header.split(" ")[1])

    pagination = Photo.page(page, page_size, user)
    return  make_response(jsonify(pagination), 200)

@photos_api.route("/photos/add", methods =["POST"])
def add():
    f = request.files['file']
    file_format = f.filename.split('.')[1]
    user_id = request.form['user_id']
    
    Photo.build(f, file_format, user_id);
    return make_response(jsonify('ok'), 200)

@photos_api.route("/photos/changestatus", methods =["POST"])
def change_status():
    data = request.get_json()
    photo_id = data['photo_id']
    status = data['status']
    Photo.update(photo_id, status)
  
    return make_response(jsonify('ok'), 200)
