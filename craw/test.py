import subprocess
import os
import concurrent.futures

# coingecko = ["coinInfo.py", "coinPrice.py"]
coingecko = ["coinInfo.py"]
alchemy = ["investorCoinBalance.py"]
etherscan = ["investorTXs.py"]
normal = ["investorTotalAsset.py"]

zipAll = ["coinInfo.py", "investorCoinBalance.py", "investorTXs.py", "investorTotalAsset.py"]

subprocess.run(['py', 'coinPrice.py'])
with concurrent.futures.ThreadPoolExecutor() as executor:
    for pyFile in zipAll:
        executor.submit(subprocess.run, ['py',pyFile])
