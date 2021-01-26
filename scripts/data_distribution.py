#
#   create a chart that shows the distribution
#   of training instances, ideally this should be
#   as uniform as possible, to ensure that the model
#   performs consistently across all instances
#
#   run from root directory
#       ex: python scripts/data_distribution.py
#

import matplotlib.pyplot as plt
import numpy as np

labels = np.load("data/labels.npy")

data = {}
for label in labels:
    data[label] = data.get(label, 0) + 1

data = sorted(data.items(), key=lambda x: x[1], reverse=True)

x = [d[0] for d in data]
y = [d[1] for d in data]

print(f"number of classes: {len(data)}")
print(f"number of data points: {len(labels)}")

plt.bar(x, y)
plt.show()
