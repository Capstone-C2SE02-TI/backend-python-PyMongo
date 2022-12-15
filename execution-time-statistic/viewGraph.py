import matplotlib.pyplot as plt
import json
from statistics import mean
import re
from os import walk
from datetime import datetime
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange, DayLocator, HourLocator, DAILY)
rule = rrulewrapper(DAILY, byeaster=1, interval=1)
loc = RRuleLocator(rule)
formatter = DateFormatter('%d/%m/%y')

pattern = re.compile(r'\Sjson$')

if __name__ == '__main__':

    for (*_, filenames) in walk('./'):
        jsonNames = set(filter(pattern.search, filenames))
        break

    # jsonNames = ['coinDataHandler.json']
    for jsonName in jsonNames:

        jsonRawName = jsonName.split('.')[0]
        print(jsonName)
        jsonData = open(f'./{jsonName}')
        executionTime_to_secUnix = json.load(jsonData)
        jsonData.close()
        dates = []
        executionTimes = []

        for secUnix in sorted(executionTime_to_secUnix.keys()):
            dates.append(datetime.fromtimestamp(int(secUnix)))
            executionTimes.append(int(executionTime_to_secUnix[secUnix]))

            # datetime.fromtimestamp
        fig, ax = plt.subplots()
        fig.set_size_inches(20,10)

        
        ax.set_xlim(dates[0], dates[-1])

        plt.plot_date(dates, executionTimes, '.-b', linewidth=1)
        for index in range(1, executionTimes.__len__() - 1):
            if executionTimes[index] > executionTimes[index-1] and executionTimes[index] > executionTimes[index + 1]:            
                ax.annotate(executionTimes[index], (dates[index], executionTimes[index]))
        ax.xaxis.set_major_locator(DayLocator())
        # ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_tick_params(rotation=30, labelsize=10)


        plt.title(f'Time to crawl {jsonRawName}')
        plt.legend(['time'])
        plt.xlabel('Max workers')
        plt.savefig(jsonRawName, dpi = 100)
