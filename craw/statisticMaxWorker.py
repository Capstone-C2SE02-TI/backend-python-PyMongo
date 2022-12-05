from investorCoinBalance import updateInvestorERC20Balances, updateInvestorETHBalances
from investorTXs import updateInvestorTXs2
import json
import time
import concurrent.futures
from datetime import date, timedelta, datetime

keys = [
    'investorERC20Balance',
    'investorETHBalance',
    'investorTXs'
]
functions = [
    updateInvestorERC20Balances,
    updateInvestorETHBalances,
    updateInvestorTXs2
]


def sortJson():

    f = open('./max-worker-statistic.json')
    data = json.load(f)
    f.close()

    newData = {}

    for name in data:
        newData[name] = {}

        intKeyList = list(map(int, data[name].keys()))
        for maxWorkers in sorted(intKeyList):
            newData[name][f'{maxWorkers}'] = data[name][f'{maxWorkers}']

    json_object = json.dumps(newData, indent=4)

    with open("./max-worker-statistic.json", "w") as outfile:
        outfile.write(json_object)


def writeToJson(key, maxWorkers, duration):

    f = open('./max-worker-statistic.json')
    data = json.load(f)

    if str(maxWorkers) in data[key]:

        data[key][str(maxWorkers)].append(duration)
    else:
        data[key][str(maxWorkers)] = [duration]

    f.close()

    json_object = json.dumps(data, indent=4)

    with open("./max-worker-statistic.json", "w") as outfile:
        outfile.write(json_object)


def statisticMaxWorker():

    while True:
        for key, function in zip(keys, functions):

            functionName = function.__name__

            if functionName == 'updateInvestorERC20Balances':
                startRange = 100
                sleepTime = 10
            else:
                startRange = 20
                sleepTime = 60
            for maxWorkers in range(startRange, 1, -1):

                start = int(time.time())
                startConvert = datetime.fromtimestamp(start).strftime('%d-%m-%Y %H:%M:%S')
                print(f'Test Max workers = {maxWorkers} for {functionName}. Start from {startConvert}')

                isWorking = function(maxWorkers)
                end = time.time()

                if not isWorking:
                    duration = -1
                    print(f'With Max workers = {maxWorkers}, {functionName} get rate limit')
                else:
                    duration = int(end-start)
                    print(f'With Max workers = {maxWorkers}, {functionName} take {duration} secs to execution')

                writeToJson(key, maxWorkers, duration)

                print(f'Sleep for {sleepTime}')
                time.sleep(sleepTime)

                if duration >= 600:
                    break

# writeToJson('investorERC20Balance',100,27)
statisticMaxWorker()
