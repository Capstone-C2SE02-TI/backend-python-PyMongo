
# from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

arr = [2,1,3]

# arr.sort()

# print(arr)
def ti(b, c = 0, d = 0):
    print(b,c,d)

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    fs = [executor.submit(ti,ar,c=3) for ar in arr]

    a = concurrent.futures.wait(fs,return_when="ALL_COMPLETED")

print(a.not_done.__len__()) 
    
