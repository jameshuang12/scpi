from .OscopeClass import OscopeClass


class TestOscope(OscopeClass):  # TODO make data, timingData, and Measurements based on settings

    def __init__(self, address: str):
        super().__init__(address)
        self.Device_Type = "TEST"
        self.Measurements = ["RxClock", "000000b", "000001b"]  # , "000010b", "000100b", "001000b",
        # "010000b", "100000b", "??????b", "??????b", "??????b"]
        self.Data = ["1,2,3,4", "5,6,7,8", "9,10,11,12"]
        self.TimingData = [1.0, 1.1, 1.2, 1.3]
        self.Number_of_Ports = 4

    "Change Functions to Test Functions "
    def write(self, key: str, value=None):
        self.Settings[key] = self.Settings_Format[key](value)

    def read(self, key: str, extra=""):
        return self.Settings[key]

    def get_all_settings(self):
        for key in self.Settings:
            value = self.Settings[key]
            self.Settings[key] = self.Settings_Format[key](value)

    def send_all_settings(self):
        for key in self.Settings:
            self.Settings[key] = self.New_Settings[key]
