import os
import json
from google.cloud import firestore
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_KEY = json.loads(os.getenv("SERVICE_ACCOUNT_KEY"))

credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_KEY)

db_client = firestore.Client(credentials=credentials)
