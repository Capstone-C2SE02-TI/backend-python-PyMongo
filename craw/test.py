from mongoDB_init import crawlClient
from pprint import pprint
investorDocs = crawlClient['investors']


for coinDoc in investorDocs.find({},{'coins' : 1}):
    pprint(coinDoc)

    break