#
#   create a chart that shows the distribution
#   of training instances, ideally this should be
#   as uniform as possible, to ensure that the model
#   performs consistently across all instances
#
#   run from root directory
#       ex: python scripts/data_distribution.py

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv

data = {}
with open('data.csv') as file:
    reader = csv.reader(file)
    for r in reader:
        data[r[0]] = data.get(r[0], 0) + 1

data = sorted(data.items(), key=lambda x: x[1], reverse=True)

x = [d[0] for d in data]
y = [d[1] for d in data]

plt.bar(x, y)
plt.show()