from .SGClass import SGClass


class TestSg(SGClass):
    """ This test class used to test the scripts through the terminal.
    This module is only used for software testing. Hardware testing 
    will still need to be necessary and executed. 

    If confused on how to test, look into PG Sample Usage for assistance
    """

    def __init__(self, address: str):
        super().__init__(address)
        self.Device_Type = "TEST"
        self.Settings = {
            "GeneralSettings": {
                "Output_Amplitude": 0.0,
                "Waveform_Shape": "",
                "Frequency": 0,
                "Power_Control": 0,
                "Start_Frequency": 300e4,
                "Stop_Frequency": 300e4,
                "Center_Frequency": 10,
                "Frequency_Span": 10,
                "Frequency_Sweep": "",
                "Sweep_Space": "",
                "Space_Step_Width": 0,
                "Pulse_Mode": "PTR",
                "RF_Frequency_Sweep_Cycle": "",
                "Pulse_Generator_State": False,
                "Screen_Saver_Mode": True
            },
            "ModGeneratorSettings": {
                "LF_Generator_Output": False,
                "LF_Frequency_Sweep": ""
            },
            "ModulationSettings": {
                "Amplitude_Modulation": False,
                "Frequency_Modulation": False,
                "Phase_Modulation": False
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
