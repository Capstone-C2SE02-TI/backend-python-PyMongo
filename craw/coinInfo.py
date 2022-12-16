from mongoDB_init import crawlClient
import requests
import json
import time
import concurrent.futures
from utils import logExecutionTime, addExecutionTime, getRandomUserAgent
# env variable pre-handler
from dotenv import load_dotenv
import os
from vpn import activeProxiesToJson, getActivateProxiesJson, BlockProxy, addTimeoutProxy, subTimeoutProxy
load_dotenv()

coinTestDocs = crawlClient['coins']


def newCoinIdHandler():

    f = open('coinId.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    getIdAPI = 'https://api.coingecko.com/api/v3/coins/'
    coinIds = [coinDoc['_id'] for coinDoc in coinTestDocs.find({}, {'_id': 1})]
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
                    {'_id': coinId},
                )

                print(f'Test isCoin success : {coinId}')

        time.sleep(2)


def getCoinData(id, proxy, timeout):

    parameter = {
        'localization': 'false',
        'tickers': 'false',
        'market_data': 'true',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }
    headers = {'User-Agent': getRandomUserAgent()}

    COIN_ID_API_URL = f'https://api.coingecko.com/api/v3/coins/{id}'

    statusCode = -1
    retryTimes = 0
    while statusCode != 200:
        retryTimes += 1

        if retryTimes >= 3:
            break
        time.sleep((statusCode != -1) * 70)

        print(f'Crawl data for {id}')
        try:
            response = requests.get(COIN_ID_API_URL, params=parameter, headers=headers, proxies={
                                    'http': proxy, 'https': proxy}, timeout=5)
        except:
            print(f'Get {id} data with proxy {proxy} timeout!')
            addTimeoutProxy(proxy)
            return {}

        statusCode = response.status_code

        if statusCode == 404:
            print(f'Dont have data for {id}')
            return {}

        if statusCode == 403:
            print(f'{proxy} got block by coingecko!')
            BlockProxy(proxy)
            return {}

        if statusCode != 200:
            print('Next time sleep for 70 Secs')
            print(statusCode, proxy)
            continue

        coinData = response.json()

    subTimeoutProxy(proxy)
    return coinData


def coinDataHandler():

    projection = {'_id': 1, 'last_updated': 1}

    activeProxy_to_timeout = getActivateProxiesJson()
    activeProxy = [proxy for proxy in activeProxy_to_timeout.keys()]
    activeProxyLen = activeProxy.__len__()
    executor = concurrent.futures.ThreadPoolExecutor()
    for index, coinDoc in enumerate(coinTestDocs.find({}, projection)):
        idCoin = coinDoc['_id']
        print(f'Get data of {idCoin}')

        proxy = activeProxy[index % activeProxyLen]
        timeout = activeProxy_to_timeout[proxy]
        coinData = getCoinData(idCoin, proxy, timeout)

        if coinData.get('id', None) != idCoin:
            print(f'Fuckdup with the {proxy}')
            activeProxy_to_timeout = getActivateProxiesJson()
            activeProxy = activeProxy = [
                proxy for proxy in activeProxy_to_timeout.keys()]
            activeProxyLen = activeProxy.__len__()
            continue

        executor.submit(
            coinTestDocs.update_one,
            {'_id': idCoin},
            {'$set': coinData}
        )

        print(f'Get data success of {idCoin}, with proxy : {proxy}')
        time.sleep(1)

    executor.shutdown()


if __name__ == '__main__':
    activeProxiesToJson()
    coinDataHandler()
    # function = coinDataHandler
    # executionTime = logExecutionTime(function)
    # addExecutionTime(function.__name__, executionTime)
