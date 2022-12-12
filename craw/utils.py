import time
from mongoDB_init import crawlClient
import json


def logExecutionTime(function):
    functionName = function.__name__

    start = time.time()
    function()
    end = time.time()

    executionDuration = int(end-start)
    print(f'{functionName} take {executionDuration}s')


def isExistedCoinSymbol(symbol):
    file = open('./utils/coinSymbols.json')
    coinSymbols = json.load(file)

    return symbol in coinSymbols

def refreshCoinSymbol():

    coinDocs = crawlClient['coins']
    coinSymbols = [coinDoc['symbol']
                   for coinDoc in coinDocs.find({}, {'symbol': 1})]

    json_object = json.dumps(coinSymbols, indent=4)

    with open('./utils/coinSymbols.json', 'w') as outfile:
        outfile.write(json_object)

def isExistedAddress(address):
    file = open('./utils/investorAddresses.json')
    investorAddresses = json.load(file)

    return address.lower() in investorAddresses

def refreshInvestorAddresses():

    investorDocs = crawlClient['investors']
    investorAddresses = [investorDoc['_id'].lower()
                         for investorDoc in investorDocs.find({}, {'_id': 1})]

    json_object = json.dumps(investorAddresses, indent=4)

    with open('./utils/investorAddresses.json', 'w') as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    refreshInvestorAddresses()
