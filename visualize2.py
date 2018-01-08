import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

big_total = []
sleep_between_groups = [5, 20, 60]
actions_per_group = [5, 10, 25, 50]

for build in sleep_between_groups:
   with open('optimizer_{0}.json'.format(build)) as json_data:
       d = json.load(json_data)
       for apg in actions_per_group:
           apg_result = d[str(apg)]
           big_total.append({"execution": str(build) + '/' + str(apg), "duration": float(apg_result['duration']),
                         "errors": int(apg_result['errors']),})


fig, ax1 = plt.subplots()
y1 = [y["duration"] for y in big_total]
x1 = [y["execution"] for y in big_total]
y2 = [y["errors"] for y in big_total]

ax2 = ax1.twinx()

ax1.plot(x1, y1, 'go')
ax2.plot(x1, y2, 'bo')

ax1.set_xlabel('sleep / concurrent threads')
ax1.set_ylabel('Duration of entire 100 block', color='g')
ax2.set_ylabel('Errors', color='b')

# df.plot(x='execution', y='data')
plt.ylim (ymin=0)
plt.show()