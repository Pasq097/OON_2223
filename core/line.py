import numpy as np


class Line:
    """Model for the lines"""

    def __init__(self, label, length):  # Constructor
        self._label = label
        self._length = length
        self._state = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #np.ones(10, dtype=int)  # self._state = ["channel x Hz is free/occupied", x10]
        self._successive = {}  # each signal when start propagating needs to stay on the same channel
        # 'till the destination

    @property  # Getter
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def state(self):
        return self._state

    @property
    def successive(self):
        return self._successive

    @label.setter
    def label(self, label):
        self._label = label

    @length.setter
    def length(self, length):
        self._length = length

    @state.setter
    def state(self, state):
        self._state = state

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self, length):
        # the light travel through the fiber at around 2/3 of the speed  of light
        c = 3 * 10 ** 8
        c_f = c * (2 / 3)
        latency = length / c_f
        return latency

    def noise_generation(self, length, signal_power):
        # 1e-9 * signal_power * length
        noise_power = length * (10 ** (-9)) * signal_power
        return noise_power

    def propagate(self, signal_information):
        # if I'm on a line e.g. AB I can only go on a successive node e.g. B it's simpler thant node propagate method
        # it has to update latency and noise_power

        #for temp in self._state:
            #print(temp)

        for node in self._successive:
            self._successive[node].propagate(signal_information)

        # self._state = 0
        # we have to "feed" the method the length of the current line
        noise_power = self.noise_generation(self._length, signal_information.signal_power)
        signal_information.update_noise_power(noise_power)
        latency = self.latency_generation(self._length)
        signal_information.update_latency(latency)

        # we need to modify the method propagate as that it will propagate the signal on a free channel ???
        # we need to check if the channel is free, where?

# l = Line(1,['AB'])
# print(l._state)
