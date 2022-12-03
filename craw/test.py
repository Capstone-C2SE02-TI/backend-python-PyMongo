from mongoDB_init import client

investorDocs = client['investors']

for investorDoc in investorDocs.find({'TXs.11' : {'$exists' : 0}},{'TXs' : 1}):
    investorTXs = investorDoc['TXs']

    currentNonce = len(investorTXs)
    
    print(investorDoc['_id'], currentNonce)


