import Signal_Information


class LightPath(Signal_Information):
    def __init__(self, signal_power, path, light_path):
        """Initialize attributes"""
        self._signal_power = signal_power
        self._noise_power = 0
        self._latency = 0
        self._path = path
        self._light_path = light_path  # is an integer, it has to indicate which frequency slot the signal occupies
        # when it is propagated

