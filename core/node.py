from core import line

class Node:
    """Model the nodes"""

    def __init__(self, label, position, connected_nodes):  # Constructor
        """initialise attributes"""
        self._label = label
        self._position = position
        self._connected_nodes = connected_nodes
        self._successive = {}
        self._switching_matrix = None
        self._transceiver = None

    @property  # getter
    def label(self):
        return self._label

    @property
    def label(self):
        return self._transceiver

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @property
    def switching_matrix(self):
        return self._switching_matrix

    @label.setter  # Setter
    def label(self, label):
        self._label = label

    @position.setter
    def position(self, position):
        self._position = position

    @connected_nodes.setter
    def connected_nodes(self, connected_nodes):
        self._connected_nodes = connected_nodes

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    @switching_matrix.setter
    def switching_matrix(self, switching_matrix):
        self._switching_matrix = switching_matrix

    # Define a propagate method that update a signal information object modifying its path attribute and call the
    # successive element propagate method, accordingly to the specified path.

    def propagate(self, light_path):
        # it has to propagate the signal_information, in the node the next element is a line
        # we need to access the dict successive and update the path
        # update the path so if the path in the obj was A,B,C.. it will # be B,C,D.. note I'm moving "on the nodes" not the line, the propagate of line don't need to update the path
        # path = signal_information.path    # successive = {"AB": obj of the line AB}
        # set for each line the optimal launch power
        light_path.update_path()
        the_current_power_is = light_path.signal_power
        light_path.signal_power = 1*10**-3
        for line in self._successive:
            if len(light_path.path) == 0:        # we reach the destination node
                return
            if light_path.path[0] == line[1]:    # propagate on the successive line
                p_opt = self._successive[line].propagate(light_path)   # set the optimal power
                light_path.signal_power = p_opt
                self._successive[line].propagate(light_path)
