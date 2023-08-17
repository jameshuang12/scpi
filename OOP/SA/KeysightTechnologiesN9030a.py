from .KeysightXSeriesN9030aN9020aN9010aN9000aN9038a import KeysightXSeriesN9030aN9020aN9010aN9000aN9038a


# See Keysight_X-Series_Analyzer_Programmer's_guide.pdf

class KeysightTechnologiesN9030a(KeysightXSeriesN9030aN9020aN9010aN9000aN9038a):

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.MaxFrequency_GHz = 26.5
        self.DCMinFrequency_Hz = 3
        self.ACMinFrequency_MHz = 10
