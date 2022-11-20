
# from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

def ti(a,b = 0,c = 0,d = 0):
    print(a,b,c,d)

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    executor.submit(ti,3,c=3)
    
