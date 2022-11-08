import Signal_Information


class Node:
    """Model the nodes"""

    def __init__(self, label, position, connected_nodes):  # Constructor
        """initialise attributes"""
        self._label = label
        self._position = position
        self._connected_nodes = connected_nodes
        self._successive = {}

    @property  # getter
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

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

    # Define a propagate method that update a signal information object modifying its path attribute and call the
    # successive element propagate method, accordingly to the specified path.

  #  def propagate(self, label, successive, connected_nodes, position):
