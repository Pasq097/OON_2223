from Signal_Information import SignalInformation


class LightPath(SignalInformation):
    def __init__(self, signal_power, path, light_path):
        """Initialize attributes"""
        super(LightPath, self).__init__(signal_power, path)
        self._light_path = light_path  # is an integer, it has to indicate which frequency slot the signal occupies
        self._Rs = 32 * 10**9
        self._df = 50 * 10**9
        # when it is propagated

    def light_path(self, light_path):
        self._light_path = light_path

    @property  # Getter
    def Rs(self):
        return self._Rs

    @property  # Getter
    def df(self):
        return self._df
