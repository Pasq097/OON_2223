import pickle
import numpy as np
import matplotlib.pyplot as plt


blocking_ratio_th = np.linspace(0.001, 0.3, 100)

with open('averages2_1.pickle', 'rb') as f:
    list1 = pickle.load(f)

with open('averages1_1.pickle', 'rb') as f:
    list2 = pickle.load(f)

with open('averages1_3.pickle', 'rb') as f:
    list3 = pickle.load(f)


fig, ax = plt.subplots()

ax.plot(list2, blocking_ratio_th)
plt.yscale('log')

ax.plot(list1, blocking_ratio_th)
plt.yscale('log')
#
ax.plot(list3, blocking_ratio_th)
plt.yscale('log')

plt.show()