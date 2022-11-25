from mongoDB_init import client
from requests import Session
import requests

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import time

# env variable pre-handler
from dotenv import load_dotenv
import os
load_dotenv()

# coinDocs = client['tokens']
coinTestDocs = client['tokensTest']

cmc_keys = os.environ['cmc_keys']
cmc_keys = [i.strip() for i in cmc_keys.split(',')]


# #TODO contract to cgcId
def crawTokenCGCID():

    getIdAPI = 'https://api.coingecko.com/api/v3/coins/ethereum/contract/'

    for coinDoc in coinTestDocs.find({'cgcId' : {'$exists' : 0}}):

        tokenAddress = coinDoc['_id']
        statusCode = -1
        while statusCode != 200:

            time.sleep( (statusCode != -1) * 70)

            print(f'Crawl cgcId for {tokenAddress}')
            response = requests.get(f'{getIdAPI}{tokenAddress.lower()}')

            statusCode = response.status_code

            if statusCode == 404:
                print(f'Dont have id for {tokenAddress}')
                break
            if statusCode != 200:
                print('Next time sleep for 70 Secs')
                print(response.json())
                continue
                
            cgcId = response.json()['id']

            coinTestDocs.update_one(
                {'_id' : tokenAddress},
                {'$set' : {'cgcId' : cgcId}}
            )

            print(f'Crawl cgcId success for {tokenAddress}')

        time.sleep(2)








def getCoinData(id):

    parameter = {
        'localization' : False,
        'tickers' : False,
        'market_data' : True,
        'community_data' : False,
        'developer_data' : False,
        'sparkline' : False

    }
    APIURL = f'https://api.coingecko.com/api/v3/coins/{id}'


    statusCode = -1
    while statusCode != 200:

        time.sleep( (statusCode != -1) * 70)

        print(f'Crawl data for {id}')
        response = requests.get(APIURL, params=parameter)

        statusCode = response.status_code

        if statusCode == 404:
            print(f'Dont have data for {id}')
            break
        if statusCode != 200:
            print('Next time sleep for 70 Secs')
            print(response.json())
            continue

        coinData = response.json()

    return coinData

    


def coinDataHandler():

    projection = {'_id' : 1, 'last_updated' : 1}
    for coinDoc in coinTestDocs.find({}, projection):
        idCoin = coinDoc['_id']
        
        print(f'Get data of {idCoin}')
        coinData = getCoinData(idCoin)

        oldUpdate = coinDoc['last_updated']
        coinTestDocs.update_one(
            {'_id' : idCoin},
            {'$set' : coinData}
        )
        newUpdate = coinDoc['last_updated']

        print(f'Get data success of {idCoin}')
        time.sleep(2)


  

# crawTokenInfo(0)
# crawTokenCGCID()
# updateTokenInfo(0)
coinDataHandler()



