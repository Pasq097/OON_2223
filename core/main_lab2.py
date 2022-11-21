# set the dataframe of main as an attribute of the network 'weighted_paths'
import Signal_Information
import network
import pandas as pd

weighted_paths = network.Network()
weighted_paths.connect()
weighted_paths.draw()
print(weighted_paths.find_best_snr())
print(weighted_paths.df)
print(weighted_paths.find_best_latency())

