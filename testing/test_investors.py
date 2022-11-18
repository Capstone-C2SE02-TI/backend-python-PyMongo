from typing_extensions import runtime
from dotenv import load_dotenv
import os
import time

load_dotenv()

ets_keys = os.environ['ets_keys']
ets_keys = [i.strip() for i in ets_keys.split(',')]


# TODO get eth balance + eth price => $

def initInvestorCraw(timeGap, runTimes):

    while True:

        if runTimes == 1:
            break

        runTimes += 1

        time.sleep(timeGap)





# TODO Get erc20 tokens + erc20 price => $