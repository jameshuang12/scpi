from .PGClass import PGClass


class TestPg(PGClass):
    """ This test class used to test the scripts through the terminal.
    This module is only used for software testing. Hardware testing 
    will still need to be necessary and executed. 

    # If confused on how to test, look into PG Sample Usage for assistance
    """

    def __init__(self, address: str):
        super().__init__(address)
        self.Device_Type = "TEST"
        self.Settings = {
            "GeneralSettings": {
                "Waveform_Type": '',
                "Continuous_Waveform": False,
                "Trigger_Source": '',
                "Trigger_Delay": 0.0,
                "Trigger_Output": False,
                "Trigger_Polarity": '',
                "Burst_Cycles": 0.0
            },
            "WaveformSettings": {
                "Frequency": 0.0,
                "Voltage_Low": -0.05,
                "Voltage_High": 0.05,
                "Phase_Parameter": 0.0,
                "Duty_Cycle": 0.0,
                "Ramp_Symmetry": 0.0,
                "Pulse_Width": 0.0,
                "Bandwidth_Parameter": 0.0,
                "Edge_Time": 0.0,
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
