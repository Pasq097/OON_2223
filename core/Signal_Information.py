
class SignalInformation:
    """model the signal information"""

    def __init__(self, signal_power, path):          # constructor
        """Initialize attributes"""
        self._signal_power = signal_power
        self._noise_power = 0
        self._latency = 0
        self._path = path

    @property  # Getter
    def signal_power(self):
        return self._signal_power

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def latency(self):
        return self._latency

    @property
    def path(self):
        return self._path

    @signal_power.setter  # Setter
    def signal_power(self, signal_power):
        self._signal_power = signal_power

    @noise_power.setter
    def noise_power(self, noise_power):
        self._noise_power = noise_power

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @path.setter
    def path(self, path):
        self._path = path

    # Define the methods to update the signal and noise powers and the latency given an increment of these quantities

    def update_signal_power(self, increment):
        self._signal_power += increment

    def update_noise_power(self, increment):
        self._noise_power += increment

    def update_latency(self, increment):
        self._latency += increment

    # Define a method to update the path once a node is crossed
    def update_path(self):
        array = self._path[1:]
        self._path = array
