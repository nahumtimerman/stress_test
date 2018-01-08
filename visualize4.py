import json

things = [5, 10, 25, 33, 50]

results = []

for thing in things:
    with open('recommended_100_actions_per_group_{0}.json'.format(thing)) as json_data:
        d = json.load(json_data)
        results.append({"duration": float(d["Iteration 0"]["total_iteration_duration"]),
                        "errors": int(d["total number of errors"]), "execution": thing})


import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator


ml = MultipleLocator(1)

fig, ax1 = plt.subplots()
y1 = [y["duration"] for y in results]
x1 = [int(y["execution"]) for y in results]
y2 = [y["errors"] for y in results]

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