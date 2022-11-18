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

# TODO Change back to metadatas
metadataDocs = client['test']
tokenDocsSnapshot = client['tokens']
coinDocsSnapshot = client['coins']

metadataAPI = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
cmc_keys = os.environ['cmc_keys']
cmc_keys = [i.strip() for i in cmc_keys.split(',')]

#   'aux': 'urls,logo,description,tags,platform,date_added,notice,status'

parameters = {
    'aux' : 'urls,logo,description,tags,platform,date_added,notice,status'
}
headers = {
    'Accepts': 'application/json',
}

session = Session()


# TODO Using id instead
def crawlSymbols():
    symbols = ''

    for tokenDoc in tokenDocsSnapshot.find():
        tokenSymbol = tokenDoc['symbol']

        symbols += tokenSymbol + ','

    for coinDoc in coinDocsSnapshot.find():
        
        tokenSymbol = coinDoc['symbol']

        symbols += tokenSymbol + ','

    return symbols[:-1]

def crawlIds():
    ids = ''

    for tokenDoc in tokenDocsSnapshot.find():
        tokenId = tokenDoc['id']
        ids += f'{tokenId},'
    
    for coinDoc in coinDocsSnapshot.find():
        coinId = coinDoc['id']
        ids += f'{coinId},'

    return ids[:-1]
    

def mapSymbolById(symbols, ids):
    symbolById = {}

    for id,symbol in zip(ids.split(','),symbols.split(',')):
        symbolById[f'{id}'] = symbol

    
    return symbolById

def crawlMetadata(runTimes):


    headers['X-CMC_PRO_API_KEY'] = cmc_keys[runTimes % len(cmc_keys)]
    session.headers.update(headers)
    
    try:
        symbols = crawlSymbols()
        ids = crawlIds()
        
        symbolById = mapSymbolById(symbols,ids)
        parameters['id'] = ids

        response = session.get(metadataAPI, params=parameters)
        data = json.loads(response.text)

        for id,symbol in symbolById.items():

            if id not in data['data']:
                print(f'Missing {symbol} metadata')
                continue

            metadataObj = data['data'][id]
            print(f'Crawl metadata for {symbol}')

            if metadataObj['tag-groups'] != None:
                metadataObj['tagGroups'] = metadataObj['tag-groups']
                
            del metadataObj['tag-groups']

            if metadataObj['tag-names'] != None:
                metadataObj['tagNames'] = metadataObj['tag-names']
                
            del metadataObj['tag-names']

            # metadataObj['_id'] = symbol
            # metadataDocs.insert_one(metadataObj)
            metadataDocs.update_one(
                {'_id' : symbol},
                {'$set' : metadataObj}
            )
            
            

            


    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)


# while True:
crawlMetadata(0)