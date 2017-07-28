import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import operator

with open("ping.txt") as myfile:
	content = myfile.readlines()

content = [line.rstrip("\n").split("\t") for line in content]
content = [[' '.join(line[:2]), line[2]] for line in content]
content = [[datetime.datetime.strptime(line[0], "%d/%m/%Y\t%H:%M:%S"), line[1]] for line in content]
data = {line[0]: float(line[1]) for line in content}
dates = [line[0] for line in content]
pings = [float(line[1]) for line in content]

offlineTime = pings.count(0)*10

print("Tempo Offline: %s" % (str(datetime.timedelta(seconds=offlineTime))))

for index, date in enumerate(dates):
	if date - dates[index-1] > timedelta(0,30):
		next_date = dates[index-1] + datetime.timedelta(0,1)
		data[next_date] = np.nan

data_x, data_y  = map(list, zip(*sorted(data.items(), key=operator.itemgetter(0))))

data_zero = {date:(data[date] if data[date] == 0 else np.nan) for date in data.keys()}
data_zero_x, data_zero_y  = map(list, zip(*sorted(data_zero.items(), key=operator.itemgetter(0))))

data_y_smooth = savgol_filter(data_y, 99, 9)
data_y_smooth = [datum_y if datum_y > 0 and data_y[index] != np.nan else np.nan for index, datum_y in enumerate(data_y_smooth)]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylabel('Ping (ms)', color='b')
ax.set_xlabel('Data', color='b')
ax.set_title("Ping na República Hollywoo")

line1, = ax.plot_date(data_x, data_y, fmt='-', linewidth=0.5, color='grey', alpha=0.5, label='Ping')
line2, = ax.plot_date(data_x, data_y_smooth, 'b-', label='Savgol')
line3, = ax.plot(data_zero_x, data_zero_y, 'r-', linewidth=2, label='Offline')

plt.legend(handles=[line1,line2,line3])

fig.tight_layout()
plt.show()
