import concurrent.futures
import time
def test(a,b,c,d,sec):
    print(sec)
    time.sleep(sec)
    return sec
    
sleeps = [1,4,3,2]
ass = [1,2,3,123]
bs = [4,5,6,123]
cd = [7,8,9,123]
ed = [10,11,12,13]
def test2():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(test,a,b,c,d,sec) for a,b,c,d,sec in zip(ass,bs,cd,ed,sleeps)]
    return results
if __name__ ==  '__main__':
    t1 = time.perf_counter()
    

    results = test2()
    for f in concurrent.futures.as_completed(results):
        print(f.result())

    t2 = time.perf_counter()

    print(f'Finished in {t2-t1} seconds')



# with concurrent.futures.ThreadPoolExecutor() as executor2:
#         executor2.map(test,ass, bs, cd,cd,[2,2,2])