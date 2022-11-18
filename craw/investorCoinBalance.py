from cmath import exp
import requests
import time
from mongoDB_init import client
from dotenv import load_dotenv
load_dotenv()
import os
import json
import concurrent.futures


investorDocs = client['investors']
metadataDocs = client['metadatas']
tokenDocs    = client['tokens']

ets_keys = os.environ['ets_keys']
ets_keys = [key.strip() for key in ets_keys.split(',')]

alchemy_keys = os.environ['alchemy_keys']
alchemy_keys = [key.strip() for key in alchemy_keys.split(',')]
alchemy_keys = alchemy_keys*10000

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

# def getInvestorsERC20Balance(investorAddress, ERC20address, ets_key):

#     time.sleep(0.5)

#     try:
#         balancesResult = requests.get(f'https://api.etherscan.io/api'
#                                 '?module=account'
#                                 '&action=tokenbalance'
#                                 f'&contractaddress={ERC20address}'
#                                 f'&address={investorAddress}'
#                                 '&tag=latest'
#                                 f'&apikey={ets_key}',
#                                 timeout = 5
#         )
#     except:
#         print(f'get {ERC20address} balance of {investorAddress} run out of time')
#         return 0

#     try:
#         balancesResult = balancesResult.json()
#         balancesResult = balancesResult['result']
#     except:
#         print(f'get {ERC20address} balance of {investorAddress} get error in return api')
#         print(balancesResult)

#     return balancesResult

# def updateInvestorERC20Balances():

#     count = 0

#     for investorDoc in investorDocs.find():
#         investorAddress = investorDoc['_id']

#         print(f'Processing {investorAddress}')
      
#         for metadataDoc in metadataDocs.find({'category' : 'token'}):


#             erc20Symbol = metadataDoc['symbol']
#             print(f'Processing {investorAddress}: getting {erc20Symbol} balance')

#             count += 1

#             # Replace key for better performance
#             ets_key = ets_keys[count % len(ets_keys)]

#             contractAddresses = metadataDoc['contract_address']
#             erc20Address = getERC20AddressIn(contractAddresses)

#             ERC20Balance = getInvestorsERC20Balance(investorAddress, erc20Address, ets_key)

#             if ERC20Balance == '0':
#                 print(f'{erc20Symbol} balance of {investorAddress} : 0')

#                 continue

         
#             erc20Decimal = metadataDoc['decimal']
#             standardERC20Balance = convertDecimal(ERC20Balance,erc20Decimal)

#             try:
#                 investorDocs.update_one(
#                     {'_id' : investorAddress},
#                     {'$set' : {f'coins.{erc20Symbol}' : float(standardERC20Balance)}}
#                 )
#             except:
#                 print(f'{investorAddress} got {erc20Symbol}:{contractAddresses} balance error in {ERC20Balance} ')

            
#             print(f'update {erc20Symbol} balance of {investorAddress} : {standardERC20Balance}')

stt = 0
def getInvestorsERC20Balance(investorAddress, contractAddresses,alchemy_key):
    global stt
    stt += 1
    # print(stt,investorAddress)
    time.sleep(0.5)

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
        response = requests.post(f'https://eth-mainnet.alchemyapi.io/v2/{alchemy_key}',timeout = 5, json=payload, headers=headers)
    except:
        print(f'get {investorAddress} balance run out of time')
        return 0
    
    try:
        balancesResult = response.json()['result']['tokenBalances']
    except:
        print(f'get balance of {investorAddress} get error in return api')


    return balancesResult

def updateInvestorERC20Balances(test):
    t1 = time.perf_counter()

    contractAddresses,symbols,decimals = [],[],[]
    for tokenDoc in tokenDocs.find():
        contractAddresses.append(tokenDoc['_id'])
        symbols.append(tokenDoc['symbol'])
        decimals.append(tokenDoc['decimal'])

    contractAddresses = [contractAddresses[i:i + 100] for i in range(0, len(contractAddresses), 100)]
    symbols = [symbols[i:i + 100] for i in range(0, len(symbols), 100)]
    decimals = [decimals[i:i + 100] for i in range(0, len(decimals), 100)]

    

    count = 0
    updateCount = 0
    investorAddresses = [investorDoc['_id'] for investorDoc in investorDocs.find({},{'TXs' : 0})]

    for symbolsChunk,contractAddressesChunk,decimalChunk in zip(symbols,contractAddresses,decimals):
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            MultiBalanceResults = [executor.submit(getInvestorsERC20Balance,investorAddress,contractAddressesChunk,alchemy_key) 
                    for investorAddress,alchemy_key in zip(investorAddresses,alchemy_keys)]

        # balanceResults = getInvestorsERC20Balance(investorAddress,contractAddressesChunk,alchemy_key)
        
        
        # TODO Get symbol to update

        for investorAddress,balanceResults in zip(investorAddresses,concurrent.futures.as_completed(MultiBalanceResults)):

            coinBalances = {}
            for symbol,contractAddressReq, balanceResult,decimal in zip(symbolsChunk,contractAddressesChunk,balanceResults.result(),decimalChunk):
                contractAddressRes, hexBalance = balanceResult.values()
                # TODO Get token decimal()
                standardDecimalBalance = convertDecimal(int(hexBalance,16),decimal)

                if standardDecimalBalance == 0.0 or standardDecimalBalance == 0:
                    continue
                
                if investorAddress == '0xb29380ffc20696729b7ab8d093fa1e2ec14dfe2b':
                    print("Balance",symbol,contractAddressReq,decimal,standardDecimalBalance)

                # investorDocs.update_one(
                #     {'_id' : investorAddress},
                #     {'$set' : {f'coins.{symbol}' : standardDecimalBalance}}

                # )

                coinBalances[f'coins.{symbol}'] = standardDecimalBalance

            investorDocs.update_one(
                    {'_id' : investorAddress},
                    {'$set' : coinBalances}

            )
            updateCount += 1
            # print("update Statement",updateCount,investorAddress)
            
        
            # NOTE For validate contract order and symbol order
            # if contractAddressReq != contractAddressRes or symbol != symbolTest:
            #     print('error')
    t2 = time.perf_counter()

    print(f'Finished in {t2-t1} seconds')

            




        


updateInvestorERC20Balances(3)



