from OOP.DCPS import DCPSClass


class TestDcps(DCPSClass):  # TODO make data, Stimulus, and SParameters based on settings
    Number_of_Modules = 4

    def __init__(self, address: str):
        super().__init__(address)
        self.Number_of_Modules = 4

    # TODO Change Functions to Test Functions
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
