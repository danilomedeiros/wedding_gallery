from functools import wraps
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import jwt
import json
from .model.user import User
from flask_cors import CORS
from bson.objectid import ObjectId

authentication_api = Blueprint('authentication', __name__)

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
   
    user = User.authenticate(login, password)

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401
 
    token = jwt.encode({
        'sub': user['login'],
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=60)},
        secret_key,  algorithm='HS256')
    response = { 'accessToken': token , 'profile':user}
    return jsonify(response)

@authentication_api.route('/register', methods =["POST"])
def register():
    data = request.get_json()
    login = data['login']
    password = data['password']
    return User.add(login, password), 201