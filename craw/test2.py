from mongoDB_init import client
testDoc = client['tests']
priceUpdate = {
    '2' : 2,
    '3' : 4
}
def initPricesField():

    testDoc.update_many(
            {},
            {"$addFields":{f'prices.minutely': {"$mergeObjects": [f'prices.minutely', priceUpdate]}}}
    )


initPricesField()