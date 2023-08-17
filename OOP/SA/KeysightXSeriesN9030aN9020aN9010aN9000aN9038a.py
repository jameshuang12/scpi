import sys

from .SAClass import SAClass


# See Keysight_X-Series_Analyzer_Programmer's_guide.pdf

class KeysightXSeriesN9030aN9020aN9010aN9000aN9038a(SAClass):
    # Presets the Device
    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.BinaryEndsWithTermination = True
        self.Endian = '<'
        self.Traces = [
            "TRACE1", "TRACE2", "TRACE3",
            "TRACE4", "TRACE5", "TRACE6"
        ]

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

    # Reads the current response values of the active data trace,
    #  reads or writes a memory trace, and reads or writes error terms. 
    def get_data(self, channel: int = 0, trace: str = ''):
        if trace in self.Traces | '':
            self.Data = self.read("TRAC", trace)
        else:
            sys.exit("Trace must be one of the following: {}".format(self.Traces))
