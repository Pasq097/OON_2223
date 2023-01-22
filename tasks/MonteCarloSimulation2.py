from core import network
from Functions_charts import BitRateHist, BlockedConnectionsGraph, CapacityAllocated, DataAllocatedPerLink, chart2, \
    snrMC, LatencyDistribution

# Network congestion
# For a given value of M, fixed number of Monte Carlo runs. For each run collect the metrics of interest
weighted_paths = network.Network()
weighted_paths.connect()
weighted_paths.draw()
# parameters
sel = 'snr'
MC_runs = 300
M = 1
threshold_M = 30
# initialize
list_snr_tot = []
list_latency_tot = []
list_bit_rate_tot = []
list_of_trf_mtrx = []
route_space_lists = []
all_blocked_connections = []
list_of_avg = []
i = 0
# MC loop
if sel == 'snr':
    for i in range(MC_runs):
        print(MC_runs - i)
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
        weighted_paths.n_amplifiers_calc_lines()
        i = i + 1
        if i <= threshold_M:
            M = M + 1
    # graph1
    trf_in = weighted_paths.creation_of_random_traffic_matrix(M)
    graph = DataAllocatedPerLink.allocation_per_link(trf_in, list_of_trf_mtrx)
    graph.show()
    # graph2
    BlockedConnectionsGraph.block_conn(threshold_M, all_blocked_connections)
    # graph3
    graph2 = BitRateHist.bit_rate_hist(list_bit_rate_tot)
    graph2.show()
    # graph 4
    snrMC.snr_mc(list_snr_tot)
    # graph 5
    CapacityAllocated.total_capacity_allocated(route_space_lists)
    # graph 6 (animated)
    chart2.total_capacity_allocated(route_space_lists)

else:
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
        list_latency_tot.append(a)
        weighted_paths.n_amplifiers_calc_lines()
        i = i + 1
        if i <= threshold_M:
            M = M + 1
    # graph 1
    LatencyDistribution.latency_hist(list_latency_tot)
    # graph 2
    trf_in = weighted_paths.creation_of_random_traffic_matrix(M)
    graph = DataAllocatedPerLink.allocation_per_link(trf_in, list_of_trf_mtrx)
    graph.show()
    # graph 3
    BlockedConnectionsGraph.block_conn(threshold_M, all_blocked_connections)
    # graph 4
    graph2 = BitRateHist.bit_rate_hist(list_bit_rate_tot)
    graph2.show()
    # graph 5
    CapacityAllocated.total_capacity_allocated(route_space_lists)
    # graph 6 (animated)
    chart2.total_capacity_allocated(route_space_lists)
