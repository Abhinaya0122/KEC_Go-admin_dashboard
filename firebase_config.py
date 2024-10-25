import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    # Provide the path to your Firebase service account key file
    cred = credentials.Certificate("loginsignup-59e5c-firebase-adminsdk-h86w9-a1acd2374e.json")
    
    # Initialize Firebase app
    firebase_admin.initialize_app(cred)
    
    # Initialize Firestore
    db = firestore.client()
    
    return db
