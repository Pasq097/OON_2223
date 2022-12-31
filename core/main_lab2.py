# set the dataframe of main as an attribute of the network 'weighted_paths'
import network
import random
import connection
import matplotlib.pyplot as plt
from statistics import mean
import CapacityAllocated

N_CONNECTIONS = 100
weighted_paths = network.Network()
weighted_paths.connect()
weighted_paths.draw()
# create a list of instances of the class connections over 100 connected nodes (100 different nodes couples)
# choose a random input node and a random output node
list_of_nodes = []
connections = []
for keys in weighted_paths.dictionary:
    list_of_nodes.append(keys)
    # special = ['A', 'B']


for k in range(N_CONNECTIONS):
    inp, out = random.sample(list_of_nodes, 2)  # this should take two unique elements from the list
    print("this is destination:" + inp + out)
    connections.append(connection.Connection(inp, out, 1e-3))
sel = 'snr'
weighted_paths.stream(connections, sel)
# print(len(connections))
if sel == 'snr':
    list_of_snr = []
    bit_rate_list = []
    for temp2 in connections:
        list_of_snr.append(temp2.snr)
        bit_rate_list.append(temp2.bit_rate)
        # print(temp2.snr)
    print(bit_rate_list)
    bit_rate_avg = mean(bit_rate_list)
    plt.title("Bit rate distribution")
    plt.ylabel('occurrences', fontweight='bold')
    plt.xlabel('bit-rate', fontweight='bold')
    plt.hist(bit_rate_list, bins=12)
    plt.axvline(bit_rate_avg, color='k', linestyle='dashed', linewidth=1)
    plt.show()
    res = list(filter(lambda item: item != 0, list_of_snr))
    a = weighted_paths.probe('snr')
    print(a)
    weighted_paths.update_route_space()
    print(weighted_paths.route_space)
    weighted_paths.n_amplifiers_calc_lines()
    weighted_paths.creation_of_random_traffic_matrix()

    plt.xlabel('SNR [dB]', fontweight='bold')
    plt.ylabel('occurrences', fontweight='bold')
    plt.title("SNR distribution")
    plt.hist(res, bins=20)
    plt.show()

    # capacity allocated into the network
    # take all the 2 nodes path and check the occupied channels
    list_of_ch_allocated = CapacityAllocated.total_capacity_allocated(weighted_paths.route_space)



else:
    list_of_latency = []
    bit_rate_list = []
    for temp in connections:
        list_of_latency.append(temp.latency)
        # print(temp.latency)
        bit_rate_list.append(temp.bit_rate)
    # print(bit_rate_list)
    bit_rate_avg = mean(bit_rate_list)
    # print(bit_rate_avg)
    plt.title("Bit rate distribution")
    plt.ylabel('occurrences', fontweight='bold')
    plt.xlabel('bit-rate', fontweight='bold')
    plt.hist(bit_rate_list, bins=12)
    plt.axvline(bit_rate_avg, color='k', linestyle='dashed',linewidth=1)
    plt.show()
    res = list(filter(lambda item: item is not None, list_of_latency))
    # print(len(res))
    a = weighted_paths.probe('latency')
    print(a)
    # find the bit rates of the accepted connections
    weighted_paths.update_route_space()

    print(weighted_paths.route_space)

    plt.xlabel('latency', fontweight='bold')
    plt.ylabel('occurrences', fontweight='bold')
    plt.title("Latency distribution")
    plt.hist(res, bins=12)
    plt.show()

    list_of_ch_allocated = CapacityAllocated.total_capacity_allocated(weighted_paths.route_space)



