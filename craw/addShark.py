from mongoDB_init import mainClient, client
import re

main_userDocs = mainClient['users']
crawl_investorDocs = client['investors']



def isAddressExisted(address):

    isExisted = False

    for _ in crawl_investorDocs.find({'_id':address}):
        isExisted = True

    return isExisted
        
def addNewAddressHandler():
    findFilter = {'addedSharks.0' : {'$exists' : True}}
    projection = {'addedSharks' : 1, 'userId' : 1}
    for main_userDoc in main_userDocs.find(findFilter, projection):

        addedAddresses = main_userDoc['addedSharks']
        
        r = re.compile(r'^0x[a-fA-F0-9]{40}$')
        validatedAddresses = list(filter(r.match, addedAddresses)) 
        
        for address in validatedAddresses:
            if not isAddressExisted(address):
                crawl_investorDocs.insert_one(
                    {
                        '_id' : address,
                        'coins' : {},
                        'TXs' : [],
                        'is_shark' : [],
                        'snapshots' : {},
                        'latestBlockNumber' : 0
                    }
                )

                print(f'Welcome newbie {address}')
            else:
                print(f'Duplicate {address}')

crawl_investorDocs.delete_one(
    {'_id' : '0x28c6c06298d514db089934071355e5743bf21d60'}
)
addNewAddressHandler()




