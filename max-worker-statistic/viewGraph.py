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
    for maxWorkers,times in data[fileName].items():
        xs.append(int(maxWorkers))
        ys.append(int(mean(times)))
        print(times, int(maxWorkers), int(mean(times)))
    
    ax1.plot(xs, ys,label = 'ratio')
    plt.savefig(fileName)
    plt.show()
    