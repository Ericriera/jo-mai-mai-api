from google.cloud import firestore

db_client = firestore.Client.from_service_account_json("./serviceAccountKey.json")
