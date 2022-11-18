from email import header
from email.quoprimime import quote
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import time

# env variable pre-handler
from dotenv import load_dotenv
import os
load_dotenv()

from mongoDB_init import client


tagDocs = client['tags']
metadataDocs = client['metadata']

tagsAPI = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories'
cmc_keys = os.environ['cmc_keys']
cmc_keys = [i.strip() for i in cmc_keys.split(',')]

#   'aux': 'urls,logo,description,tags,platform,date_added,notice,status'

parameters = {
    'start' : 1,
    'limit' : 5000
}
headers = {
    'Accepts': 'application/json',
}

session = Session()


# TODO Chu thuong gach ngang
def crawlTags(runTimes):


    headers['X-CMC_PRO_API_KEY'] = cmc_keys[runTimes % len(cmc_keys)]
    session.headers.update(headers)
    
    try:
        
        response = session.get(tagsAPI, params=parameters)
        data = json.loads(response.text)
        
        for tag in data['data']:

            tag['_id'] = tag['id']
            del tag['id']
            tagDocs.insert_one(tag)
            

            


    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)


def test():

    for tag in tagDocs.find():
        tagName = tag['name']
        tagTitle = tag['title']
        if tagName != tagTitle:
            print(f'{tagName} diff {tagTitle}')

def addCoinToTagCollection():

    for metadataDoc in metadataDocs.find():

        if 'tagNames' not in metadataDoc:
            continue
        
        metadataDocid = metadataDoc['id']
        metadataDoc_id = metadataDoc['_id']
        for tagName in metadataDoc['tagNames']:
            tagDocs.update_many(
                {'name' : tagName},
                {'$inc' : {'num_tokens' : 1}},
            )

            tagDocs.update_many(
                {'name' : tagName},
                {'$set': {f'coins.{metadataDocid}' : f'{metadataDoc_id}'} }
            )


def test():

    tagDocs.update_many(
        {},
        [{'$set' : {'num_tokens' : 0}}],
    )
    
# while True:
# crawlTags(0)
addCoinToTagCollection()


