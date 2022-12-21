from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import pymongo
import json
load_dotenv()

personal_mongodb_password = os.environ['personal_mongodb_password']
personal_mongodb_password = quote_plus(personal_mongodb_password)

personal_connection_string = f'mongodb+srv://lichnh:{personal_mongodb_password}@personal.r7jxpl0.mongodb.net/?retryWrites=true&w=majority'

personal_client = pymongo.MongoClient(personal_connection_string)
codingDB = personal_client['coding']

proxyDocs = codingDB['proxies']

with open('./utils/activeProxies.json') as activeProxiesFile:
    activeProxies = json.load(activeProxiesFile)
activeProxies = [proxy for proxy in activeProxies.keys()]

with open('./utils/blockProxies.json') as blockProxiesFile:
    blockProxies = json.load(blockProxiesFile)

with open('./utils/lowProxies.json') as lowProxiesFile:
    lowProxies = json.load(lowProxiesFile)

print(lowProxies)