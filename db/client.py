from pymongo import MongoClient


DB_URL = ""  # URL to your MongoDB database

db_client = MongoClient(DB_URL).test
