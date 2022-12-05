import subprocess
import os
import concurrent.futures
import time

# coingecko = ["coinInfo.py", "coinPrice.py"]
coingecko = ["coinInfo.py"]
alchemy = ["investorCoinBalance.py"]
etherscan = ["investorTXs.py"]
normal = ["investorTotalAsset.py"]

zipAll = ["coinInfo.py", "investorCoinBalance.py", "investorTXs.py", "investorTotalAsset.py"]

from mongoDB_init import client

coinDocs = client['coins']

beforeLen = 0
AfterLen = 0
for x in coinDocs.find({'_id' : 'bitcoin'}, {'prices.minutely'}):

    beforeLen = x['prices']['minutely'].__len__()
fileName = os.path.basename(__file__)
start = time.time()
subprocess.run(['py', 'coinPrice.py'])
with concurrent.futures.ThreadPoolExecutor() as executor:
    for pyFile in zipAll:
        executor.submit(subprocess.run, ['py',pyFile])
end = time.time()
print(int(end - start), f'sec to process {fileName}')

for x in coinDocs.find({'_id' : 'bitcoin'}, {'prices.minutely'}):

    AfterLen = x['prices']['minutely'].__len__()

print('len change:',beforeLen,'->',AfterLen)
