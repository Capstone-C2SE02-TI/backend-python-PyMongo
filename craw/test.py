from mongoDB_init import crawlClient



coinDocs = crawlClient['coins']

print(coinDocs.update_one(
    {'symbol' : 'raca'},
    {'$set' : {'sumInvest' : 1}}
).modified_count)

