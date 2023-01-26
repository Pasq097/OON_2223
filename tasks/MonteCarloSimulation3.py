import matplotlib.pyplot as plt
import pickle
from core import network
from Functions_charts import BitRateHist, BlockedConnectionsGraph, CapacityAllocated, DataAllocatedPerLink, chart2, \
    snrMC, LatencyDistribution, BlockingRatio
import numpy as np
# Network congestion
# For a given value of M, fixed number of Monte Carlo runs. For each run collect the metrics of interest
weighted_paths = network.Network()
weighted_paths.connect()
weighted_paths.draw()
# parameters
sel = 'snr'
MC_runs = 100
M = 20
# initialize

list_of_trf_mtrx_tot = []
blocking_ratio_th = np.linspace(0.001, 0.3, 100)
i = 0
t = 0
# MC loop
for th in blocking_ratio_th:
    print(len(blocking_ratio_th)-t)
    i = 0
    for i in range(MC_runs):
        # print((MC_runs-i))
        # print(MC_runs - i)
        list_of_trf_mtrx = []

        weighted_paths = network.Network()
        weighted_paths.connect()
        var = weighted_paths.stream(sel, M, th)
        route_space = weighted_paths.update_route_space()
        a = var[0]
        b = var[1]
        c = var[2]
        d = var[3]
        e = var[4]
        list_of_trf_mtrx.append(c)
        weighted_paths.n_amplifiers_calc_lines()
        i = i + 1
    list_of_trf_mtrx_tot.append(list_of_trf_mtrx)
    t = t+1


mtrx_start = weighted_paths.creation_of_random_traffic_matrix(M)

# calculate the total traffic allocated each time

result = []

for sublist in list_of_trf_mtrx_tot:
    new_sublist = []
    for dictionary in sublist:
        new_dict = {}
        for key in dictionary:
            new_dict[key] = {k: mtrx_start[key][k] - v for k, v in dictionary[key].items()}
        new_sublist.append(new_dict)
    result.append(new_sublist)

averages = []
for sublist in result:
    total = 0
    count = 0
    for dictionary in sublist:
        for key in dictionary:
            for nested_key, nested_value in dictionary[key].items():
                if key != nested_key:
                    total += nested_value
    averages.append(total / len(sublist))
print(averages)
with open('averages2_2.pickle', 'wb') as f:
    pickle.dump(averages, f)

