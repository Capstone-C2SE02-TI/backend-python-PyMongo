from mongoDB_init import client
import datetime
import time

investorDocs = client['investors']
coinTestDocs = client['tokensTest']

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

    # TODO get latest price by symbol
    priceBySymbol = getLatestTokenPrice()

    ms = datetime.datetime.now()
    currentTimestamp = str(int(time.mktime(ms.timetuple()) ))
    print(priceBySymbol)
    for investorDoc in investorDocs.find():
        investorAddress = investorDoc['_id']

        print(f'Total asset for {investorAddress}')
        totalAsset = 0
        for symbol,balance in investorDoc['coins'].items():
            
            if symbol not in priceBySymbol:
                continue

            tokenAsset = priceBySymbol.get(symbol,0) * balance
            totalAsset += tokenAsset

        print(totalAsset)
        investorDocs.update_one(
            {'_id' : investorAddress},
            {'$set' : {f'snapshots.{currentTimestamp}' : int(totalAsset)}}
        )

# investorTotalAssetSnapshot()
investorTotalAssetSnapshot()