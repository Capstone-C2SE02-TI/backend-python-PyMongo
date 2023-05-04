import json

import json
from mongoDB_init import crawlClient

investorDocs = crawlClient['investors']

addresses = investorDocs.distinct('_id')

for address in addresses:
    la = address.lower()

    if la == '0x72598E10eF4c7C0E651f1eA3CEEe74FCf0A76CF2'.lower():

        print('halo')
projection = {'TXs': 1}
for investorDoc in investorDocs.find({}, projection, batch_size=1, limit=2):

    TXs = investorDoc['TXs']
    _id = investorDoc['_id']
    counter = {}

    print(_id)
    for tx in TXs:
        if 'contractAddress' not in tx:
            continue

        if tx['contractAddress'] in counter:
            continue

        counter[tx['contractAddress']] = {
            'tokenName': tx['tokenName'],
            'tokenSymbol': tx['tokenSymbol']
        }
    investorDocs.update_one(
        {'_id': _id},
        {'$set': {'pair_tradings': counter}}
    )
