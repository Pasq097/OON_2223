import network
import matplotlib.pyplot as plt
from statistics import mean
import BitRateHist
import DataAllocatedPerLink
import CapacityAllocated
import BlockedConnectionsGraph
import chart
import chart2
# Network congestion
# For a given value of M, fixed number of Monte Carlo runs. For each run collect the metrics of interest
weighted_paths = network.Network()
weighted_paths.connect()
weighted_paths.draw()

sel = 'snr'
MC_runs = 30
M = 1
soglia_M = 20
list_snr_tot = []
list_bit_rate_tot = []
list_of_trf_mtrx = []
route_space_lists = []
all_blocked_connections = []
i = 0
if sel == 'snr':
    for i in range(MC_runs):
        print(MC_runs-i)
        weighted_paths = network.Network()
        weighted_paths.connect()
        var = weighted_paths.stream(sel, M)
        route_space = weighted_paths.update_route_space()
        route_space_lists.append(route_space)
        a = var[0]
        b = var[1]
        c = var[2]
        d = var[3]
        all_blocked_connections.append(d)
        list_of_trf_mtrx.append(c)
        list_bit_rate_tot.append(b)
        list_snr_tot.append(a)
        # list_bit_rate_tot.append(c)
        # a = weighted_paths.probe('snr')
        # print(a)
        # print(weighted_paths.route_space)
        weighted_paths.n_amplifiers_calc_lines()
        # list_of_ch_allocated = CapacityAllocated.total_capacity_allocated(weighted_paths.route_space)
        # print(list_snr_tot)
        i = i+1
        if i <= soglia_M:
            M = M + 1

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
list_bit_rate_avg = []
list_of_avg = []
for list in list_snr_tot:
    snr_rate_avg = mean(list)
    list_of_avg.append(snr_rate_avg)
for list2 in list_bit_rate_tot:
    bit_rate_avg = mean(list2)
    list_bit_rate_avg.append(bit_rate_avg)
trf_in = weighted_paths.creation_of_random_traffic_matrix(M)

graph = DataAllocatedPerLink.allocation_per_link(trf_in, list_of_trf_mtrx)
graph.show()
chart2.total_capacity_allocated(route_space_lists)
BlockedConnectionsGraph.block_conn(soglia_M, all_blocked_connections)

graph2 = BitRateHist.bit_rate_hist(list_bit_rate_avg)
graph2.show()

CapacityAllocated.total_capacity_allocated(route_space_lists)

# chart.animated_chart(list_snr_tot)


plt.title("SNR MONTE CARLO")
plt.ylabel('occurrences', fontweight='bold')
plt.xlabel('SNR avarage [dB] ', fontweight='bold')
plt.hist(list_snr_tot, bins=30)
# plt.axvline(bit_rate_avg, color='k', linestyle='dashed', linewidth=1)
plt.show()


