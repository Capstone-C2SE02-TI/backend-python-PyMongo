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
tokenDocs = client['tokens']

#  TODO Transfer to mongoDB
cmc_api = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
cmc_keys = os.environ['cmc_keys']
cmc_keys = [i.strip() for i in cmc_keys.split(',')]

# NOTE change aux when crawl data again
parameters = {
  'start':'1',
  'limit':'120',
  'convert':'USD',
  'sort_dir':'desc',
  'cryptocurrency_type':'tokens',
  'aux':'platform,num_market_pairs,cmc_rank,date_added,tags,circulating_supply,volume_24h_reported,volume_7d,volume_7d_reported,volume_30d,volume_30d_reported'
}
headers = {
    'Accepts': 'application/json',
}

session = Session()

def crawTokenInfo(runTimes):


  headers['X-CMC_PRO_API_KEY'] = cmc_keys[runTimes % len(cmc_keys)]
  session.headers.update(headers)
  
  try:
    response = session.get(cmc_api, params=parameters)
    data = json.loads(response.text)


    for token in data['data']:

      # Upscale later ( now only ETH )
      # Platform len is only 1.
      # Recognize multi eco system by using tags
      
      if token['platform'] != None:
          if token['platform']['symbol'] == 'ETH':
            continue
          else:
            print(token)
            break
    


  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

  runTimes += 1


def updateTokenInfo(runTimes):


  headers['X-CMC_PRO_API_KEY'] = cmc_keys[runTimes % len(cmc_keys)]
  session.headers.update(headers)
  
  try:
    response = session.get(cmc_api, params=parameters)
    data = json.loads(response.text)


    for token in data['data']:

      # Upscale later ( now only ETH )
      # Platform len is only 1.
      # Recognize multi eco system by using tags
      if token['platform'] != None:
          if token['platform']['symbol'] == 'ETH':

            tokenSlug = token['slug']
            print(f'Update {tokenSlug} to mongoDB')
            tokenDocs.update_one(
              {'id' : token['id']},
              {'$set' : token}
            )

  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


updateTokenInfo(0)