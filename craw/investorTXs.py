import concurrent.futures
from utils import logExecutionTime
from mongoDB_init import crawlClient
from web3 import Web3
import requests
from dotenv import load_dotenv
import os
import time
load_dotenv()

investorDocs = crawlClient['investors']

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
    try:
        newTXs = requests.get('https://api.etherscan.io/api?module=account&action=tokentx&'
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
    function = updateInvestorTXs2
    logExecutionTime(function)
