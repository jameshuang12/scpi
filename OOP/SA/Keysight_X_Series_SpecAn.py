import sys
from SAClass import SAClass

# See Keysight_X-Series_Analyzer_Programmer's_guide.pdf

class Keysight_X_Series_N9030A_N9020A_N9010A_N9000A_N9038A(SAClass):
    BinaryEndsWithTermination = True
    Endian = '<'
    Traces = [
        "TRACE1", "TRACE2", "TRACE3", 
        "TRACE4", "TRACE5", "TRACE6"
    ]

    #Presets the Device
    def send_Preset(self):
        currentTimeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        self.write("SYST:PRES")
        self.write(self.Common_SCPI["WaitToContinue"])
        self.Device.settimeout(currentTimeout)
        self.get_All_Settings()

    #Aborts a running measurement and resets the trigger system.
    def send_Abort(self):
        self.write("ABOR")

    #Initiates a sweep when the device is not in continuous sweep
    def send_Initiate(self):
        self.write("INIT:IMM")

    #Reads the current response values of the active data trace, 
    #  reads or writes a memory trace, and reads or writes error terms. 
    def get_Data(self, Trace:str=''):
        if Trace in self.Traces|'':
            self.Data = self.read("TRAC", Trace)
        else:
            sys.exit("Trace must be one of the following: {}".format(self.Traces))

