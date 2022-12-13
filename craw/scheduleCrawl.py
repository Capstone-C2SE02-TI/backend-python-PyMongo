import schedule
import time

from coinPrice import coinPriceHandler
from addShark import addNewAddressHandler

schedule.every().day.at("00:10").do(coinPriceHandler)
schedule.every().day.at("01:00").do(addNewAddressHandler)

while True:
    schedule.run_pending()
    time.sleep(1)