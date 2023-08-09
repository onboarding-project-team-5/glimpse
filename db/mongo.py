from pymongo import MongoClient
from certifi import where

DB_URL = ''
client = MongoClient(DB_URL, tlsCAFile=where())

db = client.dbsparta