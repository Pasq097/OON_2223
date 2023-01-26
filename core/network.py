import json
import random
from core import connection, node, line
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import math
from core import PROVA_DFS, update_route, Checking_ch, LightPath
import scipy.special as scipy
from Functions_charts import BitRateHist, LatencyDistribution


class Network:
    """Model for the network"""

    def __init__(self):  # Constructor, has to read the given JSON file and create all instances of all nodes and lines
        self._nodes = {}  # il dizionario deve avere come chiave la label del nodo e come valore l'istanza del nodo
        self._lines = {}  # il dizionario ha come key il nome della linea AB,BF etc e come value l'istanza della linea
        self._route_space = None
        self._df = None
        # with open('../resources/nodes.json', 'r') as file:
        #     self._dictionary = json.load(file)
        #     k = 0
        #     x_values = []
        #     y_values = []
        #     labels = list(self._dictionary.keys())
        #     nodes = list(self._dictionary.keys())
        #     for _ in self._dictionary.keys():
        #         values = self._dictionary[nodes[k]]
        #         nodes[k] = node.Node(nodes[k], values["position"], values["connected_nodes"])
        #         k = k + 1
        # self._nodes = {k: v for k, v in zip(labels, nodes)}
        # obj = list(self._nodes.values())
        # edge = []
        #
        # for nodo in self._nodes.keys():
        #     for p in self._nodes[nodo].connected_nodes:
        #         edge.append(nodo + p)
        #
        # distances = []
        # temp = []
        # for nodo in self._nodes.values():
        #     q = nodo.position
        #     temp = nodo.connected_nodes
        #     for temporary in range(0, len(temp)):
        #         w = self._nodes[temp[temporary]].position
        #         distance = ((q[0] - w[0]) ** 2 + (q[1] - w[1]) ** 2) ** 0.5
        #         distances.append(distance)
        # lines = []
        # for _ in edge:
        #     for var in distances:
        #         lines.append(line.Line(edge, var))
        # self._lines = {k: v for k, v in zip(edge, lines)}

        with open(r'C:\Users\Pac\OON_2223\resources\full_network.json') as file:
            self._dictionary_2 = json.load(file)
            k = 0
            x_values = []
            y_values = []
            labels = list(self._dictionary_2.keys())
            nodes = list(self._dictionary_2.keys())
            for _ in self._dictionary_2.keys():
                values = self._dictionary_2[nodes[k]]
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

        self._switching_matrices = {}

        for key in self._dictionary_2:
            a = self._dictionary_2[key]['switching_matrix']
            self._switching_matrices[key] = a
        self._strategy = []
        if "transceiver" in self._dictionary_2:
            self._strategy.append(self._dictionary_2[key]['transceiver'])
        else:
            self._strategy.append('flex_rate')

        number_of_channels = self._dictionary_2['A']['switching_matrix']
        self.n_ch = len(number_of_channels['B']['B'])

    @property
    def dictionary_2(self):
        return self._dictionary_2

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
        for _ in self._dictionary_2.keys():
            instances = list(self._dictionary_2.keys())
            values = self._dictionary_2[instances[k]]
            plot_values = list(values["position"])
            x_values.append(plot_values[0])
            y_values.append(plot_values[1])
            k = k + 1

        x = np.array(x_values)
        y = np.array(y_values)
        plt.scatter(x, y)
        k = 0
        for key in self._dictionary_2:
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
        for node in self._dictionary_2[start]["connected_nodes"]:
            if node not in path:
                newpaths = PROVA_DFS.find_all_paths(self._dictionary_2, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def n_amplifiers_calc_lines(self):
        for linea in self._lines:
            length = self._lines[linea].length
            n_a = length / (80 * 10 ** 3)
            n_a = round(n_a)
            # print(n_a)
            self._lines[linea].n_amplifiers = n_a

    def connect(self):
        # need to call node and create successive as dictionary { node : "lines connected to the node"}
        for key in self._nodes:  # it gives the list of the letter A, B ,C....
            for temp in self._nodes[key].connected_nodes:  # it gives the connected nodes of the specific object node
                self._nodes[key].successive[key + temp] = self._lines[key + temp]
        # need to call line and create successive as dictionary {line : "node connected to the line"}
        for key in self._lines:
            self._lines[key].successive[key] = self._nodes[key[1]]

        # creation of the switching matrix for each node
        # dictA{ 'B' : { 'B': [0*10], 'C':[CHs], 'D':[CHs] }, 'C' : {...}...
        dict_of_node = {}

        for key in self._nodes:
            # print(key)
            con_nod = []
            for temp in self._nodes[key].connected_nodes:
                con_nod.append(temp)

            x = np.ones(6, dtype=int)
            dict_of_node = {ver: {col: x for col in con_nod} for ver in con_nod}

            for i in dict_of_node:
                for j in dict_of_node[i]:
                    if i == j:
                        dict_of_node[i][j] = np.zeros(6, dtype=int)
            # print(dict_of_node)
            self._nodes[key].switching_matrix = dict_of_node

        for key in self._dictionary_2:
            self._nodes[key].switching_matrix = self._switching_matrices[key]
            for i in self._strategy:
                self._nodes[key].transceiver = i

        # block = self._nodes['A'].switching_matrix['C']['B']
        # print(block)
        # block = current_switching_matrix['A']['B']
        # print(block)
        # dataframe creation
        self.n_amplifiers_calc_lines()
        nodes_in_network = list(self._dictionary_2.keys())
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
            s1 = LightPath.LightPath(1 * 10 ** -3, temp, 1)
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
        self._df = pd.DataFrame(mylist, column, dtype=None)
        self._df = self._df.transpose()
        # print(self._df)                               ##############################

        dict_03 = {}
        for i in range(0, self.n_ch):
            dict_03[i] = 1
        self._route_space = pd.DataFrame(dict_03, index=res)
        # print(self._route_space)                       #######################################

    def propagate(self, light_path):
        # has to propagate the signal_information through the specified path
        # return the modified spectral_information's
        # it call the first propagate, it's like starting the domino
        for node in self._nodes:
            if len(light_path.path) == 0:
                return
            if light_path.path[0] == node[0]:
                self._nodes[node].propagate(light_path)

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

    def probe(self, sel='latency'):
        # need to create two dataframe one for latency and one for SNR
        for key in self._nodes:  # it gives the list of the letter A, B ,C....
            for temp in self._nodes[key].connected_nodes:  # it gives the connected nodes of the specific object node
                self._nodes[key].successive[key + temp] = self._lines[key + temp]
            # need to call line and create successive as dictionary {line : "node connected to the line"}
        for key in self._lines:
            self._lines[key].successive[key] = self._nodes[key[1]]
            # dataframe creation
        nodes_in_network = list(self._dictionary_2.keys())
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
            s1 = LightPath.LightPath(1 * 10 ** -3, temp, 1)
            self.propagate(s1)
            total_accumulated_latency.append(s1.latency)
            total_accumulated_noise.append(s1.noise_power)
            x = math.log10(s1.signal_power / s1.noise_power)
            y = 10 * x
            signal_to_noise_ratio.append(y)
        dict_01 = {}
        if sel == 'latency':
            for i in range(0, self.n_ch):
                dict_01[i + 1] = total_accumulated_latency
            pd.set_option('display.max_rows', None)
            df_latency = pd.DataFrame(dict_01, index=res, dtype=float)
            return df_latency
        elif sel == 'snr':
            dict_02 = {}
            for i in range(0, self.n_ch):
                dict_02[i + 1] = signal_to_noise_ratio
            pd.set_option('display.max_rows', None)
            df_snr = pd.DataFrame(dict_02, index=res, dtype=float)
            return df_snr

    def calculate_bit_rate(self, light_path, path, strategy):
        path_to_search = '->'.join(path)
        df = self.probe('snr')
        var = list(df.loc[path_to_search])
        var_lin = 10 ** (var[0] / self.n_ch)
        R_s = light_path.Rs
        # R_s = 32 * 10 ** 9  # GHz
        B_n = 12.5 * 10 ** 9  # GHz
        BER = 10 ** -3
        # print('the GSNR is '+ str(var[0]))
        if strategy == 'fixed_rate':
            x = (R_s / B_n)
            y = scipy.erfcinv(2 * BER)
            z = 2 * y ** 2
            tot = z * x
            # print('the tot is' + str(tot))
            if var_lin >= tot:
                R_b = 100  # Gbps
            else:
                R_b = 0
        elif strategy == 'flex_rate':
            x = (R_s / B_n)
            y = scipy.erfcinv(2 * BER)
            z = 2 * y ** 2
            tot = z * x
            # print(tot)
            tot2 = (14 / 3) * (scipy.erfcinv((3 / 2) * BER)) ** 2 * x
            # print(tot2)
            tot3 = 10 * (scipy.erfcinv((8 / 3) * BER)) ** 2 * x
            # print(tot3)
            if var_lin < tot:
                R_b = 0
            elif tot <= var_lin <= tot2:
                R_b = 100
            elif tot2 <= var_lin <= tot3:
                R_b = 200
            elif var_lin >= tot3:
                R_b = 400
        elif strategy == 'shannon':
            R_b = (2 * R_s * math.log2(1 + var_lin * (R_s / B_n))) / (10 ** 9)
        return R_b

    def creation_of_random_traffic_matrix(self, M=1):
        columns_dict = {}
        values = M * 100
        x = values
        for key in self._nodes:
            columns_dict[key] = values
        dict = {ver: {col: x for col in columns_dict} for ver in columns_dict}
        for i in dict:
            for j in dict[i]:
                if i != j:
                    dict[i][j] = values
                else:
                    dict[i][j] = 0
        return dict

    def traffic_matrix_management(self, traffic_matrix, all_possible_connections):
        # creates and manages the connections given a traffic matrix
        flag = 0
        while flag == 0:
            conn = random.sample(all_possible_connections, 1)
            inp, out = conn[0][0], conn[0][1]
            x = traffic_matrix[inp][out]
            if x == 0:
                flag = 0
                values = []
                for x in traffic_matrix.values():
                    for y in x.values():
                        values.append(y)
                flag_control_1 = all(val == 0 for val in values)

                if flag_control_1 == True:
                    break
            else:
                flag = 1
                flag_control_1 = False

        return inp, out, flag_control_1

    # def reset_of_the_ch(self):
    #     for line_obj in self._lines:
    #         self._lines[line_obj]._state = np.ones(10, dtype=int)

    # def reset_route_space(self):
    #     for i in range(0, 350):
    #         pd.set_option('display.max_rows', None)
    #         self._route_space.iloc[i] = 1

    def stream(self, selection='snr', M=1, th=0.3):
        # Route space has to be a pandas dataframe that for all the possible paths describe the availability for each CH
        #         1    2    3     4     5  ... 10
        # A->B    0    0    1     0     1  ... 1
        # B->C    1    0    0     1     0  ... 0
        # ....   ...  ...  ...   ...   ... ... ...
        # How to find out if the CH of a specific path is free or not?
        # Note that one signal from root->target need to be transmitted on the same CH for each line
        flag_control = False
        trf_mtrx = self.creation_of_random_traffic_matrix(M)
        # self.reset_of_the_ch()
        # self.reset_route_space()
        if selection == 'latency':
            list_of_latency = []
            list_of_bit_rate = []
            blocked_connections = 0
            requested_connections = 0
            established_conn = 0
            nodes = []
            blk = 0
            soglia = 0
            for n in self._nodes.keys():
                nodes.append(n)
            all_possible_connections = [x + y for x, y in itertools.permutations(nodes, 2)]
            # print(trf_mtrx)
            while flag_control == False:
                values = self.traffic_matrix_management(trf_mtrx)
                input = values[0]
                output = values[1]
                temp = connection.Connection(input, output, 1e-3)
                requested_connections = requested_connections + 1
                flag_control = values[2]
                possible_paths = self.find_best_latency(input, output)
                k = 0
                for temporary in possible_paths:
                    possible_lines = [''.join(pair) for pair in zip(temporary[:-1], temporary[1:])]
                    # IDEA -> create a dynamic dictionary like this DICT = {'LINE_LABEL': CHANNEL.STATES,.....}
                    # after is possible to check each values in the lines of the path to check for each line the same CH
                    dict_for_ch = {}
                    for temp2 in possible_lines:
                        dict_for_ch[temp2] = self._lines[temp2].state
                    nodes_for_swm = temporary.lstrip(temporary[0]).rstrip(temporary[-1])
                    flag_is = Checking_ch.checking_ch(dict_for_ch, nodes_for_swm, self._nodes,
                                                      temporary)  # in flag_is is stored if there is CH free
                    # and which one is it, the index
                    if flag_is[0] == 1:
                        the_path_is = temporary
                        the_ch_is = flag_is[1]
                        break
                    else:
                        k = k + 1
                if k < len(possible_paths):
                    # print('path' + the_path_is)
                    # print('ch'+str(the_ch_is))
                    signal_power = temp.signal_power
                    # print(the_path_is)
                    light_path = LightPath.LightPath(signal_power, the_path_is, the_ch_is)
                    x = temporary[0]
                    strategy = self._nodes[x].transceiver
                    bit_rate = self.calculate_bit_rate(light_path, temporary, strategy)
                    x = trf_mtrx[input][output]
                    new_value = x - bit_rate
                    if new_value < 0:
                        new_value = 0
                    trf_mtrx[temp.input][temp.output] = new_value
                    # print('the bit rate is ' + str(bit_rate))
                    # print(trf_mtrx)
                    # print('the bit rate is ' + str(bit_rate))
                    temp.bit_rate = bit_rate
                    if bit_rate == 0:  # zero bit rate case, need to reject the connection
                        print('the connection over this path is rejected')
                        break
                    self.propagate(light_path)
                    established_conn = established_conn + 1
                    print(established_conn)
                    lines_to_use = [''.join(pair) for pair in zip(the_path_is[:-1], the_path_is[1:])]
                    for temp5 in lines_to_use:
                        self._lines[temp5].state[the_ch_is] = 0
                    nodes_for_swm = the_path_is.lstrip(the_path_is[0]).rstrip(the_path_is[-1])
                    for n_swm in nodes_for_swm:
                        index_swm = the_path_is.index(n_swm)
                        block = (
                            self._nodes[n_swm].switching_matrix[the_path_is[index_swm - 1]][the_path_is[index_swm + 1]])
                        # print('the block is' + str(block))
                        block[the_ch_is] = 0
                        if the_ch_is == 0:
                            block[the_ch_is + 1] = 0
                        elif the_ch_is == self.n_ch - 1:
                            block[the_ch_is - 1] = 0
                        else:
                            block[the_ch_is + 1] = 0
                            block[the_ch_is - 1] = 0
                        # print(block)
                    x = math.log10(light_path.signal_power / light_path.noise_power)
                    y = 10 * x
                    temp.snr = y
                    temp.latency = light_path.latency
                    list_of_latency.append(temp.latency)
                    list_of_bit_rate.append(temp.bit_rate)
                elif k >= len(possible_paths):
                    the_path_is = list(the_path_is)
                    for c in all_possible_connections:
                        if c[0] == the_path_is[0] and c[-1] == the_path_is[-1]:
                            all_possible_connections.remove(c)
                            blk = blk + 1
                    if soglia > 300:
                        flag_control = True
                    temp.snr = 0
                    temp.latency = None
                    soglia = soglia + 1

            return list_of_latency, list_of_bit_rate, trf_mtrx, blk, requested_connections

        elif selection == 'snr':
            list_of_snr = []
            list_of_bit_rate = []
            requested_connections = 0
            all_connections = 0
            nodes = []
            blk = 0
            blocking_ratio = 0
            for n in self._nodes.keys():
                nodes.append(n)
            all_possible_connections = [x + y for x, y in itertools.permutations(nodes, 2)]
            # print(trf_mtrx)
            while flag_control == False and blocking_ratio < th:
                values = self.traffic_matrix_management(trf_mtrx, all_possible_connections)
                input = values[0]
                output = values[1]
                temp = connection.Connection(input, output, 1e-3)
                requested_connections = requested_connections + 1
                flag_control = values[2]
                possible_paths = self.find_best_snr(input, output)
                k = 0
                for temporary in possible_paths:
                    possible_lines = [''.join(pair) for pair in zip(temporary[:-1], temporary[1:])]
                    # IDEA -> create a dynamic dictionary like this DICT = {'LINE_LABEL': CHANNEL.STATES,.....}
                    # after is possible to check each values in the lines of the path to check for each line the same CH
                    dict_for_ch = {}
                    for temp2 in possible_lines:
                        dict_for_ch[temp2] = self._lines[temp2].state
                    nodes_for_swm = temporary.lstrip(temporary[0]).rstrip(temporary[-1])
                    flag_is = Checking_ch.checking_ch(dict_for_ch, nodes_for_swm, self._nodes,
                                                      temporary)  # in flag_is is stored if there is CH free
                    # and which one is it, the index
                    if flag_is[0] == 1:
                        the_path_is = temporary
                        the_ch_is = flag_is[1]
                        break
                    else:
                        k = k + 1
                if k < len(possible_paths):
                    # print('path' + the_path_is)
                    # print('ch'+str(the_ch_is))
                    signal_power = temp.signal_power
                    # print(the_path_is)
                    light_path = LightPath.LightPath(signal_power, the_path_is, the_ch_is)
                    x = temporary[0]
                    strategy = self._nodes[x].transceiver
                    bit_rate = self.calculate_bit_rate(light_path, temporary, strategy)
                    x = trf_mtrx[input][output]
                    new_value = x - bit_rate
                    if new_value < 0:
                        new_value = 0
                    trf_mtrx[temp.input][temp.output] = new_value
                    # print('the bit rate is ' + str(bit_rate))
                    # print(trf_mtrx)
                    # print('the bit rate is ' + str(bit_rate))
                    temp.bit_rate = bit_rate
                    if bit_rate == 0:  # zero bit rate case, need to reject the connection
                        print('the connection over this path is rejected')
                        break
                    self.propagate(light_path)
                    all_connections = all_connections + 1
                    lines_to_use = [''.join(pair) for pair in zip(the_path_is[:-1], the_path_is[1:])]
                    for temp5 in lines_to_use:
                        self._lines[temp5].state[the_ch_is] = 0
                    nodes_for_swm = the_path_is.lstrip(the_path_is[0]).rstrip(the_path_is[-1])
                    for n_swm in nodes_for_swm:
                        index_swm = the_path_is.index(n_swm)
                        block = (
                            self._nodes[n_swm].switching_matrix[the_path_is[index_swm - 1]][the_path_is[index_swm + 1]])
                        # print('the block is' + str(block))
                        block[the_ch_is] = 0
                        if the_ch_is == 0:
                            block[the_ch_is + 1] = 0
                        elif the_ch_is == self.n_ch - 1:
                            block[the_ch_is - 1] = 0
                        else:
                            block[the_ch_is + 1] = 0
                            block[the_ch_is - 1] = 0
                        # print(block)
                    x = math.log10(light_path.signal_power / light_path.noise_power)
                    y = 10 * x
                    temp.snr = y
                    temp.latency = light_path.latency
                    list_of_snr.append(temp.snr)
                    list_of_bit_rate.append(temp.bit_rate)
                elif k >= len(possible_paths):
                    print('non riesco ad allocare il traffico')
                    the_path_is = list(the_path_is)
                    for c in all_possible_connections:
                        if c[0] == the_path_is[0] and c[-1] == the_path_is[-1]:
                            all_possible_connections.remove(c)
                    blk = blk + 1
                    temp.snr = 0
                    temp.latency = None
                blocking_ratio = (blk/requested_connections)
            # print('allocated connections' + str(all_connections))
            return list_of_snr, list_of_bit_rate, trf_mtrx, blk, requested_connections

    def update_route_space(self):

        res = list(self._route_space.index)
        all_paths = []
        for var_t in res:
            var_t = var_t.replace('->', '')
            all_paths.append(var_t)
        result_l = []
        for pat in all_paths:
            result_f = update_route.update_route(pat, self._lines, self._nodes)
            result_l.append(result_f)
        for i in range(0, len(all_paths)):
            pd.set_option('display.max_rows', None)
            self._route_space.iloc[i] = result_l[i]

        return self._route_space