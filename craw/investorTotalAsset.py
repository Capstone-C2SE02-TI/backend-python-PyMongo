from mongoDB_init import client
import datetime
import time
import os
investorDocs = client['investors']
coinTestDocs = client['coins']

def getLatestTokenPrice():
    priceBySymbol = {}

    filter = {'asset_platform_id' : {'$ne' : None}}
    projection = {'prices' : 1, 'symbol' : 1}
    for coinTestDoc in coinTestDocs.find(filter,projection):
        coinSymbol = coinTestDoc['symbol']
        if 'minutely' not in coinTestDoc['prices']:
            print(f'{coinSymbol} dont have minutely price')
            continue

        minutelyPrice = coinTestDoc['prices']['minutely']
        latestTimeStamp = max(minutelyPrice.keys(), default=0)

        priceBySymbol[coinSymbol] = minutelyPrice.get(latestTimeStamp,0)

    return priceBySymbol


    


def investorTotalAssetSnapshot():

    priceBySymbol = getLatestTokenPrice()
    ms = datetime.datetime.now()
    currentTimestamp = str(int(time.mktime(ms.timetuple()) ))
    
    print(priceBySymbol)
    projection = {'coins' : 1, '_id' : 1}
    for investorDoc in investorDocs.find({},projection):
        investorAddress = investorDoc['_id']

        print(f'Total asset for {investorAddress}')
        totalAsset = 0
        for symbol,balance in investorDoc['coins'].items():
            
            if symbol not in priceBySymbol:
                continue

            tokenAsset = priceBySymbol[symbol] * balance
            totalAsset += tokenAsset

        updateResult = investorDocs.update_one(
            {'_id' : investorAddress},
            {'$set' : {f'snapshots.{currentTimestamp}' : int(totalAsset)}}
        )
        print(totalAsset,updateResult.modified_count)
    
        if updateResult.modified_count == 0:
            print('Cant update in', investorAddress)
            break

def updateSharkStatus():

    sharkTotalAsset = 100000

    # investorDocs.update_many(
    #     {'$gte' : ['totalAsset']}
    # )

    for investorDoc in investorDocs.find({},{'snapshots' : 1}):

        latestUnix = max(investorDoc['snapshots'].keys())

        latestTotalAsset = investorDoc['snapshots'][latestUnix]

        sharkStatus = latestTotalAsset >= sharkTotalAsset

        investorDocs.update_one(
            {'_id' : investorDoc['_id']},
            {'$set' : {'is_shark' : sharkStatus}}
        )

