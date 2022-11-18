from mongoDB_init import client
import datetime
import time

investorDocs = client['investors']
metadataDocs = client['metadatas']

def getLatestTokenPrice():
    priceBySymbol = {}

    for metadataDoc in metadataDocs.find({'category' : 'token'}):
        if 'hourly' not in metadataDoc['prices']:
            continue

        hourlyPrice = metadataDoc['prices']['hourly']
        latestTimeStamp = max(hourlyPrice.keys())

        tokenSymbol = metadataDoc['symbol']
        priceBySymbol[tokenSymbol] = hourlyPrice[latestTimeStamp]

    return priceBySymbol


    


def investorTotalAssetSnapshot():

    # TODO get latest price by symbol
    priceBySymbol = getLatestTokenPrice()

    ms = datetime.datetime.now()
    currentTimestamp = str(int(time.mktime(ms.timetuple()) * 1000))

    for investorDoc in investorDocs.find():

        totalAsset = 0
        for symbol,balance in investorDoc['coins'].items():
            
            if symbol not in priceBySymbol:
                continue

            tokenAsset = priceBySymbol[symbol] * balance
            totalAsset += tokenAsset

        investorDocs.update_one(
            {'_id' : investorDoc['_id']},
            {'$set' : {f'snapshots.{currentTimestamp}' : int(totalAsset)}}
        )

# investorTotalAssetSnapshot()
investorTotalAssetSnapshot()