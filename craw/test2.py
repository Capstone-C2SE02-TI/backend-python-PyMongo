from dotenv import load_dotenv
import os
import time
load_dotenv()

ets_keys = os.environ['ets_keys']
ets_keys = [i.strip() for i in ets_keys.split(',')]
ets_keys = ets_keys*10000

print(ets_keys[:10])