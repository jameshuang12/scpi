import numpy as np

from .SAClass import SAClass


class TestSa(SAClass):  # TODO make data, and frequencies based on settings
    def __init__(self, address: str):
        super().__init__(address)
        self.Device_Type = "TEST"
        self.Measurements = []  # RxClock", "000000b", "000001b", "000010b", "000100b", "001000b",
        # "010000b", "100000b", "??????b", "??????b", "??????b"]
        self.Data = np.int32(749.354670004)  # , "5,6,7,8", "9,10,11,12"]
        self.Frequencies = []
        self.Number_of_Ports = 1

    "Change Functions to Test Functions"
    def write(self, key: str, value=None):
        self.Settings[key] = self.Settings_Format[key](value)

    def read(self, key: str, extra: str = ''):
        return self.Settings[key]

    def get_all_settings(self):
        for key in self.Settings:
            value = self.Settings[key]
            self.Settings[key] = self.Settings_Format[key](value)

    def send_all_settings(self):
        for key in self.Settings:
            self.Settings[key] = self.New_Settings[key]
