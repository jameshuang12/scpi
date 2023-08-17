from .DMMClass import DMMClass


class TestDmm(DMMClass):
    """ This test class used to test the scripts through the terminal.
    This module is only used for software testing. Hardware testing 
    will still need to be necessary and executed. 

    If confused on how to test, look into DMM Sample Usage for assistance
    """

    def __init__(self, address: str):
        super().__init__(address)
        self.Device_Type = "TEST"
        self.Settings = {
            "GeneralSettings": {
                "Measurement_Function": "",
                "Trigger_Level": 0,
                "Continuous_Read": True,
                "Data_Format": ""
            },
            "MeasurementSettings": {
                "Auto_Measurement_Level": True,
                "Measurement_Range": 0
            }
        }

    "Change Functions to Test Functions"

    def write(self, command: str, value=None, channel: int = -1):
        """ return the command and the value that will send to the hardware.
        """
        if value is not None:
            return f"{command} {value}{self.TChar}"
        else:
            return f"{command} {self.TChar}"

    def read(self, command: str, extra: str = '', channel: int = -1):
        """ prints the command and return the value of the specified command
        """
        self.log_info(f"{command}?{extra}")
        for key, setting_command in self.Setting_Commands.items():
            if setting_command == command:
                for i in self.Settings:
                    if key in self.Settings[i].keys():
                        return self.Settings[i][key]

    def send_all_settings(self):
        """ Sets up all the new settings by updating the current setting
        """
        for key in self.Settings:
            for setting in self.Settings[key]:
                self.Settings[key][setting] \
                    = self.New_Settings[key][setting]
