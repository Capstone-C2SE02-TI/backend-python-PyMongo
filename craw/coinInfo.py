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
def newCoinIdHandler():

    f = open('coinId.json')
  
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    getIdAPI = 'https://api.coingecko.com/api/v3/coins/'
    coinIds = [coinDoc['_id'] for coinDoc in coinTestDocs.find({},{'_id' : 1})]
    for i in data:
    
        coinId = i['id']
        if coinId in coinIds:
            continue

        statusCode = -1
        while statusCode != 200:


            print(f'Test isCoin : {coinId}')
            response = requests.get(f'{getIdAPI}{coinId}')

            statusCode = response.status_code

            if statusCode == 404:
                print(f'Dont have info for {coinId}')
                break
            if statusCode != 200:
                print('Next time sleep for 70 Secs')
                time.sleep(70)

                print(response.status_code)
                continue    

            response = response.json()
            if response['asset_platform_id'] == None:

                
                coinTestDocs.insert_one(
                    {'_id' : coinId},
                )

                print(f'Test isCoin success : {coinId}')

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
            print(statusCode)
            continue

        coinData = response.json()

    return coinData

    


def coinDataHandler():

    projection = {'_id' : 1, 'last_updated' : 1}
    for coinDoc in coinTestDocs.find({}, projection):
        idCoin = coinDoc['_id']
        
        print(f'Get data of {idCoin}')
        coinData = getCoinData(idCoin)

        coinTestDocs.update_one(
            {'_id' : idCoin},
            {'$set' : coinData}
        )

        print(f'Get data success of {idCoin}')
        time.sleep(2)


  



fileName = os.path.basename(__file__)
start = time.time()
coinDataHandler()
end = time.time()
print(int(end - start), f'sec to process {fileName}')



