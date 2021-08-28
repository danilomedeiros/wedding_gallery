from functools import wraps
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app
import jwt
import json
import pymongo
from pymongo import MongoClient
from .model import User
from flask_cors import CORS
from bson.objectid import ObjectId
from dao.mongo_utils import db

authentication_api = Blueprint('authentication', __name__)

users = db["users"]
secret_key = '123'
CORS(authentication_api)

@authentication_api.route('/api/login', methods =["POST"])
def login():
    data = request.get_json()
    login = ''
    password = ''
    if 'login' in data:
        login = data['login']
    if 'password' in data:
        password = data['password']
    
    user_from_db = users.find_one({"login":login})
    user = User.authenticate(user_from_db, password)

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    token = jwt.encode({
        'sub': user['login'],
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        secret_key)
    response = { 'accessToken': token , 'profile':user_from_db}
    print(response)
    return jsonify(response)


@authentication_api.route('/register', methods =["POST"])
def register():
    data = request.get_json()
    login = data['login']
    password = data['password']
    id = ObjectId()
    user = User(id, login, password, User.friend)
    user_json =  {"login":user.login, "password": user.password}
    users.insert_one(user_json)
    return user_json, 201
