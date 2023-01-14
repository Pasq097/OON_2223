import numpy as np
import numpy.random
import matplotlib.pyplot as plt

l = ['A', 'B', 'C',  'D']
D_IN = {'A': {'A': 0, 'B': 800, 'C': 800, 'D': 800, 'E': 800, 'F': 800}, 'B': {'A': 800, 'B': 0, 'C': 800, 'D': 800, 'E': 800, 'F': 800}, 'C': {'A': 800, 'B': 800, 'C': 0, 'D': 800, 'E': 800, 'F': 800}, 'D': {'A': 800, 'B': 800, 'C': 800, 'D': 0, 'E': 800, 'F': 800}, 'E': {'A': 800, 'B': 800, 'C': 800, 'D': 800, 'E': 0, 'F': 800}, 'F': {'A': 800, 'B': 800, 'C': 800, 'D': 800, 'E': 800, 'F': 0}}
D = {'A': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}, 'B': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}, 'C': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}, 'D': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}, 'E': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}, 'F': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}}


result = {}

for key, value in D_IN.items():
    result[key] = {}
    for sub_key, sub_value in value.items():
        result[key][sub_key] = D_IN[key][sub_key] - D[key][sub_key]
print(result)

new_dictonary = {str((k,k1)):v1 for k, v in result.items() for k1,v1 in v.items()}
plt.figure(figsize=(30,200))
plt.bar(new_dictonary.keys(), new_dictonary.values(), width=0.5, color='g')
plt.show()