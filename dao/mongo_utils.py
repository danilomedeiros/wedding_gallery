
from dotenv import load_dotenv
from pymongo import MongoClient
import os

cluster = None

if not cluster:
    load_dotenv()
    database_url = os.environ.get('database_url')
    cluster = MongoClient(database_url)

db = cluster["wedding_gallery_db"]