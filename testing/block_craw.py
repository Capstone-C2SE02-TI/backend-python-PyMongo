from web3 import Web3
from dotenv import load_dotenv
import os
load_dotenv()

infura_key = os.environ['infura_key']
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))

latestBlock = w3.eth.get_block(15488117,True)


# https://stackoverflow.com/questions/69544988/how-to-filter-eth-transactions-by-address-with-web3-py

# https://etherscan.io/tx/0xd101056aa43708c3390130468aa69bc4cf9465461821bb7b6ff54ae513e87244
# block 15488117 

# from 0x82a4cf34187e9196e57b7517b961a06416c3263d
# contract interact to 0xdac17f958d2ee523a2206206994597c13d831ec7
# to 0xb3a55de0aec1b91552a97a4e8f35e7247a5cf935
# 784 usdt

# Function: transfer(address _to, uint256 _value)
# input 0xa9059cbb                                                  len 10 tx['input'].upper()[:10]
# 000000000000000000000000b3a55de0aec1b91552a97a4e8f35e7247a5cf935  len 64 tx['input'].upper()[10:74]
# 000000000000000000000000000000000000000000000000000000002ec25320  len 64 tx['input'].upper()[74:]
# Combine 3 things above to go input

w3.fromWei

txFrom = '0x82a4cf34187e9196e57b7517b961a06416c3263d'.upper()
txTo = '0xb3a55de0aec1b91552a97a4e8f35e7247a5cf935'.upper()
for tx in latestBlock['transactions']:

    try:
        if tx['from'].upper() == txFrom and txTo[2:] in tx['input'].upper():
            for atb in tx:
                print(atb,' : ', tx[atb])

            print('methodId',tx['input'].upper()[:10])
            print('to',tx['input'].upper()[10:74])
            print('usdtvalue',w3.toInt(hexstr = tx['input'].upper()[74:]))
    except:
        print('Sth wrong, continue')

        continue