import json
import node
import line
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import math
import Signal_Information
from core import PROVA_DFS
import Cheking_lines
import Checking_ch
import LightPath


class Network:
    """Model for the network"""

    def __init__(self):  # Constructor, has to read the given JSON file and create all instances of all nodes and lines
        self._nodes = {}  # il dizionario deve avere come chiave la label del nodo e come valore l'istanza del nodo
        self._lines = {}  # il dizionario ha come key il nome della linea AB,BF etc e come value l'istanza della linea
        self._route_space = None
        self._df = None
        with open('nodes.json', 'r') as file:
            self._dictionary = json.load(file)
            k = 0
            x_values = []
            y_values = []
            labels = list(self._dictionary.keys())
            nodes = list(self._dictionary.keys())
            for _ in self._dictionary.keys():
                values = self._dictionary[nodes[k]]
                nodes[k] = node.Node(nodes[k], values["position"], values["connected_nodes"])
                k = k + 1
        self._nodes = {k: v for k, v in zip(labels, nodes)}
        obj = list(self._nodes.values())
        edge = []

        for nodo in self._nodes.keys():
            for p in self._nodes[nodo].connected_nodes:
                edge.append(nodo + p)

        distances = []
        temp = []
        for nodo in self._nodes.values():
            q = nodo.position
            temp = nodo.connected_nodes
            for temporary in range(0, len(temp)):
                w = self._nodes[temp[temporary]].position
                distance = ((q[0] - w[0]) ** 2 + (q[1] - w[1]) ** 2) ** 0.5
                distances.append(distance)
        lines = []
        for _ in edge:
            for var in distances:
                lines.append(line.Line(edge, var))
        self._lines = {k: v for k, v in zip(edge, lines)}

    @property
    def dictionary(self):
        return self._dictionary

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def df(self):
        return self._df

    @property
    def route_space(self):
        return self._route_space

    def draw(self):
        x_values = []
        y_values = []
        k = 0
        for _ in self._dictionary.keys():
            instances = list(self._dictionary.keys())
            values = self._dictionary[instances[k]]
            plot_values = list(values["position"])
            x_values.append(plot_values[0])
            y_values.append(plot_values[1])
            k = k + 1

        x = np.array(x_values)
        y = np.array(y_values)
        plt.scatter(x, y)
        k = 0
        for key in self._dictionary:
            plt.annotate(key, (x_values[k], y_values[k]), weight="bold")
            k = k + 1

        for temp in self._nodes:
            q1 = self._nodes[temp].position

            for temp2 in self._nodes[temp].connected_nodes:
                q2 = self._nodes[temp2].position
                x, y = [q1[0], q2[0]], [q1[1], q2[1]]
                plt.plot(x, y)
        plt.xlabel('x-Axis', fontweight='bold')
        plt.ylabel('y-Axis', fontweight='bold')
        plt.title("Network abstraction")
        plt.show()

    def find_all_paths(self, start, end, path=[]):  # DFS based algorithm
        path = path + [start]
        if start == end:
            return [path]
        paths = []
        for node in self._dictionary[start]["connected_nodes"]:
            if node not in path:
                newpaths = PROVA_DFS.find_all_paths(self._dictionary, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def connect(self):
        # need to call node and create successive as dictionary { node : "lines connected to the node"}
        for key in self._nodes:  # it gives the list of the letter A, B ,C....
            for temp in self._nodes[key].connected_nodes:  # it gives the connected nodes of the specific object node
                self._nodes[key].successive[key + temp] = self._lines[key + temp]
        # need to call line and create successive as dictionary {line : "node connected to the line"}
        for key in self._lines:
            self._lines[key].successive[key] = self._nodes[key[1]]
        # dataframe creation
        nodes_in_network = list(self.dictionary.keys())
        com = itertools.permutations(nodes_in_network, 2)

        res = []
        all_possible_paths = []
        paths = []
        for val in com:
            paths.append(self.find_all_paths(val[0], val[1]))

        for temp in paths:
            for temporary in temp:
                all_possible_paths.append(temporary)

        for paths in all_possible_paths:
            res.append('->'.join(paths))

        # find the total accumulated latency
        # self.connect()
        total_accumulated_latency = []
        total_accumulated_noise = []
        signal_to_noise_ratio = []
        for temp in all_possible_paths:
            s1 = Signal_Information.SignalInformation(1 * 10 ** -3, temp)
            self.propagate(s1)
            total_accumulated_latency.append(s1.latency)
            total_accumulated_noise.append(s1.noise_power)
            x = math.log10(s1.signal_power / s1.noise_power)
            y = 10 * x
            signal_to_noise_ratio.append(y)
        mylist = [res, total_accumulated_latency, total_accumulated_noise, signal_to_noise_ratio]
        # total accumulated noise
        # signal-to-noise ratio 10log(signal_power/noise_power)
        column = ['path', 'total latency', 'accumulated noise', 'signal-to-noise-ratio [dB]']
        pd.set_option("display.precision", 10)
        self._df = pd.DataFrame(mylist, column, dtype=float)
        self._df = self._df.transpose()
        print(self._df)

        dict_03 = {}
        for i in range(0, 10):
            dict_03[i] = 1
        self._route_space = pd.DataFrame(dict_03, index=res)
        print(self._route_space)




    def propagate(self, signal_information):
        # has to propagate the signal_information through the specified path
        # return the modified spectral_information's
        # it call the first propagate, it's like starting the domino
        for node in self._nodes:
            if len(signal_information.path) == 0:
                return
            if signal_information.path[0] == node[0]:
                self._nodes[node].propagate(signal_information)

    # Define a method that returns the path with the best snr for a given pair of nodes
    def find_best_snr(self, node_1, node_2):
        # need to confront all the snr of the specified paths
        row_list = self._df['path'].tolist()
        new_list = []
        for temp in row_list:
            if node_1 == temp[0] and node_2 == temp[-1]:
                new_list.append(temp)
        indexes = []
        for temp2 in new_list:
            a = list(self._df['path'].values == temp2)
            for temp3 in a:
                if temp3 == True:
                    indexes.append(a.index(temp3))
        c = []
        for temp4 in indexes:
            c.append(self._df['signal-to-noise-ratio [dB]'][temp4])
            dictionary_of_val = dict(zip(new_list, c))

        res = sorted(dictionary_of_val.items(), key=lambda x: x[1], reverse=True)
        possible_paths_sorted = []
        for temp5 in res:
            temporary = temp5[0]
            temporary = temporary.replace('->', '')
            possible_paths_sorted.append(temporary)

        return possible_paths_sorted

    def find_best_latency(self, node_1, node_2):
        row_list = self._df['path'].tolist()
        new_list = []
        for temp in row_list:
            if node_1 == temp[0] and node_2 == temp[-1]:
                new_list.append(temp)
        indexes = []
        for temp2 in new_list:
            a = list(self._df['path'].values == temp2)
            for temp3 in a:
                if temp3 == True:
                    indexes.append(a.index(temp3))
        c = []
        for temp4 in indexes:
            c.append(self._df['total latency'][temp4])
            dictionary_of_val = dict(zip(new_list, c))
        res = sorted(dictionary_of_val.items(), key=lambda x: x[1])
        possible_paths_sorted = []
        for temp5 in res:
            temporary = temp5[0]
            temporary = temporary.replace('->', '')
            possible_paths_sorted.append(temporary)
        return possible_paths_sorted  # it returns all possible paths sorted from fastest to slower

    def stream(self, list_of_connections, selection='snr'):
        # Route space has to be a pandas dataframe that for all the possible paths describe the availability for each CH
        #         1    2    3     4     5  ... 10
        # A->B    0    0    1     0     1  ... 1
        # B->C    1    0    0     1     0  ... 0
        # ....   ...  ...  ...   ...   ... ... ...
        # How to find out if the CH of a specific path is free or not?
        # Note that one signal from root->target need to be transmitted on the same CH for each line

        if selection == 'latency':
            for temp in list_of_connections:
                possible_paths = self.find_best_latency(temp.input, temp.output)
                k = 0
                dict_for_ch = {}
                for temporary in possible_paths:
                    # print(temporary)
                    # extract all the lines of the path and then check each CH
                    possible_lines = [''.join(pair) for pair in zip(temporary[:-1], temporary[1:])]
                    # IDEA -> create a dynamic dictionary like this DICT = {'LINELABEL': CHANNEL.STATES,.....}
                    # after is possible to check each values in the lines of the path to check for each line the same CH
                    for temp2 in possible_lines:
                        dict_for_ch[temp2] = self._lines[temp2].state
                    flag_is = Checking_ch.checking_ch(dict_for_ch)  # in flag_is is stored if there is CH free
                    # and which one is it, the index
                    if flag_is[0] == 1:
                        the_path_is = temporary
                        the_ch_is = flag_is[1]
                        break
                    else:
                        k = k + 1
                if k < len(possible_paths):
                    signal_power = temp.signal_power
                    # signal = Signal_Information.SignalInformation(signal_power, the_path_is)
                    light_path = LightPath.LightPath(signal_power, the_path_is, the_ch_is)
                    self.propagate(light_path)
                    lines_to_use = [''.join(pair) for pair in zip(the_path_is[:-1], the_path_is[1:])]
                    for temp5 in lines_to_use:
                        self._lines[temp5].state[the_ch_is] = 0
                        res = list(self._route_space.index)
                        index = ""
                        for l in range(0, len(the_path_is)):
                            if l == 0:
                                index = index + the_path_is[l]
                            else:
                                index = index + '->' + the_path_is[l]

                            for a in res:
                                if index in a:
                                    pd.set_option('display.max_rows', None)
                                    self._route_space.loc[a, the_ch_is] = 0

                    x = math.log10(light_path.signal_power / light_path.noise_power)
                    y = 10 * x
                    temp.snr = y
                    temp.latency = light_path.latency
                elif k >= len(possible_paths):
                    temp.snr = 0
                    temp.latency = None

        elif selection == 'snr':
            for temp in list_of_connections:
                possible_paths = self.find_best_snr(temp.input, temp.output)
                k = 0
                dict_for_ch = {}
                for temporary in possible_paths:
                    # print(temporary)
                    # extract all the lines of the path and then check each CH
                    possible_lines = [''.join(pair) for pair in zip(temporary[:-1], temporary[1:])]
                    # IDEA -> create a dynamic dictionary like this DICT = {'LINELABEL': CHANNEL.STATES,.....}
                    # after is possible to check each values in the lines of the path to check for each line the same CH
                    for temp2 in possible_lines:
                        dict_for_ch[temp2] = self._lines[temp2].state
                    flag_is = Checking_ch.checking_ch(dict_for_ch)      # in flag_is is stored if there is CH free
                                                                        # and which one is it, the index
                    if flag_is[0] == 1:
                        the_path_is = temporary
                        the_ch_is = flag_is[1]
                        break
                    else:
                        k = k + 1
                if k < len(possible_paths):
                    signal_power = temp.signal_power
                    # signal = Signal_Information.SignalInformation(signal_power, the_path_is)
                    light_path = LightPath.LightPath(signal_power, the_path_is, the_ch_is)
                    self.propagate(light_path)
                    lines_to_use = [''.join(pair) for pair in zip(the_path_is[:-1], the_path_is[1:])]
                    for temp5 in lines_to_use:
                        self._lines[temp5].state[the_ch_is] = 0
                        res = list(self._route_space.index)
                        index = ""
                        for l in range(0, len(the_path_is)):
                            if l == 0:
                                index = index + the_path_is[l]
                            else:
                                index = index + '->' + the_path_is[l]

                            for a in res:
                                if index in a:
                                    pd.set_option('display.max_rows', None)
                                    self._route_space.loc[a, the_ch_is] = 0

                    x = math.log10(light_path.signal_power / light_path.noise_power)
                    y = 10 * x
                    temp.snr = y
                    temp.latency = light_path.latency
                elif k >= len(possible_paths):
                    temp.snr = 0
                    temp.latency = None

    def probe(self):
        # need to create two dataframe one for latency and one for SNR
        for key in self._nodes:  # it gives the list of the letter A, B ,C....
            for temp in self._nodes[key].connected_nodes:  # it gives the connected nodes of the specific object node
                self._nodes[key].successive[key + temp] = self._lines[key + temp]
            # need to call line and create successive as dictionary {line : "node connected to the line"}
        for key in self._lines:
            self._lines[key].successive[key] = self._nodes[key[1]]
            # dataframe creation
        nodes_in_network = list(self.dictionary.keys())
        com = itertools.permutations(nodes_in_network, 2)

        res = []
        all_possible_paths = []
        paths = []
        for val in com:
            paths.append(self.find_all_paths(val[0], val[1]))

        for temp in paths:
            for temporary in temp:
                all_possible_paths.append(temporary)

        for paths in all_possible_paths:
            res.append('->'.join(paths))

        # find the total accumulated latency
        # self.connect()
        total_accumulated_latency = []
        total_accumulated_noise = []
        signal_to_noise_ratio = []
        for temp in all_possible_paths:
            s1 = Signal_Information.SignalInformation(1 * 10 ** -3, temp)
            self.propagate(s1)
            total_accumulated_latency.append(s1.latency)
            total_accumulated_noise.append(s1.noise_power)
            x = math.log10(s1.signal_power / s1.noise_power)
            y = 10 * x
            signal_to_noise_ratio.append(y)
        dict_01 = {}
        for i in range(0, 10):
            dict_01[i+1] = total_accumulated_latency
        df_latency = pd.DataFrame(dict_01, index=res)
        print(df_latency)

        dict_02 = {}
        for i in range(0, 10):
            dict_02[i+1] = signal_to_noise_ratio
        df_snr = pd.DataFrame(dict_02, index=res)
        print(df_snr)

#net1 = Network()
#net1.connect()
#net1.probe()