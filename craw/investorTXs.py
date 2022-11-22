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

# NOTE Cur using startBlock = curBlock - 10000
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
    if 'result' in newTXs.json():
        newTXs = newTXs.json()['result']
    else:
        print(newTXs.json())
        time.sleep(1)
        return []

    print(f'Crawling new TXs of {investorAddress} successfully')
    return newTXs
  

def resetInvestorTXs():

    investorDocs.update_many(
        {},
        { '$set' : {'TXs' : []}}
    )
        

def updateInvestorTXs(runTimes, timeGap):

    infura_key = infura_keys[runTimes % len (infura_keys)]
    curBlock = getCurBlock(infura_key)

    
    count = 0
    print(f'crawAllTokenTXs {runTimes}')

    for investor in investorDocs.find():
        count += 1
        ets_key = ets_keys[count % len (ets_keys)]

        investorAddress = investor['_id']

       
        print(f'Processing {investorAddress}')
        


        oldLatestBlock = investor['latestBlockNumber']
        newTXs = getInvestorTXs(oldLatestBlock,curBlock, ets_key, investorAddress)
        

        newLatestBlock = curBlock

        print(f'Updating TXs of {investorAddress}') 
        investorDocs.update_one(
            {'_id' : investorAddress},
            { 
                '$push':{ 
                    'TXs': { 
                            '$each': newTXs
                        } 
                },
                '$set':{
                    'latestBlockNumber' : newLatestBlock
                } 
            }
        )

        
        print(f'Updated TXs of {investorAddress} successfully')

    runTimes += 1

    
def updateInvestorTXs2(runTimes, timeGap):

    infura_key = infura_keys[runTimes % len (infura_keys)]
    curBlock = getCurBlock(infura_key)

    
    investorAddresses = []
    latestBlocks = []
    
    for investorDoc in investorDocs.find({},{'TXs' : 0}):
        investorAddresses.append(investorDoc['_id'])
        latestBlocks.append(investorDoc['latestBlockNumber'])


    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(getInvestorTXs,latestBlock,curBlock,ets_key,investorAddress) 
                    for latestBlock,ets_key,investorAddress in zip(latestBlocks,ets_keys,investorAddresses)]
    except:
        print("Error in multi thread crawling TXs of Investors")

    newLatestBlock = curBlock

    

    for investorAddress, result in zip(investorAddresses, concurrent.futures.as_completed(results)):

        try:
            investorDocs.update_one(
                {'_id' : investorAddress},
                { 
                    '$push':{ 
                        'TXs': { 
                                '$each': result.result()
                            } 
                    },
                    '$set':{
                        'latestBlockNumber' : newLatestBlock
                    } 
                }
            )
        except:
            print(f'Update TXs fail in {investorAddress}')
            print(result.result())
            break
        print(f'Update TXs success in {investorAddress}')


    




# resetInvestorTXs()
updateInvestorTXs2(0,0)

