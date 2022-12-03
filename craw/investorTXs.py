from dotenv import load_dotenv
import os
import time
load_dotenv()
import requests
from web3 import Web3
from mongoDB_init import client
import concurrent.futures

investorDocs = client['investors']

ets_keys = os.environ['ets_keys']
ets_keys = [i.strip() for i in ets_keys.split(',')]
ets_keys = ets_keys*10000
infura_keys = os.environ['infura_keys'] 
infura_keys = [i.strip() for i in infura_keys.split(',')]


def getCurBlock(infura_key):

    w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))
    curBlock = w3.eth.get_block_number()
    
    return curBlock


def getInvestorTXs(startBlock, curBlock, ets_key, investorAddress):

    pages = 1
    offset = 10000
    newTXs = requests.get('https://api.etherscan.io/api?module=account&action=tokentx&'
            f'address={investorAddress}&'
            f'page={pages}&'
            f'offset={offset}&'
            f'startblock={startBlock}&'
            f'endblock={curBlock}&'
            'sort=asc&'
            f'apikey={ets_key}')
    # print(newTXs.json())
    if newTXs.json()['status'] == '1':
        newTXs = newTXs.json()
        newTXs['investorAddress'] = investorAddress
    else:
        return {}

    print(f'Crawling new TXs of {investorAddress} successfully')
    return newTXs
  

def resetInvestorTXs():

    investorDocs.update_many(
        {},
        { '$set' : {'TXs' : []}}
    )

def setLatestBlockNumber(blockNum = 13919833):

    investorDocs.update_many(
        {},
        { '$set' : {'latestBlockNumber' : blockNum}}
    )


def isFuturesWork():
    
    for investorDoc in investorDocs.find({'TXs.0' : {'$exists' : True}}):

        investorAddress = investorDoc['_id'].lower()
        firstTX = investorDoc['TXs'][0]
        
        FromAddress = firstTX['from'].lower()
        ToAddress = firstTX['to'].lower()

        if (investorAddress not in FromAddress) and (investorAddress not in ToAddress):
            print('Future not working in TXs')
            return

    
def updateInvestorTXs2(runTimes, timeGap):

    infura_key = infura_keys[runTimes % len (infura_keys)]
    curBlock = getCurBlock(infura_key)

    
    investorAddresses = []
    latestBlocks = []
    
    for investorDoc in investorDocs.find({},{'TXs' : 0}):
        investorAddresses.append(investorDoc['_id'])
        latestBlocks.append(investorDoc['latestBlockNumber'])


    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=14) as executor:
            results = [executor.submit(getInvestorTXs,latestBlock,curBlock,ets_key,investorAddress) 
                    for latestBlock,ets_key,investorAddress in zip(latestBlocks,ets_keys,investorAddresses)]
    except:
        print("Error in multi thread crawling TXs of Investors")

    newLatestBlock = curBlock

    waiTest = concurrent.futures.wait(
            results, return_when="ALL_COMPLETED")

    if waiTest.not_done.__len__() != 0:
        print("All the futures not done yet!")
        return

    for response in concurrent.futures.as_completed(results):
        
        try:
            if response.result().get('result',[]) == []:
                continue

            investorAddress = response.result()['investorAddress']

            investorDocs.update_one(
                {'_id' : investorAddress},
                { 
                    '$push':{ 
                        'TXs': { 
                                '$each': response.result()['result']
                        } 
                    },
                    '$set':{
                        'latestBlockNumber' : newLatestBlock
                    } 
                }
            )
        except:
            print(f'Update TXs fail in {investorAddress}')
            print(response.result())
            break
        print(f'Update TXs success in {investorAddress}')






fileName = os.path.basename(__file__)
start = time.time()
# resetInvestorTXs()
# setLatestBlockNumber()
updateInvestorTXs2(0,0)
end = time.time()
print(int(end - start), f'sec to process {fileName}')
# isFuturesWork()

# investorDocs.delete_many(
#     {'TXs.0' : {'$exists' : 0}}
# )
# for investorDoc in investorDocs.find({'TXs.0' : {'$exists' : 0}}):
#     print(investorDoc['_id'])
#     print(investorDoc['TXs'])

    

