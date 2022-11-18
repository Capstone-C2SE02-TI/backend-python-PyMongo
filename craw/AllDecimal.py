from urllib import request
from web3 import Web3
from dotenv import load_dotenv
import os
from mongoDB_init import client
import requests
load_dotenv()

metadataDocs = client['metadatas']
tokenDocs = client['tokens']

infura_keys = os.environ['infura_keys']
infura_keys = [infura_key.strip() for infura_key in infura_keys.split(',')]

ets_keys = os.environ['ets_keys']
ets_keys = [infura_key.strip() for infura_key in ets_keys.split(',')]


def getCoinDecimal(infura_key, ets_key, contractAddress):

   w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))

   # data = requests.get('https://api.etherscan.io/api'
   #                   '?module=contract'
   #                   '&action=getabi'
   #                   f'&address={contractAddress}'
   #                   f'&apikey={ets_key}'
   #    )
   # data = data.json()
   abi = [{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]
   contractAddress = Web3.toChecksumAddress(contractAddress)
   deployed_contract = w3.eth.contract(contractAddress, abi=abi)

   decimal = 18

   try:
      decimal = deployed_contract.functions.decimals().call()
   except:
      print(f'{contractAddress} dont have decimals function')

   return decimal

def updateCoinDecimal(runTimes):

   infura_key = infura_keys[runTimes % len(infura_keys)]
   ets_key = ets_keys[runTimes % len(ets_keys)]

   for metadataDoc in metadataDocs.find({'category' : 'token'}):
      erc20Address = ''
      erc20Symbol = ''
      for contractAddressPlatform in metadataDoc['contract_address']:
            
            if 'ETH' == contractAddressPlatform['platform']['coin']['symbol']:

               erc20Address = contractAddressPlatform['contract_address']
               erc20Symbol = metadataDoc['symbol']

            break
         
      if erc20Address == '' or erc20Symbol == '':
         metadataId = metadataDoc['_id']
         print(f'Address, symbol error in {metadataId}')
         continue

      decimal = getCoinDecimal(infura_key, ets_key, erc20Address)
      
      metadataDocs.update_one(
         {'_id' : erc20Symbol},
         { '$set' : {'decimal' : decimal}}
      )

def updateCoinDecimal(runTimes):

   infura_key = infura_keys[runTimes % len(infura_keys)]
   ets_key = ets_keys[runTimes % len(ets_keys)]

   for tokenDoc in tokenDocs.find():
      
      decimal = getCoinDecimal(infura_key, ets_key, tokenDoc['_id'])
      
      tokenDocs.update_one(
         {'_id' : tokenDoc['_id']},
         { '$set' : {'decimal' : decimal}}
      )
      

               
      

updateCoinDecimal(0)
# getCoinDecimal(infura_keys[0],ets_keys[0],'0x15D4c048F83bd7e37d49eA4C83a07267Ec4203dA')







