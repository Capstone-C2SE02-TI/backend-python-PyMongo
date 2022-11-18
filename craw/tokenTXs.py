from webbrowser import get
from dotenv import load_dotenv
import os
import time
load_dotenv()
import requests
from web3 import Web3
from mongoDB_init import client
tokenDocs = client['tokens']

ets_keys = os.environ['ets_keys']
ets_keys = [i.strip() for i in ets_keys.split(',')]
infura_keys = os.environ['infura_key'] 
infura_keys = [i.strip() for i in infura_keys.split(',')]


# TODO store the last crawled block in some where else.
lastBlock = 15501400

# TODO feat: get latest block by using web3 to save credit in ets
def getCurBlock(infura_key):
    w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))
    curBlock = w3.eth.get_block_number()
    
    return curBlock

# NOTE Cur using startBlock = curBlock - 10
def getLatestTokenTXs(runTimes,timeGap, contractAddress):

    curBlock = getCurBlock(runTimes)

    # Get new txs in etherscan
    newTXs = requests.get('https://api.etherscan.io/api?module=account&action=tokentx&'
            f'contractaddress={contractAddress}&'
            'page=1&offset=10000 &'
            f'startblock={int(curBlock)-10}&'
            f'endblock={curBlock}&'
            'sort=asc&'
            f'&apikey={ets_keys[runTimes % len(ets_keys)]}')
    newTXs = newTXs.json()['result']

    return newTXs

# TODO craw txs of all docs in tokens collection
# crawTokenTXs(0,0,'0xdac17f958d2ee523a2206206994597c13d831ec7')

def updateAllTokenTXs():

    runTimes = 0
    timeGap = 0


    print(f'crawAllTokenTXs {runTimes}')
    for tokenDoc in tokenDocs.find():

        tokenName = tokenDoc['name']
        print(f'Processing {tokenName}')
        getLatestTokenTXs(runTimes, timeGap, tokenDoc['_id'])


# getLatestTokenTXs(0,0,'0xdac17f958d2ee523a2206206994597c13d831ec7')
updateAllTokenTXs()
# print(getCurBlock(0))
