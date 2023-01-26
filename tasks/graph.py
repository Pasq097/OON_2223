import pickle
import numpy as np
import matplotlib.pyplot as plt


blocking_ratio_th = np.linspace(0.001, 0.1, 80)

#with open('averages4_1.pickle','rb') as f:
    #list1 = pickle.load(f)

with open('averages7_2.pickle', 'rb') as f:
    list2 = pickle.load(f)

#with open('averages3_3.pickle', 'rb') as f:
    #list3 = pickle.load(f)


fig, ax = plt.subplots()

ax.plot(list2, blocking_ratio_th)
plt.yscale('log')

# ax.plot(list2, blocking_ratio_th)
# plt.yscale('log')
#
# ax.plot(list3, blocking_ratio_th)
# plt.yscale('log')

plt.show()