import os
from pymongo import MongoClient

DB_URL = os.getenv("DB_URL")

db_client = MongoClient(DB_URL).test
