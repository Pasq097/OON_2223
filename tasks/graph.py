import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

blocking_ratio_th = np.linspace(0.001, 0.3, 100)

with open('averages3_1.pickle', 'rb') as f:
    list1 = pickle.load(f)

with open('averages3_2.pickle', 'rb') as f:
    list2 = pickle.load(f)

with open('averages3_3.pickle', 'rb') as f:
    list3 = pickle.load(f)


fig, ax = plt.subplots()
yhat2 = savgol_filter(list1, 51, 3)
ax.plot(yhat2, blocking_ratio_th, label='fixed-rate')
ax.plot(list1, blocking_ratio_th, alpha=0.2)
plt.yscale('log')

ax.plot(list2, blocking_ratio_th, alpha=0.2)
yhat1 = savgol_filter(list2, 51, 3)
ax.plot(yhat1, blocking_ratio_th,label='flex-rate')
plt.yscale('log')

yhat3 = savgol_filter(list3, 51, 3)
ax.plot(yhat3, blocking_ratio_th, label='Shannon')
ax.plot(list3, blocking_ratio_th, alpha=0.2)
ax.grid()
plt.yscale('log')
plt.xlabel('Total traffic allocated [Gbps]')
plt.ylabel('Blocking ratio')
plt.title('Total traffic allocated respect to the blocking ratio for different transceiver strategies')
plt.legend(loc='upper right')


plt.show()
