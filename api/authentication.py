from functools import wraps
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, make_response
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

@authentication_api.route('/user/register', methods =["POST"])
def register():
    print('REGISTER')
    data = request.get_json()
    name = data['name']
    email = data['email']
    login = data['login']
    password = data['password']
    user = User.find_by_login(login);
    if (user):
        return make_response('login '+login+' already registered.', 422)
    
    user = User.find_by_email(email);
    if(not user):
        return make_response('invite for '+ email +' not found.', 422)

    User.update(email, name, login, password)
    return make_response('Register done.', 200)

@authentication_api.route('/user/invite', methods =["POST"])
def invite():
    data = request.get_json()
    email = data['email']
    user = User.find_by_email(email);

    if(user):
        return make_response('Email already registered.', 422)
    
    User.add_friend(email)
    return make_response('Friend add.', 200)
