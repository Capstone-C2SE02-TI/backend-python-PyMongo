import subprocess
import os
import concurrent.futures
import time

from coinInfo import coinDataHandler
from coinPrice import coinPriceMinutelyHandler
from coinSumInvestment import UpdateCoinSumInvest
from investorCoinBalance import updateInvestorERC20Balances,updateInvestorETHBalances
from investorTotalAsset import investorTotalAssetSnapshot, updateSharkStatus
from investorTXs import updateInvestorTXs2

coingecko = [coinPriceMinutelyHandler]
alchemy = [updateInvestorERC20Balances]
etherscan = [updateInvestorTXs2, updateInvestorETHBalances]
normal = [investorTotalAssetSnapshot, UpdateCoinSumInvest, updateSharkStatus]

zipAll = coingecko + alchemy + etherscan + normal

# def executorReplay(function):

#     with concurrent.futures.ThreadPoolExecutor() as executorLevel2:


fileName = os.path.basename(__file__)
start = time.time()
with concurrent.futures.ThreadPoolExecutor() as executorLevel1:
    for pyFile in zipAll:
        executorLevel1.submit(pyFile)
# coinDataHandler()

end = time.time()
print(int(end - start), f'sec to process {fileName}')
