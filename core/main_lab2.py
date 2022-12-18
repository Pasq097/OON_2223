# set the dataframe of main as an attribute of the network 'weighted_paths'
import network
import random
import connection
import matplotlib.pyplot as plt

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
    #special = ['A', 'B']


for k in range(N_CONNECTIONS):
    inp, out = random.sample(list_of_nodes, 2)  # this should take two unique elements from the list
    print("this is destination:" + inp + out)
    connections.append(connection.Connection(inp, out, 1e-3))
sel = 'latency'
weighted_paths.stream(connections, sel)
# print(len(connections))
if sel == 'snr':
    list_of_snr = []
    for temp2 in connections:
        list_of_snr.append(temp2.snr)
        # print(temp2.snr)
    res = list(filter(lambda item: item != 0, list_of_snr))
    # print(res)
    # print(len(res))
    weighted_paths.probe()
    weighted_paths.update_route_space()
    print(weighted_paths.route_space)
    plt.xlabel('SNR [dB]', fontweight='bold')
    plt.ylabel('occurrences', fontweight='bold')
    plt.title("SNR distribution")
    plt.hist(res, bins=20)
    plt.show()
else:
    list_of_latency = []
    for temp in connections:
        list_of_latency.append(temp.latency)
        # print(temp.latency)
    res = list(filter(lambda item: item is not None, list_of_latency))
    # print(len(res))
    a = weighted_paths.probe()
    b = weighted_paths.route_space

    weighted_paths.update_route_space()
    print(b)
    plt.xlabel('latency', fontweight='bold')
    plt.ylabel('occurrences', fontweight='bold')
    plt.title("Latency distribution")
    plt.hist(res, bins=12)
    plt.show()
