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
from mongoDB_init import client
coinDocs = client['coins']


cmc_api = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
cmc_keys = os.environ['cmc_keys']
cmc_keys = [i.strip() for i in cmc_keys.split(',')]

parameters = {
  'start':'1',
  'limit':'10',
  'convert':'USD',
  'sort_dir':'desc',
  'cryptocurrency_type':'coins',
  'aux':'num_market_pairs,cmc_rank,date_added,tags,platform,circulating_supply,volume_24h_reported,volume_7d,volume_7d_reported,volume_30d,volume_30d_reported'
}
headers = {
    'Accepts': 'application/json',
}

session = Session()

def crawCoinInfo(runTimes):


  headers['X-CMC_PRO_API_KEY'] = cmc_keys[runTimes % len(cmc_keys)]
  session.headers.update(headers)
  
  try:
    response = session.get(cmc_api, params=parameters)
    data = json.loads(response.text)



    for coin in data['data']:

      # Upscale later ( now only ETH )
      # Platform len is only 1.
      # Recognize multi eco system by using tags

        coin['TXs'] = []
        coinSlug = coin['slug']
        print(f'Adding {coinSlug} to firebase')
        coinDocs.document(coinSlug).set(coin)
    


  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

  runTimes += 1


def updateCoinInfo(runTimes):


  headers['X-CMC_PRO_API_KEY'] = cmc_keys[runTimes % len(cmc_keys)]
  session.headers.update(headers)
  
  try:
    response = session.get(cmc_api, params=parameters)
    data = json.loads(response.text)


    for coin in data['data']:

        coinSlug = coin['slug']
        print(f'Update {coinSlug} to mongoDB')
        coinDocs.update_one(
          {'id' : coin['id']},
          {'$set' : coin}
        )        
    


  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


updateCoinInfo(0)