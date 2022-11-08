
class Line:
    """Model for the lines"""

    def __init__(self, label, length):  # Constructor
        self._label = label
        self._length = length
        self._successive = {}

    @property  # Getter
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @label.setter
    def label(self, label):
        self._label = label

    @length.setter
    def length(self, length):
        self._length = length

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self, length):
        # the light travel through the fiber at around 2/3 of the speed  of light
        c = 3 * 10(**8)
        c_f = c * (2 / 3)
        latency = length / c_f
        return latency

    def noise_generation(self, length, signal_power):
        # 1e-9 * signal_power * length
        noise_power = length * 1 * 10 ** (-9) * signal_power
        return noise_power

 #   def propagate(self):

