from .VNAClass import VNAClass


class TestVna(VNAClass):
    """Class that represents a physical VNA, allowing for testing of test
    scripts without the use of a physical VNA"""
    # TODO make data, Stimulus, and SParameters based on settings

    def __init__(self, address: str):
        "Initializes values"
        super().__init__(address)
        self.Device_Type = "TEST"
        self.SParameters = ["S11", "S12", "S21", "S22"]
        self.Data = '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16\n'
        self.Stimulus = "1, 2"
        self.Number_of_Ports = 4

    "Change Functions to Test Functions"
    # TODO Move these functions to a new parent class

    def write(self, command: str, value=None, channel: int = -1):
        """ return the command and the value that will send to the hardware.
        """
        if value is not None:
            # Checks a channel number exist
            if channel == -1:
                return f"{command} {value}{self.TChar}"
            else:
                return f"{command} {value}{self.TChar}".format(channel)
        else:
            return f"{command}{self.TChar}"

    def read(self, command: str, extra: str = '', channel: int = -1):
        """ prints the command and return the value of the specified command
        """
        self.log_info(f"{command}?{extra}")
        if channel == -1:
            self.log_info(f"{command}? {extra}{self.TChar}")
        else:
            self.log_info(
                f"{command}? {extra}{self.TChar}".format(channel))
        for key, setting_command in self.Setting_Commands.items():
            if channel != -1:
                setting_command.format(channel)
                command.format(command)
            if setting_command == command:
                for i in self.Settings:
                    if key in self.Settings[i].keys():
                        return self.Settings[i][key]

    def send_all_settings(self):
        """Modifies the self.get_all_settings so that it does not use socket"""
        channel = -1
        for key in self.Settings:
            if key != "GeneralSettings":
                if "channel" in self.Settings[key]:
                    channel = self.Settings[key]['channel']
            for setting in self.Settings[key]:
                self.write(self.Setting_Commands[setting],
                           self.Settings[key][setting], channel)
