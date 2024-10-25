import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    # Provide the path to your Firebase service account key file
    cred = credentials.Certificate("")
    
    # Initialize Firebase app
    firebase_admin.initialize_app(cred)
    
    # Initialize Firestore
    db = firestore.client()
    
    return db
