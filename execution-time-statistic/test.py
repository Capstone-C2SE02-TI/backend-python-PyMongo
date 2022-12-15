# Implementation of matplotlib function
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import numpy as np
   
date1 = datetime.datetime(2020, 4, 2)
date2 = datetime.datetime(2020, 4, 6)
delta = datetime.timedelta(hours = 6)
dates = drange(date1, date2, delta)
   
y = np.arange(len(dates))
   
fig, ax = plt.subplots()
ax.plot_date(dates, y ** 2, 'g')
   
ax.set_xlim(dates[0], dates[-1])
   
ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(range(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%y'))
   
ax.fmt_xdata = DateFormatter('% Y-% m-% d % H:% M:% S')
fig.autofmt_xdate()
plt.title('matplotlib.pyplot.plot_date() function Example', fontweight ="bold")
plt.show()