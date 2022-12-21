import pymongo
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
load_dotenv()

mongodb_password = os.environ['mongodb_password']
mongodb_password = quote_plus(mongodb_password)

connect_string = f'mongodb+srv://hdttuan:{mongodb_password}@cluster0.h09da4d.mongodb.net/?retryWrites=true&w=majority'

crawlClient = pymongo.MongoClient(connect_string)
crawlClient = crawlClient['TRACKINGINVESTMENT_CRAWL']


main_mongodb_password = os.environ['main_mongodb_password']
main_mongodb_password = quote_plus(main_mongodb_password)

main_connect_string = f'mongodb+srv://hdttuan:{main_mongodb_password}@trackinginvestmentmain.4hjg8pg.mongodb.net/TRACKINGINVESTMENT_MAIN?retryWrites=true&w=majority'
mainClient = pymongo.MongoClient(main_connect_string)
mainClient = mainClient['TRACKINGINVESTMENT_MAIN']







