import string
import sys

from .PNAClass import PNAClass, string_to_list

# See FSPN_UserManual_en_02.pdf
# Data and frequencies will be passed as two lists of numbers


class RohdeSchwarzFspn(PNAClass):

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.BinaryEndsWithTermination = True
        self.Endian = '<'
        self.Traces = [
            "TRACE1",
            "TRACE2",
            "TRACE3",
            "TRACE4",
            "TRACE5",
            "TRACE6"
        ]
        self.TrueFalseString = ["ON", "OFF"]

    # Presets the Device
    def send_preset(self):
        current_timeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        self.write("SYST:PRES")
        self.write(self.Common_SCPI["WaitToContinue"])
        self.Device.settimeout(current_timeout)
        self.get_all_settings()

    # Aborts a running measurement and resets the trigger system.
    def send_abort(self):
        self.write("ABOR")

    # Initiates a sweep when the device is not in continuous sweep
    def send_initiate(self):
        self.write("INIT:IMM")

    # Gets the currently set center/carrier frequency for the measurement
    def get_carrier_freq(self):
        frequency = self.read("FREQ:CENT")
        self.log_info(frequency)
        return frequency

    # Queries the location and level of all spurs that have been detected.
    # Returns the coordinates of detected spurs as a list of alternating frequency and power values.
    def get_spurs(self):
        self.SpurData = self.read("FETC:PNO:SPUR")
        self.SpurData = self.SpurData.translate(
            {ord(i): None for i in string.whitespace})
        self.SpurData = string_to_list(self.SpurData)
        spur_freq = self.SpurData[::2]
        self.log_info(max(spur_freq))
        spur_power = self.SpurData[1::2]
        self.log_info(max(spur_power))
        return self.SpurData

    # Gets the number of points in the current trace
    def get_points(self, trace: str = "TRACE1"):
        if trace not in self.Traces:
            sys.exit("Points can only be counted for: ".format(self.Traces))
        points = self.write("TRAC:POIN", trace)
        return points

    # Returns the coordinates of the trace as alternating frequency and power values
    # in a comma delimited string beginning at the nearest offset frequency.
    def get_data(self, channel: int = 0, trace: str = "TRACE1"):
        if trace not in self.Traces:
            sys.exit("Data can only be pulled for: {}".format(self.Traces))
        self.Data = self.read("TRAC:DATA", trace)
        return self.Data
