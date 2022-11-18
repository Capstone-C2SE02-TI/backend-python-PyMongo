from cmath import exp
import requests
import time
from mongoDB_init import client
from dotenv import load_dotenv
load_dotenv()
import os
import json

sharkDocs = client['shark']
sharkAddresses = [shark['_id'] for shark in sharkDocs.find()]
metadataDocs = client['metadata']

ets_keys = os.environ['ets_keys']
ets_keys = [key.strip() for key in ets_keys.split(',')]

# TODO Change the name later, it not dict
def crawlERC20Addresses():

    erc20Addresses = {}
    for metadataDoc in metadataDocs.find({'category' : 'token'}):
      
        for contractAddresses in metadataDoc['contract_address']:
            
            if 'ETH' == contractAddresses['platform']['coin']['symbol']:
                erc20Address = contractAddresses['contract_address']
                erc20Symbol = metadataDoc['symbol']

                erc20Addresses[erc20Symbol] = erc20Address

    return erc20Addresses

def crawlSharkWaller(pages):

    # Using slug to get the url
    # sharkUrlPage = sharkUrl + str(pages)

    # html = requests.get(sharkUrlPage)
    # soup = BeautifulSoup(html.text,'html.parser')

    # table = soup.select_one('table.table')

    print(3)

def crawlWalletsETHBalance(wallets, ets_key):

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

    ETHBalancesResult = crawlWalletsETHBalance(wallets, ets_keys[runTimes % len(ets_keys)])

    for balanceResult in ETHBalancesResult:

        address = balanceResult['account']
        balance = balanceResult['balance']

        sharkDocs.update_one(
            {'_id' : address},
            {'$set' : { 'coins' : {'ETH' : int(balance[:-18])}}}
        )

def crawlWalletsERC20Balance(wallet, ERC20address,ets_key):

    balancesResult = requests.get(f'https://api.etherscan.io/api'
                            '?module=account'
                            '&action=tokenbalance'
                            f'&contractaddress={ERC20address}'
                            f'&address={wallet}'
                            '&tag=latest'
                            f'&apikey={ets_key}'
    )

    balancesResult = balancesResult.json()
    balancesResult = balancesResult['result']
    return balancesResult
    
def updateWalletERC20Balances(wallets, ERC20_SymbolToAddress):

    
    count = 0

    for wallet in wallets:
        
        for symbol,address in ERC20_SymbolToAddress.items():
            count += 1

            # Replace key for better performance
            ets_key = ets_keys[count % len(ets_keys)]

            erc20Balance18Decimal = crawlWalletsERC20Balance(wallet, address, ets_key)

            if erc20Balance18Decimal == '0':
                continue

            # TODO Not all coin Decimal is 18 => find sw to get Decimal number of it
            erc20Balance = erc20Balance18Decimal[:-18]

            try:
                sharkDocs.update_one(
                    {'_id' : wallet},
                    {'$set' : {f'coins.{symbol}' : int(erc20Balance)}}
                )
            except:
                print(f'{wallet} got {symbol}:{address} balance error in {erc20Balance18Decimal} ')

            
            # print(f'update {symbol} balance of {wallet} : {erc20Balance}')

        


updateWalletERC20Balances(sharkAddresses, crawlERC20Addresses())



