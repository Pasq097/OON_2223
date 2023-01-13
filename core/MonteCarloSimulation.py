import network
import CapacityAllocated
import matplotlib.pyplot as plt
from statistics import mean
# Single traffic matrix scenario
# For a given value of M, fixed number of Monte Carlo runs. For each run collect the metrics of interest
weighted_paths = network.Network()
weighted_paths.connect()
weighted_paths.draw()

sel = 'snr'
MC_runs = 100
list_snr_tot = []
i = 0
if sel == 'snr':
    for i in range(MC_runs):
        weighted_paths = network.Network()
        weighted_paths.connect()
        b = weighted_paths.stream(sel)
        list_snr_tot.append(b)
        a = weighted_paths.probe('snr')
        #print(a)
        weighted_paths.update_route_space()
        #print(weighted_paths.route_space)
        weighted_paths.n_amplifiers_calc_lines()
        #list_of_ch_allocated = CapacityAllocated.total_capacity_allocated(weighted_paths.route_space)
        #print(list_snr_tot)
        i = i+1
else:
    for i in len(MC_runs):
        weighted_paths.stream(sel)
        a = weighted_paths.probe('latency')
        print(a)
        # find the bit rates of the accepted connections
        weighted_paths.update_route_space()
        print(weighted_paths.route_space)
        list_of_ch_allocated = CapacityAllocated.total_capacity_allocated(weighted_paths.route_space)
        i = i+1

list_of_avg = []
for list in list_snr_tot:
    snr_rate_avg = mean(list)
    list_of_avg.append(snr_rate_avg)


plt.title("SNR MONTE CARLO")
plt.ylabel('occurrences', fontweight='bold')
plt.xlabel('SNR avarage ', fontweight='bold')
plt.hist(list_of_avg, bins=12)
#plt.axvline(bit_rate_avg, color='k', linestyle='dashed', linewidth=1)
plt.show()


