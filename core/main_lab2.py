# set the dataframe of main as an attribute of the network 'weighted_paths'
import network
import random
import connection
import matplotlib.pyplot as plt

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

for k in range(4):
    inp, out = random.sample(list_of_nodes, 2)  # this should take two unique elements from the list
    #print("this is dest:" + inp + out)
    connections.append(connection.Connection(inp, out, 1 * 10 ** -3))
weighted_paths.stream(connections)
print(len(connections))

list_of_latency = []
list_of_snr = []
for temp in connections:
    list_of_latency.append(temp.latency)
    #print(temp.latency)

plt.hist(list_of_latency, bins=10)
plt.show()
# plot the graphs
# for the latency

