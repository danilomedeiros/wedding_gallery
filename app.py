from dotenv import load_dotenv
from flask import Flask, request, Response, jsonify,make_response,redirect, render_template
from dao.mongoflask import MongoJSONEncoder, ObjectIdConverter
from api.photos import photos_api
from api.comments import comments_api
from api.authentication import authentication_api
from api.likes import likes_api
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="frontend/dist", template_folder="frontend/dist",static_url_path='/')

#app = Flask(__name__, static_folder='./frontend/dist',static_url_path='/')
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.json_encoder = MongoJSONEncoder
app.url_map.converters['objectid'] = ObjectIdConverter
app.register_blueprint(photos_api)
app.register_blueprint(comments_api)
app.register_blueprint(authentication_api)
app.register_blueprint(likes_api)

@app.route('/')
def index():
  return redirect('/gallery')

@app.route('/gallery')
def gallery():
  return render_template('index.html')


@app.route('/login')
def login():
  return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)