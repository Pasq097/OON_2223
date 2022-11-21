# Definition of the class Connection 

class Connection:
    def __init__(self, input, output, signal_power):  # constructor
        """Initialise attributes"""
        self._input = input
        self._output = output
        self._signal_power = signal_power
        self._latency = 0
        self.snr = 0

    @property  # Getter
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @property
    def snr(self):
        return self._snr

    @input.setter
    def input(self, input):
        self._input = input

    @output.setter
    def output(self, output):
        self._output = output

    @signal_power.setter
    def signal_power(self, signal_power):
        self._signal_power = signal_power

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @snr.setter
    def snr(self, snr):
        self._snr = snr
