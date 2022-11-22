import Signal_Information
import network
import itertools
import pandas as pd
import math

# For all possible paths between all possible nodes couples, create a pandas dataframe that contain the path string,
# the total accumulated latency, the total accumulated latency noise etc.
# propagation through the paths of spectral information with signal_power of 1 mW


# find all possible nodes couples
net1 = network.Network()
nodes_in_network = list(net1.dictionary.keys())
com = itertools.permutations(nodes_in_network, 2)

res = []
all_possible_paths = []
paths = []
for val in com:
    paths.append(net1.find_all_paths(val[0], val[1]))

for temp in paths:
    for temporary in temp:
        all_possible_paths.append(temporary)

for paths in all_possible_paths:
    res.append('->'.join(paths))

# find the total accumulated latency
net1.connect()
net1.draw()

total_accumulated_latency = []
total_accumulated_noise = []
signal_to_noise_ratio = []
for temp in all_possible_paths:
    s1 = Signal_Information.SignalInformation(1 * 10 ** -3, temp)
    net1.propagate(s1)
    total_accumulated_latency.append(s1.latency)
    total_accumulated_noise.append(s1.noise_power)
    x = math.log(s1.signal_power / s1.noise_power)
    y = 10 * x
    signal_to_noise_ratio.append(y)
mylist = [res, total_accumulated_latency, total_accumulated_noise, signal_to_noise_ratio]

# total accumulated noise

# signal-to-noise ratio 10log(signal_power/noise_power)

column = ['path', 'total latency', 'accumulated noise', 'signal-to-noise-ratio [dB]']
pd.set_option("display.precision", 10)
pd.set_option('display.max_columns', None)
df = pd.DataFrame(mylist, column, dtype=float)
df = df.transpose()
print(df)

