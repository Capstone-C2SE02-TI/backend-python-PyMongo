from mongoDB_init import client
testDoc = client['tests']
priceUpdate = {
    'prices.minutely.4' : 2,
    'prices.minutely.5' : 4,
    'prices.daily.3' : 2
}
def initPricesField():

    testDoc.update_many(
            {},
            {'$set': priceUpdate}
    )


initPricesField()