from mongoDB_init import client
testDoc = client['tests']
priceUpdate = {
    '2' : 2,
    '3' : 4
}
def initPricesField():

    testDoc.update_many(
            {},
            {"$set" : {'a' : 3}}
    )

