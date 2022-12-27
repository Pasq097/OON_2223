import numpy as np


class Line:
    """Model for the lines"""

    def __init__(self, label, length):  # Constructor
        self._label = label
        self._length = length
        self._state = np.ones(10, dtype=int)  # self._state = ["channel x Hz is free/occupied", x10]
        self._successive = {}  # each signal when start propagating needs to stay on the same channel
        # 'till the destination
        self._n_amplifiers = None       # Calculate this number with the line length, one amplifier for 80 km
        self._gain = 16  # dB
        self._noise_figure = 5.5  # dB
        self._alpha_dB = 0.2       # dB / km
        self._beta = 2.13e-26      # ps^2/km
        self._gamma = 1.27e-3         # Wm-1

    @property  # Getter
    def label(self):
        return self._label

    @property
    def n_amplifiers(self):
        return self._n_amplifiers

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

    @n_amplifiers.setter
    def n_amplifiers(self, n_amplifiers):
        self._n_amplifiers = n_amplifiers

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

    def ase_generation(self, number_of_amplifiers):
        # ASE = N (h * f * Bn * NF * [G-1]
        # in linear units
        f = 193.414 * 10**12  # THz
        B_n = 12.5 * 10**9  # GHz
        h = 6.62607015 * 10**-34
        noise_figure_lin = 10 ** (self._noise_figure/20)
        gain_lin = 10 ** (self._gain/20)

        ASE = number_of_amplifiers * (h * f * B_n * noise_figure_lin * (gain_lin - 1))

        return ASE

    # def nli_generation(self):
        # in linear units

    def propagate(self, signal_information):
        # if I'm on a line e.g. AB I can only go on a successive node e.g. B it's simpler thant node propagate method
        # it has to update latency and noise_power
        # for temp in self._state:
        # print(temp)
        # ch = signal_information.light_path
        # self.state[ch] = 0
        for node in self._successive:
            self._successive[node].propagate(signal_information)
        # self._state = 0
        # we have to "feed" the method the length of the current line
        noise_power = self.noise_generation(self._length, signal_information.signal_power)
        signal_information.update_noise_power(noise_power)
        latency = self.latency_generation(self._length)

        # ASE = self.ase_generation(self._n_amplifiers)
        # print(ASE)

        signal_information.update_latency(latency)

        # we need to modify the method propagate as that it will propagate the signal on a free channel ???
        # we need to check if the channel is free, where?
