import time
from datetime import datetime
from mongoDB_init import crawlClient
import json

def getCurrentDateTime():
    secUnix = time.time()
    return getDateTime(secUnix)

def getDateTime(secUnix):
    return datetime.fromtimestamp(secUnix).strftime('%d-%m-%Y %H:%M:%S')

    
def logExecutionTime(function):
    functionName = function.__name__

    start = time.time()
    penaltyTime = 0
    try:
        function()
    except:
        print(f'{functionName} got error!')
        penaltyTime = 600

    end = time.time() + penaltyTime

    executionDuration = int(end-start)
    print(f'{functionName} take {executionDuration}s. With penalty Time = {penaltyTime}')

    return executionDuration


def addExecutionTime(functionName, executionTime = '3'):
    
    currentSecUnix = int(time.time())
    try:
        readFile = open(f'../execution-time-statistic/{functionName}.json','r')
        print(f'Open {readFile.name} success')
    except FileNotFoundError:
        print(f'Dont have {functionName} execution time statistic file, now create it!')
        with open(f'../execution-time-statistic/{functionName}.json','w') as initFile:
            initFile.write("{}")
        readFile = open(f'../execution-time-statistic/{functionName}.json','r')
        
    executionTimes = json.load(readFile)
    readFile.close()
    executionTimes[currentSecUnix] = executionTime

    json_object = json.dumps(executionTimes, indent=4)
    with open(f'../execution-time-statistic/{functionName}.json','w') as initFile:
        initFile.write(json_object)

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
    print(getCurrentDateTime())
