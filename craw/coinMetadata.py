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

# firebase pre-handler
from firebase_init import client

metadataDocs = client.collection(u'metadata')
coinDocsSnapshot = client.collection(u'coins').get()

metadataAPI = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
cmc_keys = os.environ['cmc_keys']
cmc_keys = [i.strip() for i in cmc_keys.split(',')]

#   'aux': 'urls,logo,description,tags,platform,date_added,notice,status'

parameters = {
}
headers = {
    'Accepts': 'application/json',
}

session = Session()


def crawlSymbols():
    symbols = ''

    for coinDoc in coinDocsSnapshot:
        coinSlug = coinDoc.to_dict()['symbol']

        symbols += coinSlug + ','

    return symbols[:-1]




def crawlTokenMetadata(runTimes):


    headers['X-CMC_PRO_API_KEY'] = cmc_keys[runTimes % len(cmc_keys)]
    session.headers.update(headers)
    
    try:
        
      symbols = crawlSymbols()

      parameters['symbol'] = symbols
      response = session.get(metadataAPI, params=parameters)

      data = json.loads(response.text)


      for symbol in symbols.split(','):
        count = 0

        if symbol not in data['data']:
            print(f'Missing {symbol} metadata')
            continue

        for metadataObj in data['data'][symbol]:
            print(f'Crawl metadata {count}th times for {symbol}')
            count += 1

            if metadataObj['tag-groups'] != None:
                metadataObj['tagGroups'] = metadataObj['tag-groups']
                
            del metadataObj['tag-groups']

            if metadataObj['tag-names'] != None:
                metadataObj['tagNames'] = metadataObj['tag-names']
                
            del metadataObj['tag-names']

            if metadataDocs.document(symbol).get().exists == True:
                metadataDocs.document(symbol).update(metadataObj)
            else:
                metadataDocs.document(symbol).set(metadataObj)
            
            

            


    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)


while True:
    crawlTokenMetadata(0)