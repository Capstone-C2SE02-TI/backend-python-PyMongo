from web3 import Web3
from dotenv import load_dotenv
import os
import time

load_dotenv()
infura_keys = os.environ['infura_key'] 
infura_keys = [i.strip() for i in infura_keys.split(',')]


def getCurBlock(runTimes, seed):

    w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_keys[runTimes % len(infura_keys)]}'))
    curBlock = w3.eth.get_block_number()
    
    return curBlock


print(getCurBlock(5,2))

time.sleep(10)

print(getCurBlock(6,2))


