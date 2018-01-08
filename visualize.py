import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

big_total = []
builds = [10, 15, 30, 50, 75, 100]
files = ['1_loop_breaker_number_of_builds_30',
         '2_loops_breaker_number_of_builds_30',
         '3_loops_breaker_number_of_builds_30',
         '4_loops_breaker_number_of_builds_25']


for file in files:
   with open(file + '.json') as json_data:
       d = json.load(json_data)
       big_total.append({"execution": file, "duration": float(d['total average duration']),
                     "errors": int(d['total number of errors'])})


# big_total.append({"Jmeter Users / API Users": "25 / 50", "API Users": 50, "API Time": 188, "Jmeter Time": 153, "Errors": 0})
# big_total.append({"Jmeter Users / API Users": "35 / 60", "API Users": 65, "API Time": 232, "Jmeter Time": 173, "Errors": 0})
# big_total.append({"Jmeter Users / API Users": "40 / 80", "API Users": 80, "API Time": 278, "Jmeter Time": 196, "Errors": 0})
# big_total.append({"Jmeter Users / API Users": "50 / 100", "API Users": 100, "API Time": 413, "Jmeter Time": 231, "Errors": 0})
# df = pd.DataFrame(big_total)
# print (df)

fig, ax1 = plt.subplots()
y1 = [y["duration"] for y in big_total]
x1 = [y["execution"] for y in big_total]
y2 = [y["errors"] for y in big_total]

ax2 = ax1.twinx()

ax1.plot(x1, y1, 'g-')
ax2.plot(x1, y2, 'b-')

ax1.set_xlabel('Execution Type')
ax1.set_ylabel('Average Duration', color='g')
ax2.set_ylabel('Errors', color='b')

# df.plot(x='execution', y='data')
plt.ylim (ymin=0)
plt.show()