from mongoDB_init import crawlClient
import datetime
import time
import os
import concurrent.futures
from utils import logExecutionTime
investorDocs = crawlClient['investors']
coinTestDocs = crawlClient['coins']


def getLatestTokenPrice():
    priceBySymbol = {}

    filter = {'asset_platform_id': {'$ne': None}}
    projection = {'prices': 1, 'symbol': 1}
    for coinTestDoc in coinTestDocs.find(filter, projection):
        coinSymbol = coinTestDoc['symbol']
        if 'minutely' not in coinTestDoc['prices']:
            print(f'{coinSymbol} dont have minutely price')
            continue

        minutelyPrice = coinTestDoc['prices']['minutely']
        latestTimeStamp = max(minutelyPrice.keys(), default=0)

        priceBySymbol[coinSymbol] = minutelyPrice.get(latestTimeStamp, 0)

    return priceBySymbol


def investorTotalAssetSnapshot():

    priceBySymbol = getLatestTokenPrice()
    ms = datetime.datetime.now()
    currentTimestamp = str(int(time.mktime(ms.timetuple())))

    totalAssetByAddress = {}
    projection = {'coins': 1, '_id': 1}
    for investorDoc in investorDocs.find({}, projection):
        investorAddress = investorDoc['_id']

        print(f'Total asset for {investorAddress}')
        totalAsset = 0
        for symbol, balance in investorDoc['coins'].items():

            if symbol not in priceBySymbol:
                continue

            tokenAsset = priceBySymbol[symbol] * balance
            totalAsset += tokenAsset
        totalAssetByAddress[investorAddress] = totalAsset

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futureResults = [
            executor.submit(
                investorDocs.update_one,
                {'_id': investorAddress},
                [{
                    '$set': {
                        f'snapshots.{currentTimestamp}':
                            int(totalAsset)
                    }
                },
                    {
                        '$set': {
                            'snapshot':
                            totalAsset
                        }}])
            for investorAddress, totalAsset in totalAssetByAddress.items()
        ]

    waitResult = concurrent.futures.wait(
        futureResults, return_when="ALL_COMPLETED")

    if waitResult.not_done.__len__() != 0:
        print("All the futures not done yet!")
        return False


def investorTotalAssetSnapshot2():

    priceBySymbol = getLatestTokenPrice()
    ms = datetime.datetime.now()
    currentTimestamp = str(int(time.mktime(ms.timetuple())))

    projection = {'coins': 1, '_id': 1}
    with concurrent.futures.ThreadPoolExecutor() as executor:

        for investorDoc in investorDocs.find({}, projection):
            investorAddress = investorDoc['_id']

            print(f'Total asset for {investorAddress}')
            totalAsset = 0
            for symbol, balance in investorDoc['coins'].items():

                if symbol not in priceBySymbol:
                    continue

                tokenAsset = priceBySymbol[symbol] * balance
                totalAsset += tokenAsset

            executor.submit(investorDocs.update_one, {'_id': investorAddress}, [{'$set': {f'snapshots.{currentTimestamp}': int(totalAsset)}},
                                                                                {'$set': {
                                                                                    'snapshot': totalAsset}}
                                                                                ]
            )


def updateSharkStatus():

    sharkTotalAsset = 100000
    

    investorDocs.update_many(
        {'snapshot' : {'$gte' : sharkTotalAsset}},
        {'$set': {'is_shark': True}}
    )

    investorDocs.update_many(
        {'snapshot' : {'$lt' : sharkTotalAsset}},
        {'$set': {'is_shark': False}}
    )
  


# investorDocs.update_many(
#     {},
#     {'$set' : {'snapshot' : 0}}
# )
if __name__ == '__main__':
    function = updateSharkStatus
    logExecutionTime(function)
    
