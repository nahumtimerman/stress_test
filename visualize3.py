result = [{"execution": "5", "duration": 2795.2799999713898, "memory": 25.81113498030786, "errors": 0, "average_cpu_percent": 20.87747941281764},
          {"execution": "10", "duration": 1915.6349999904633, "memory": 29.383333333333585, "errors": 0, "average_cpu_percent": 34.83463949843253},
          {"execution": "25", "duration": 1333.2460000514984, "memory": 32.375075075075, "errors": 0, "average_cpu_percent": 47.088888888888796},
          {"execution": "50", "duration": 1248.906000137329, "memory": 35.91712439418408, "errors": 1, "average_cpu_percent": 50.71429725363495}]


import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator


ml = MultipleLocator(1)

fig, ax1 = plt.subplots()
y1 = [y["duration"] for y in result]
x1 = [int(y["execution"]) for y in result]
y2 = [y["errors"] for y in result]

ax2 = ax1.twinx()

ax1.plot(x1, y1, 'g-')
ax2.plot(x1, y2, 'ro', markersize=5)


ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
ax1.set_xlabel('Concurrent threads')
ax1.set_ylabel('Duration of entire 100 block', color='g')
ax2.set_ylabel('Errors', color='b')

# df.plot(x='execution', y='data')
plt.ylim (ymin=0)
plt.show()