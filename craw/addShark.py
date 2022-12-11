from mongoDB_init import mainClient, crawlClient
import re
from utils import logExecutionTime
main_userDocs = mainClient['users']
crawl_investorDocs = crawlClient['investors']



def isAddressExisted(address):

    isExisted = False

    for _ in crawl_investorDocs.find({'_id':address},{}):
        isExisted = True

    return isExisted

def addNewAddressHandler():
    findFilter = {'addedSharks.0' : {'$exists' : True}}
    projection = {'addedSharks' : 1, 'userId' : 1}
    r = re.compile(r'^0x[a-fA-F0-9]{40}$')

    validatedETHAddresses = {}
    for main_userDoc in main_userDocs.find(findFilter, projection):

        addresses = main_userDoc['addedSharks']
        
        ETHAddresses = set(filter(r.match, addresses)) 
        
        validatedETHAddresses = validatedETHAddresses.union(ETHAddresses)
    
    for address in validatedETHAddresses:
        if isAddressExisted(address):
            print(f'Duplicate {address}')
            continue

        crawl_investorDocs.insert_one(
            {
                '_id' : address,
                'coins' : {},
                'TXs' : [],
                'is_shark' : False,
                'snapshots' : {},
                'latestBlockNumber' : 0
            }
        )

        print(f'Welcome newbie {address}')


if __name__ == '__main__':
    function = addNewAddressHandler
    logExecutionTime(function)




