from mongoDB_init import client
import json
investorDocs = client['investors']

totalTX = 0
totalShark = 0
# investorDocs.delete_many(
#     {'TXs.8888' : {'$exists' : True}},
# )
for investorDoc in investorDocs.find({'TXs.0' : {'$exists' : False}}):


    # print(investorDoc['_id'], len(investorDoc['TXs']))
    # totalTX += len(investorDoc['TXs'])
    # print(investorDoc['_id'], )
    totalTX += len(investorDoc['TXs'])
    totalShark += 1

print(f'Total {totalTX}, {totalShark} sharks ')

# for investorDoc in investorDocs.find():
#     print(investorDoc['_id'])
#     print(investorDoc['TXs'][-1]['blockNumber'])
    
#     investorDocs.update_one(
#         {'_id' : investorDoc['_id']},
#         {'$set' : {'latestBlockNumber' : investorDoc['TXs'][-1]['blockNumber']}}
#     )


    # before = 0
    # after = 0
    # investorAddress = investorDoc['_id']
    # print(f'processing {investorAddress}')
    # for TXs in investorDoc['TXs']:
    #     after = int(TXs['timeStamp'])

    #     if after < before:
    #         print(f'{investorAddress}Not in order')
    #         break
    #     print(before,'->',after)
    #     before = after
    # # break
