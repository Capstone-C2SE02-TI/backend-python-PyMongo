import matplotlib.pyplot as plt
import json
from statistics import mean

f = open('./max-worker-statistic.json')
data = json.load(f)
f.close()

def sortJson():

    f = open('./max-worker-statistic.json')
    data = json.load(f)
    f.close()

    newData = {}

    for name in data:
        newData[name] = {}

        intKeyList = list(map(int, data[name].keys()))
        for maxWorkers in sorted(intKeyList, reverse=False):

            if maxWorkers & 1:
                continue
            times = data[name][f'{maxWorkers}']

            times = [time if time >= 0 else 600 for time in times]

            newData[name][f'{maxWorkers}'] = times

    json_object = json.dumps(newData, indent=4)

    with open("./max-worker-statistic.json", "w") as outfile:
        outfile.write(json_object)

sortJson()
for fileName in data:
    
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    xs = []
    ys = []

    xMin = 999
    yMin = 999
    for maxWorkers,times in data[fileName].items():
        xs.append(int(maxWorkers))

        meanTimes = mean(times)
        ys.append(meanTimes)

        if yMin > meanTimes:
            yMin = meanTimes
            xMin = int(maxWorkers)


    print(f'Min time to crawl {fileName} is {yMin}, at Max Workers = {xMin}')


    ax1.plot(xs, ys)
    ax1.plot(xMin,yMin,'r*')
    plt.title(f'Time to crawl {fileName}')
    plt.legend(['time'])
    plt.xlabel('Max workers')
    plt.savefig(fileName)
    plt.show()
    