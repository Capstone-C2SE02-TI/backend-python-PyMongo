from heapq import merge
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from mongoDB_init import client
import time
from datetime import date, timedelta


coinDocs = client['coins']
tokenDocs = client['tokens']
metadataDocs = client['metadatas']
idsConvert = json.load( open('./id-CMCToCGC.json'))


# NOTE If hourly , days only 90
parameters = {
    'vs_currency' : 'usd',
    'days' : 'max'
}
headers = {
    'Accepts': 'application/json'
}

session = Session()
session.headers.update(headers)

def initPricesField(id):

    havePricesDoc = metadataDocs.find({'prices' : { '$exists' : False}})

    for doc in havePricesDoc:
        print(doc['_id'])
    
   

    
def crawlCoinPrice(id, interval, symbol):
    time.sleep(2)
    parameters['interval'] = interval

    if id in idsConvert['data']:
        requestId = idsConvert['data'][id]
    else:
        requestId = id


    try:
        response = session.get(f'https://api.coingecko.com/api/v3/coins/{requestId}/market_chart', params=parameters, timeout=5)
    except:
        print(f'Timeout for {requestId}')
        return False

    data = json.loads(response.text)

    if 'error' in data:
        print(f'Dont have price in {requestId}')
        return False

    try:
        prices = data['prices']
        print(f'Crawl {requestId} price')
    except:
        print(f'This shit {requestId} gone wrong')
        print(data)
        return False
    
    for price in prices:
        unix, intervalPrice = price
        # TODO Change here
        updateStatus = metadataDocs.update_one(
                    {'_id' : symbol},
                    {'$set': {f'prices.{interval}.{unix}' : intervalPrice} }
                )
        print(f'add {symbol} data => {unix} : {intervalPrice} ')
    return True



def crawlAllCoinPrice():

    c = 0
    f = 0

    # for coinDoc in coinDocs.find():
    #     c += 1
    #     f += (crawlCoinPrice(coinDoc['_id'], 'daily', coinDoc['symbol']) == False)

    print('now is get token docs')

    # TODO Prices token fail ~50%
    
    tokenSlugs = []
    tokenSymbols = []
    for tokenDoc in tokenDocs.find():
        
        tokenSlugs.append(tokenDoc['slug'])
        tokenSymbols.append(tokenDoc['symbol'])
        
    for tokenSlug,tokenSymbol in zip(tokenSlugs,tokenSymbols):
        c += 1
        isCrawlSuccess = crawlCoinPrice(tokenSlug, 'hourly', tokenSymbol)
        f += isCrawlSuccess


    print(float((c-f)/c))


# crawlCoinPrice('ethereum','daily')
crawlAllCoinPrice()
# crawlCoinPrice('polkadot','daily','DOT')

        

    