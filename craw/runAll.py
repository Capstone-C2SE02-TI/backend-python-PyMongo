import subprocess
import os
import concurrent.futures
import time

from coinInfo import coinDataHandler
from coinPrice import coinPriceMinutelyHandler, coinPriceHandler
from coinSumInvestment import UpdateCoinSumInvest
from investorCoinBalance import updateInvestorERC20Balances,updateInvestorETHBalances
from investorTotalAsset import investorTotalAssetSnapshot
from investorTXs import updateInvestorTXs2

# coingecko = [coinDataHandler, coinPriceMinutelyHandler]
coingecko = [coinPriceMinutelyHandler]
alchemy = [updateInvestorERC20Balances]
etherscan = [updateInvestorTXs2, updateInvestorETHBalances]
normal = [investorTotalAssetSnapshot, UpdateCoinSumInvest]

zipAll = coingecko + alchemy + etherscan + normal

fileName = os.path.basename(__file__)
start = time.time()
coinDataHandler()

with concurrent.futures.ThreadPoolExecutor() as executor:
    for pyFile in zipAll:
        executor.submit(pyFile)
end = time.time()
print(int(end - start), f'sec to process {fileName}')
