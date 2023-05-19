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
ets_keys = ["DQTBUEXC9H7KMDDS87SIHCPRWZVGJCGFD5"]
ets_keys = ets_keys*10000
infura_keys = os.environ['infura_keys']
infura_keys = [i.strip() for i in infura_keys.split(',')]

routers = ['0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D','0xEfF92A263d31888d860bD50809A8D171709b7b1c','0xf164fC0Ec4E93095b804a4795bBe1e041497b92a','0x13f4EA83D0bd40E75C8222255bc855a974568Dd4']
rOldLen = len(routers)
for i in range(rOldLen):
    routers.append(routers[i].lower())
print(routers)

def getCurBlock(infura_key):

    w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))
    curBlock = w3.eth.get_block_number()

    return curBlock


def getInvestorTXs(startBlock, curBlock, ets_key, investorAddress):

    pages = 1
    offset = 10000
    try:
        newTXs = requests.get('https://api-testnet.bscscan.com/api?module=account&'
                              'action=tokentx&'
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
    # Cycle is revert to old tx
    # Find all pair in uni,pancake
    # All pair in testnet
    # API to show that pair
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

    curBlock = 29734921

    investorAddresses = ["0x72598E10eF4c7C0E651f1eA3CEEe74FCf0A76CF2"]
    latestBlocks = ["0"]

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
            print(investorAddress)
            print(TXsResult)
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

    # resetInvestorTXs()
    # setLatestBlockNumber()
    updateInvestorTXs2()