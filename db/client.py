import os
from pymongo import MongoClient

DB_URL = os.getenv("DB_URL")
ENV = os.getenv("ENV")

db_client = MongoClient(DB_URL)[ENV]
