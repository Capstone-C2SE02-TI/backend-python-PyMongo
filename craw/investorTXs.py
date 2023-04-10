import concurrent.futures

from hexbytes import HexBytes
from utils import logExecutionTime
from mongoDB_init import crawlClient
from web3 import Web3
import requests
from dotenv import load_dotenv
import os
import time
import random
load_dotenv()

investorDocs = crawlClient['investors']

ets_keys = os.environ['ets_keys']
ets_keys = [i.strip() for i in ets_keys.split(',')]
ets_keys = ets_keys*10000
infura_keys = os.environ['infura_keys']
infura_keys = [i.strip() for i in infura_keys.split(',')]

routers = ['0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D','0xEfF92A263d31888d860bD50809A8D171709b7b1c','0xf164fC0Ec4E93095b804a4795bBe1e041497b92a','0x13f4EA83D0bd40E75C8222255bc855a974568Dd4']
rOldLen = len(routers)
for i in range(rOldLen):
    routers.append(routers[i].lower())
print(routers)
def getTransactionInput(hash, mainnet = False):
    infura_key = infura_keys[random.randint(1,len(infura_keys))-1]
    print(infura_key)
    if mainnet:
        url = 'https://mainnet.infura.io/v3/'
    else:
        url = 'https://goerli.infura.io/v3/'
    w3 = Web3(Web3.HTTPProvider(f'{url}{infura_key}'))

    txData = {'accessList': [], 
         'blockHash': HexBytes('0xfd1838979ee036d833b76beca9b94182b7606db4cc9071790db548a0d7a50eaf'), 
         'blockNumber': 8733005, 
         'chainId': '0x5', 
         'from': '0x72598E10eF4c7C0E651f1eA3CEEe74FCf0A76CF2', 
         'gas': 213948, 
         'gasPrice': 119389272035, 
         'hash': HexBytes('0x9c4379b86845eab75fe72aacc48da8ae167d436cc7f9c5bd331973a5714bd755'), 
         'input': '0x7ff36ab5000000000000000000000000000000000000000000000000000000013433ba5a000000000000000000000000000000000000000000000000000000000000008000000000000000000000000072598e10ef4c7c0e651f1ea3ceee74fcf0a76cf2000000000000000000000000000000000000000000000000000000006422f5f80000000000000000000000000000000000000000000000000000000000000002000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d600000000000000000000000007865c6e87b9f70255377e024ace6630c1eaa37f',
         'maxFeePerGas': 225945214370, 
         'maxPriorityFeePerGas': 1000000000, 
         'nonce': 269, 
         'r': HexBytes('0x498e7d9c30119b047c4a6b626d380bfc3b7479761d75974326452270ad456902'), 
         's': HexBytes('0x790b7a6c5ba382b9280a46fc1c0a164126c54ea00a7273740a2bd1c454bcbfe6'), 
         'to': '0xEfF92A263d31888d860bD50809A8D171709b7b1c', 
         'transactionIndex': 211, 
         'type': '0x2', 
         'v': 1, 
         'value': 1000000000000000000}
    txData = w3.eth.get_transaction(hash)

    return txData['input']


def getCurBlock(infura_key):

    w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))
    curBlock = w3.eth.get_block_number()

    return curBlock


def getInvestorTXs(startBlock, curBlock, ets_key, investorAddress):

    pages = 1
    offset = 10000
    try:
        newTXs = requests.get('https://api.etherscan.io/api?module=account&action=txlist&'
                              f'address={investorAddress}&'
                              f'page={pages}&'
                              f'offset={offset}&'
                              f'startblock={startBlock}&'
                              f'endblock={curBlock}&'
                              'sort=asc&'
                              f'apikey={ets_key}',
                              timeout=60)
    except:
        print(
            f'Get TXs fail of {investorAddress} with time out')

        return {'status': '-1'}
    # print(newTXs.json())
    if newTXs.json().get('status', -1) == '1' or newTXs.status_code == 200:
        newTXs = newTXs.json()
        newTXs['investorAddress'] = investorAddress

    else:
        print(
            f'Get TXs fail of {investorAddress} with status code {newTXs.status_code}')
        return {'status': '-1'}

    # print(f'Crawling new TXs of {investorAddress} successfully')
    return newTXs


def resetInvestorTXs():

    investorDocs.update_many(
        {},
        {'$set': {'TXs': []}}
    )


def setLatestBlockNumber(blockNum=13919833):

    investorDocs.update_many(
        {},
        {'$set': {'latestBlockNumber': blockNum}}
    )


def isFuturesWork():

    for investorDoc in investorDocs.find({'TXs.0': {'$exists': True}}):

        investorAddress = investorDoc['_id'].lower()
        firstTX = investorDoc['TXs'][0]

        FromAddress = firstTX['from'].lower()
        ToAddress = firstTX['to'].lower()

        if (investorAddress not in FromAddress) and (investorAddress not in ToAddress):
            print('Future not working in TXs')
            return


def updateInvestorTXs2(maxWorkers=5):

    infura_key = infura_keys[0]
    curBlock = getCurBlock(infura_key)

    investorAddresses = []
    latestBlocks = []

    for investorDoc in investorDocs.find({}, {'latestBlockNumber': 1}):
        investorAddresses.append(investorDoc['_id'])
        latestBlocks.append(investorDoc['latestBlockNumber'])
    # investorAddresses = investorAddresses[:1]
    # latestBlocks = latestBlocks[:1]
    print(f'1/ Process transaction of {len(investorAddresses)} investor')
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
            results = [executor.submit(getInvestorTXs, latestBlock, curBlock, ets_key, investorAddress)
                       for latestBlock, ets_key, investorAddress in zip(latestBlocks, ets_keys, investorAddresses)]

            print('start waiting')
            futureWaited = concurrent.futures.wait(
                results, return_when=concurrent.futures.FIRST_COMPLETED)

            while futureWaited.not_done.__len__() != 0:
                print(f'Have {futureWaited.not_done.__len__()} left')

                time.sleep(2)
                futureWaited = concurrent.futures.wait(
                    results, return_when=concurrent.futures.FIRST_COMPLETED)
    except:
        print("Error in multi thread crawling TXs of Investors")
        return False

    newLatestBlock = curBlock

    print(f'2/ Update transaction of {len(investorAddresses)} investor')

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
    for response in concurrent.futures.as_completed(results):

        try:
            if response.result().get('status', '-1') == '-1':
                return False

            if response.result().get('status') == '0':
                if response.result().get('message', 'NOTOK') == 'NOTOK':
                    return False
                continue

            if response.result().get('result', []) == []:
                continue
        except:
            print(f'Some field gone wrong in below:')
            print(response.result())

        try:
            investorAddress = response.result()['investorAddress']
            TXsResult = response.result()['result']
            executor.submit(
                investorDocs.update_one,
                {'_id': investorAddress},
                {
                    '$push': {
                        'TXs': {
                            '$each': TXsResult
                        }
                    },
                    '$set': {
                        'latestBlockNumber': newLatestBlock
                    }
                }

            )

        except:
            print(f'Update TXs fail in {investorAddress}')
            print(response.result())
            return False

    executor.shutdown()
    print(f'Process success transaction of {len(investorAddresses)} investor')
    return True


if __name__ == '__main__':

    # print(getTransactionInput("0x109d85c1ef5204aa0e389ac8306f9761e5e7ca10022db9bb499a5a9a2be7676a", mainnet=True))
    pass