
import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate('../capstone-c1se04-ti-crawl-firebase-adminsdk-lgmmw-49a1da3270.json')
firebase_admin.initialize_app(cred)
client = firestore.client()



