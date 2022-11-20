from cmath import exp
import requests
import time
from mongoDB_init import client
from dotenv import load_dotenv
load_dotenv()
import os
import json
import concurrent.futures
import asyncio

investorDocs = client['investors']
metadataDocs = client['metadatas']
tokenDocs    = client['tokens']

ets_keys = os.environ['ets_keys']
ets_keys = [key.strip() for key in ets_keys.split(',')]

alchemy_keys = os.environ['alchemy_keys']
alchemy_keys = [key.strip() for key in alchemy_keys.split(',')]
alchemy_keys = alchemy_keys * 10000

# TODO Change the name later, it not dict
def getERC20AddressIn(contractAddresses):

    erc20Address = None

    for contractAddressPlatform in contractAddresses:
        
        if 'ETH' == contractAddressPlatform['platform']['coin']['symbol']:
            erc20Address = contractAddressPlatform['contract_address']

            break
            
            
    if erc20Address is None:
        raise Exception('Null erc20 address')

    return erc20Address 

def crawlSharkWaller(pages):

    # Using slug to get the url
    # sharkUrlPage = sharkUrl + str(pages)

    # html = requests.get(sharkUrlPage)
    # soup = BeautifulSoup(html.text,'html.parser')

    # table = soup.select_one('table.table')

    print(3)

def getWalletsETHBalance(wallets, ets_key):

    wallets = ','.join(wallets)
    balancesResult = requests.get(f'https://api.etherscan.io/api'
                            '?module=account'
                            '&action=balancemulti'
                            f'&address={wallets}'
                            '&tag=latest'
                            f'&apikey={ets_key}'
    )

    balancesResult = balancesResult.json()
    balancesResult = balancesResult['result']
    return balancesResult




def updateWalletETHBalances(wallets, runTimes):

    ETHBalancesResult = getWalletsETHBalance(wallets, ets_keys[runTimes % len(ets_keys)])

    for balanceResult in ETHBalancesResult:

        address = balanceResult['account']
        balance = balanceResult['balance']

        investorDocs.update_one(
            {'_id' : address},
            {'$set' : { 'coins' : {'ETH' : int(balance[:-18])}}}
        )

def convertDecimal(value, decimalFrom, decimalTo = 0):

   return float(value) / 10**(decimalFrom - decimalTo)


def getInvestorsERC20Balance(investorAddress, contractAddresses,alchemy_key):


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
 a
    # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor2:

    #     try:
    #         f = executor2.submit(requests.post,url = f'https://eth-mainnet.alchemyapi.io/v2/{alchemy_key}',timeout = 5, json=payload, headers=headers)
    #         # response = requests.post(f'https://eth-mainnet.alchemyapi.io/v2/{alchemy_key}',timeout = 5, json=payload, headers=headers)
    #         response = f.result()
    #     except:
    #         print(f'get {investorAddress} balance run out of time')
    #         return 0

    try:
        response = requests.post(f'https://eth-mainnet.alchemyapi.io/v2/{alchemy_key}',timeout = 5, json=payload, headers=headers)
    except:
        print(f'get {investorAddress} balance run out of time')
        return 0
    
    try:
        balancesResult = response.json()['result']
        # balancesResult = response.json()['result']
        # balancesResult = response.json()['result']['address']
        # balancesResult = response.json()
    except:
        print(f'get balance of {investorAddress} get error in return api')


    return balancesResult

async def test1(investorAddresses,alchemy_keys,contractAddressesChunk):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        multiBalanceResults = [executor.submit(getInvestorsERC20Balance,investorAddress,contractAddressesChunk,alchemy_key)
            for investorAddress,alchemy_key in zip(investorAddresses,alchemy_keys)]
        await asyncio.sleep(10)
    
    return multiBalanceResults

async def updateInvestorERC20Balances(test):

    contractAddresses,symbols,decimals = [],[],[]
    for tokenDoc in tokenDocs.find():
        contractAddresses.append(tokenDoc['_id'])
        symbols.append(tokenDoc['symbol'])
        decimals.append(tokenDoc['decimal'])

    chunkSize = 100
    contractAddresses = [contractAddresses[i:i + chunkSize] for i in range(0, len(contractAddresses), chunkSize)]
    symbols = [symbols[i:i + chunkSize] for i in range(0, len(symbols), chunkSize)]
    decimals = [decimals[i:i + chunkSize] for i in range(0, len(decimals), chunkSize)]

    
    
    count = 0
    updateCount = 0
    
    investorAddresses = [investorDoc['_id'] for investorDoc in investorDocs.find({},{'TXs' : 0})]
    # investorAddresses = investorAddresses[:15]
    investorAddresses.sort()

    for symbolsChunk,contractAddressesChunk,decimalChunk in zip(symbols,contractAddresses,decimals):

        
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            multiBalanceResults = [executor.submit(getInvestorsERC20Balance,investorAddress,contractAddressesChunk,alchemy_key)
                for investorAddress,alchemy_key in zip(investorAddresses,alchemy_keys)]
        # balancesResult = getInvestorsERC20Balance(investorAddress,contractAddressesChunk,alchemy_key)
        multiBalanceResults = [balanceResults.result() for balanceResults in concurrent.futures.as_completed(multiBalanceResults)]
        coinBalances = {}

        multiBalanceResults.sort(key = lambda x : x['address'].lower())
        notOke = 0
        oke = 0
        isLastOke = False
        print(len(investorAddresses) == len(multiBalanceResults),len(investorAddresses),len(multiBalanceResults))
        for investorAddress,balanceResults in zip(investorAddresses,multiBalanceResults):
            try:
                if investorAddress.lower() != balanceResults['address'].lower():
                    # print(investorAddress.lower(),balanceResults['address'].lower())
                    notOke += 1

                    if isLastOke:
                        print( oke,'Oke')
                        isLastOke = False
                    continue
                else:
                    if not isLastOke:
                        print( notOke,'Not Oke')
                        isLastOke = True
                    oke += 1
            except:
                print(balanceResults)
                break
        
        print(float(notOke) / len(investorAddresses))

            
        # TODO Get symbol to update
            # for symbol,contractAddressReq, balanceResult,decimal in zip(symbolsChunk,contractAddressesChunk,balanceResults.result()['tokenBalances'],decimalChunk):
            #     contractAddressRes, hexBalance = balanceResult.values()
            #     # TODO Get token decimal()
            #     standardDecimalBalance = convertDecimal(int(hexBalance,16),decimal)

            #     if standardDecimalBalance == 0.0:
            #         continue
                
            #     print(symbol,contractAddressReq,decimal,standardDecimalBalance)

            #     investorDocs.update_one(
            #         {'_id' : investorAddress},
            #         {'$set' : {f'coins.{symbol}' : standardDecimalBalance}}

            #     )

            #     coinBalances[f'coins.{symbol}'] = standardDecimalBalance
            
            # updateCount += 1

            # investorDocs.update_one(
            #         {'_id' : investorAddress},
            #         {'$set' : coinBalances}
            # )    

            # print(f'Update No.{updateCount} success.',investorAddress)

                
                
        

            
loop = asyncio.get_event_loop()
loop.run_until_complete(updateInvestorERC20Balances(3))



        




