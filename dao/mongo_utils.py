
from pymongo import MongoClient

cluster = None

if not cluster:
    cluster = MongoClient("mongodb+srv://wedding_gallery:wedding_gallery@cluster0.gbp8l.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["wedding_gallery_db"]