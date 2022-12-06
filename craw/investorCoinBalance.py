import asyncio
import concurrent.futures
import json
import os
from cmath import exp
import requests
import time
from mongoDB_init import client
from dotenv import load_dotenv
load_dotenv()

investorDocs = client['investors']
coinTestDocs = client['coins']

ets_keys = os.environ['ets_keys']
ets_keys = [key.strip() for key in ets_keys.split(',')]
ets_keys = ets_keys * 1000

alchemy_keys = os.environ['alchemy_keys']
alchemy_keys = [key.strip() for key in alchemy_keys.split(',')]
alchemy_keys = alchemy_keys * 10000


def test():

    for invest in investorDocs.find({},{'_id' : 1}):
        print(invest['_id'])
        break
def getWalletsETHBalance(wallets, ets_key):

    wallets = ','.join(wallets)

    balancesResult = {}
    try: 
        balancesResult = requests.get(f'https://api.etherscan.io/api'
                                        '?module=account'
                                        '&action=balancemulti'
                                        f'&address={wallets}'
                                        '&tag=latest'
                                        f'&apikey={ets_key}',
                                        timeout=60
                                        )
        

        balancesResult = balancesResult.json()
    except:
        print(balancesResult)
        return {'status' : -1}

    balancesResult['status'] = 1
    return balancesResult


def updateInvestorETHBalances(maxWorkers = 10):
    chunkSize = 20

    investorAddresses = [investorDoc['_id']
                         for investorDoc in investorDocs.find({}, {'_id': 1})]
    investorAddresses = [investorAddresses[i:i + chunkSize]
                         for i in range(0, len(investorAddresses), chunkSize)]
                    
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        multiETHBalanceResults = [
            executor.submit(
                getWalletsETHBalance, 
                investorAddress,
                ets_key
            )
            for investorAddress, ets_key in zip(investorAddresses, ets_keys)
        ]

    
    multiETHBalanceResults = [ethBalanceResults.result() 
                               for ethBalanceResults in concurrent.futures.as_completed(multiETHBalanceResults)]

    fractionDigits = 5
    countTest = 0
    for ETHBalanceResults in multiETHBalanceResults:
        countTest += 1

        if ETHBalanceResults.get('status', -1) == -1:
            print(ETHBalanceResult)
            print('Status is -1')
            return False
        for ETHBalanceResult in ETHBalanceResults['result']:

            if isinstance(ETHBalanceResult, str):
                print(ETHBalanceResults)
                return False

            
            investorAddress = ETHBalanceResult['account']

            if len(ETHBalanceResult['balance']) <= 13:
                continue
            
            ETHBalance = float(ETHBalanceResult['balance'][:-13])/(10**fractionDigits)
            # investorDocs.update_one(
            #     {'_id' : investorAddress},
            #     {'$set' : {'coins.eth' : ETHBalance} }
            # )    
    return True


def convertDecimal(value, decimalFrom, decimalTo=0):

    return float(value) / 10**(decimalFrom - decimalTo)


def getInvestorsERC20Balance(investorAddress, contractAddresses, alchemy_key):

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    payload = {
        "id": '1',
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenBalances",
        'params': [investorAddress, contractAddresses]
    }

    try:
        response = requests.post(
            f'https://eth-mainnet.alchemyapi.io/v2/{alchemy_key}', json=payload, headers=headers, timeout=60)
    except:
        print(f'get {investorAddress} balance run out of time')
        return {'status' : 0}
        
    balancesResult = {}

    try:
        balancesResult = response.json()['result']
    except:
        print(f'get ERC20 balance of {investorAddress} error, Status code:{response.status_code}')
        
    balancesResult['status'] = 1
    return balancesResult


def updateInvestorERC20Balances(maxWorkers = 50):

    contractAddresses, symbols, decimals = [], [], []
    filter = {'asset_platform_id' : {'$ne' : None}}
    projection = {'symbol' : 1, 'detail_platforms' : 1}
    for coinDoc in coinTestDocs.find(filter, projection):
        symbols.append(coinDoc['symbol'])

        contractAddresses.append(coinDoc['detail_platforms']['ethereum']['contract_address'])
        decimals.append(coinDoc['detail_platforms']['ethereum']['decimal_place'])
    
    
    chunkSize = 100
    contractAddresses = [contractAddresses[i:i + chunkSize]
                         for i in range(0, len(contractAddresses), chunkSize)]
    symbols = [symbols[i:i + chunkSize]
               for i in range(0, len(symbols), chunkSize)]
    decimals = [decimals[i:i + chunkSize]
                for i in range(0, len(decimals), chunkSize)]

    updateCount = 0

    investorAddresses = [investorDoc['_id']
                         for investorDoc in investorDocs.find({}, {'_id': 1})]
    
    # investorAddresses = investorAddresses[:15]
    investorAddresses.sort(key=str.lower)

    balanceUpdated = {}
    for symbolsChunk, contractAddressesChunk, decimalChunk in zip(symbols, contractAddresses, decimals):
        with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
            multiBalanceResults = [
                executor.submit(
                    getInvestorsERC20Balance, 
                    investorAddress,
                    contractAddressesChunk, 
                    alchemy_key)
                for investorAddress, alchemy_key in zip(investorAddresses, alchemy_keys)
            ]

        waiTest = concurrent.futures.wait(
            multiBalanceResults, return_when="ALL_COMPLETED")

        if waiTest.not_done.__len__() != 0:
            print("All the futures not done yet!")
            return False
        
        print('All futures all done')

        multiBalanceResults = [balanceResults.result() 
                               for balanceResults in concurrent.futures.as_completed(multiBalanceResults)]
        

        multiBalanceResults.sort(key=lambda x: x.get('address','0').lower())
     
        print(len(investorAddresses) == len(multiBalanceResults),
              len(investorAddresses), len(multiBalanceResults))
        
        
        for investorAddress, balanceResults in zip(investorAddresses, multiBalanceResults):
            if investorAddress.lower() != balanceResults.get('address','0').lower():
                print('different Address between input and output')
                return False            

            if balanceResults.get('status',0) == 0:
                print(balanceResults)
                print('Nah, error so I gotta our of here')
                return False

            coinBalances = {}
            
            for symbol, contractAddressReq, balanceResult, decimal in zip(symbolsChunk, contractAddressesChunk, balanceResults['tokenBalances'], decimalChunk):
                contractAddressRes, hexBalance = balanceResult.values()

                standardDecimalBalance = convertDecimal(
                    int(hexBalance, 16), decimal)

                if standardDecimalBalance == 0.0 or standardDecimalBalance == 0:
                    continue

                coinBalances[f'coins.{symbol}'] = standardDecimalBalance
            
            if coinBalances.__len__() == 0:
                continue
            
            updateCount += 1


           
            
            # if investorAddress not in balanceUpdated:
            #     investorDocs.update_one(
            #         {'_id': investorAddress},
            #         [{'$set': {'coins' : {'$literal': {}}}},{'$set': coinBalances}]
            #     )

            #     balanceUpdated[investorAddress] = True
            # else:
            #     investorDocs.update_one(
            #         {'_id': investorAddress},
            #         {'$set': coinBalances}
            #     )

            # print(f'Update No.{updateCount} success.', investorAddress)
    return True




