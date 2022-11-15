import json
import node
import line
import numpy as np
import matplotlib.pyplot as plt

from core import PROVA_DFS


class Network:
    """Model for the network"""

    def __init__(self):  # Constructor, has to read the given JSON file and create all instances of all nodes and lines
        self._nodes = {}  # il dizionario deve avere come chiave la label del nodo e come valore l'istanza del nodo
        self._lines = {}  # il dizionario ha come key il nome della linea AB,BF etc e come value l'istanza della linea
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

    def draw(self, dictionary):
        x_values = []
        y_values = []
        k = 0
        for _ in dictionary.keys():
            instances = list(dictionary.keys())
            values = dictionary[instances[k]]
            plot_values = list(values["position"])
            x_values.append(plot_values[0])
            y_values.append(plot_values[1])
            k = k + 1

        x = np.array(x_values)
        y = np.array(y_values)
        plt.scatter(x, y)

        for temp in self._nodes:
            q1 = self._nodes[temp].position

            for temp2 in self._nodes[temp].connected_nodes:
                q2 = self._nodes[temp2].position
                x, y = [q1[0], q2[0]], [q1[1], q2[1]]
                plt.plot(x, y)
        plt.show()

    def connect(self):
        # need to call node and create successive as dictionary { node : "lines connected to the node"}
        for key in self._nodes:  # it gives the list of the letter A, B ,C....
            for temp in self._nodes[key].connected_nodes:  # it gives the connected nodes of the specific object node
                self._nodes[key].successive[key + temp] = self._lines[key + temp]
        # need to call line and create successive as dictionary {line : "node connected to the line"}
        for key in self._lines:
            self._lines[key].successive[key] = self._nodes[key[1]]

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

    def propagate(self, signal_information):
        # has to propagate the signal_information through the specified path
        # return the modified spectral_information's
        # it call the first propagate, it's like starting the domino
        for node in self._nodes:
            if len(signal_information.path) == 0:
                return
            if signal_information.path[0] == node[0]:
                self._nodes[node].propagate(signal_information)


#net1 = Network()
# a = net1.dictionary
# b = net1.nodes
#c = net1.lines
# d = net1.connect
# e = net1.find_all_paths("A", "F")
#print(c)
#print(net1.lines['AB'].length)

# net1.draw(a)
