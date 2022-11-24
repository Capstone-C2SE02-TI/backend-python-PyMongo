import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from mongoDB_init import client
import time
from datetime import date, timedelta, datetime


coinTestDocs = client['tokensTest']






def initPricesField():

    coinTestDocs.update_many(
        {},
        {'$set' : {
            'prices' : {
                'daily' : {},
                'hourly' : {},
                'minutely' : {}
            }
            }
        }
    )
    
   

    
def getCoinPrice(cgcId, interval, days):

    parameters = {
        'vs_currency' : 'usd',
        'days' : days,
        'interval' : interval
    }

    
    statusCode = -1
    while statusCode != 200:

        response = requests.get(f'https://api.coingecko.com/api/v3/coins/{cgcId}/market_chart', params=parameters)

        statusCode = response.status_code
        if statusCode == 404:
            print(f'Dont have price for {cgcId}')
            return []

        if statusCode != 200:
            print('Now sleep for 70 Secs')
            print(response.json())
            time.sleep(65)
            continue



    return response.json()['prices']



def coinPriceHandler():

    for coinDoc in coinTestDocs.find({}, {'cgcId': 1}):
        
        coinId = coinDoc['cgcId']

        interval = 'daily'
        days = 'max'

        print(f'Getting price for {coinId}')
        coinPrice = getCoinPrice(coinId,interval,days)
        priceUpdate = {}

        for miliUnix,price in coinPrice:
            secondUnix = int(miliUnix / 1000)
             
            priceUpdate[f'{interval}.{secondUnix}'] = price

        coinTestDocs.update_one(
            {'cgcId' : coinId},
            {'$set' : priceUpdate}
        )

        print(f'Get price success for {coinId}')

        time.sleep(5)


coinPriceHandler()
# for unix,price in getCoinPrice('bitcoin','minutely','1','abc')['prices']:
#     ts = int(unix/1000)
#     print(datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S'),price)

        

    