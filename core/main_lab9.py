import network
import CapacityAllocated

weighted_paths = network.Network()
weighted_paths.connect()
weighted_paths.draw()
# create a list of instances of the class connections over 100 connected nodes (100 different nodes couples)
# choose a random input node and a random output node
list_of_nodes = []
connections = []
sel = 'latency'
weighted_paths.stream(sel)

if sel == 'snr':
    a = weighted_paths.probe('snr')
    print(a)
    weighted_paths.update_route_space()
    print(weighted_paths.route_space)
    weighted_paths.n_amplifiers_calc_lines()
    list_of_ch_allocated = CapacityAllocated.total_capacity_allocated(weighted_paths.route_space)

else:
    a = weighted_paths.probe('latency')
    print(a)
    # find the bit rates of the accepted connections
    weighted_paths.update_route_space()
    print(weighted_paths.route_space)
    list_of_ch_allocated = CapacityAllocated.total_capacity_allocated(weighted_paths.route_space)



