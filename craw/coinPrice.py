import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from mongoDB_init import crawlClient
import time
from datetime import date, timedelta, datetime
import os
from utils import logExecutionTime
coinTestDocs = crawlClient['coins']

def delPricesField():

    coinTestDocs.update_many(
        {},
        [{'$unset' : 'prices'}]
    )

def initPricesField():

    coinTestDocs.update_many(
        {},
        {'$set': {
            'prices': {
                'daily': {},
                'hourly': {},
                'minutely': {}
            }
        }
        }
    )


def getCoinPrice(id, interval, days):

    parameters = {
        'vs_currency': 'usd',
        'days': days,
        'interval': interval
    }

    statusCode = -1
    while statusCode != 200:

        response = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{id}/market_chart', params=parameters)

        statusCode = response.status_code
        if statusCode == 404:
            print(f'Dont have price for {id}')
            return []

        if statusCode != 200:
            print('Now sleep for 70 Secs')
            print(f'Status error code: {statusCode}')
            time.sleep(65)
            continue

    return response.json()['prices']

def getCoinPriceByRange(id, fromSecUnix, toSecUnix):

    parameters = {
        'vs_currency': 'usd',
        'from' : fromSecUnix,
        'to' : toSecUnix,
    }

    statusCode = -1
    while statusCode != 200:

        response = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{id}/market_chart/range', params=parameters)

        statusCode = response.status_code
        if statusCode == 404:
            print(f'Dont have price for {id}')
            return []

        if statusCode != 200:
            print(f'Now sleep for 70 Secs : {int(time.time())}')
            print(statusCode)
            time.sleep(70)
            print(f'Done sleep, let continue! : {int(time.time())}')
            continue

    return response.json()['prices']


def coinPriceHandler():

    # intervals = ['daily', 'hourly', 'minutely']
    # dayss = ['max', '90', '1']
    intervals = ['daily', 'hourly']
    dayss = ['1', '1']

    coinIds = [coinDoc['_id'] for coinDoc in coinTestDocs.find({}, {'_id': 1})]
    for coinId in coinIds:

        priceUpdate = {}
        for interval, days in zip(intervals, dayss):

            print(f'Getting price {interval} for {coinId}')
            coinPrice = getCoinPrice(coinId, interval, days)

            for miliUnix, price in coinPrice:
                secondUnix = int(miliUnix / 1000)

                priceUpdate[f'prices.{interval}.{secondUnix}'] = price
            time.sleep(2)
            

        coinTestDocs.update_one(
            {'_id': coinId},
            [
                {'$set': priceUpdate}
            ]
        )
        print(f'Get price success for {coinId}')

def coinPriceMinutelyHandler():

    intervalsBySec = {
        'minutely' : 86000
    }
  
    ms = datetime.now()
    currentTimestamp = int(time.mktime(ms.timetuple()))

    print(currentTimestamp - intervalsBySec['minutely'], currentTimestamp)


    fromSecUnix = currentTimestamp - intervalsBySec['minutely']
    toSecUnix = currentTimestamp

    for coinDoc in coinTestDocs.find({}, {'_id' : 1}):

        coinId = coinDoc['_id']

        print(f'Getting price minutely for {coinId}')
        coinPrice = getCoinPriceByRange(coinId, fromSecUnix, toSecUnix)

        priceUpdate = {}
        for miliUnix, price in coinPrice:
            secondUnix = int(miliUnix / 1000)

            priceUpdate[f'prices.minutely.{secondUnix}'] = price
        
        if priceUpdate == {}:
            continue

        coinTestDocs.update_one(
            {'_id': coinId},
            {'$set': priceUpdate}
        )
        print(f'Get price minutely success for {coinId}')

        time.sleep(2)


if __name__ == '__main__':
    function = coinPriceMinutelyHandler
    logExecutionTime(function)
# for unix,price in getCoinPriceByRange('bitcoin','1669255913','1669341913'):
#     ts = int(unix/1000)
#     print(datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S'),price)

# for unix,price in getCoinPrice('bitcoin',interval='daily',days=1):
#     ts = int(unix/1000)
#     print(datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S'),price)
