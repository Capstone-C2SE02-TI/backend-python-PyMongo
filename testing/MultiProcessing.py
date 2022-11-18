import concurrent.futures

def test(a,b,c,d,e):
    print(a,b,c,d,e)

ass = [1,2,3,123]
bs = [4,5,6,123]
cd = [7,8,9,123]
ed = [10,11,12,13]


with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(test,ass, bs,cd,ed,[1,1,1,1])

# with concurrent.futures.ThreadPoolExecutor() as executor2:
#         executor2.map(test,ass, bs, cd,cd,[2,2,2])