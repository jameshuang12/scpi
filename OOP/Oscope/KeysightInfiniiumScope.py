import string
import sys
from .OscopeClass import OscopeClass


# See Infiniium-Scopes-Programmer-Guide.pdf

class KeysightInfiniiumScope(OscopeClass):

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.BinaryEndsWithTermination = True
        self.Endian = '<'

    # Basic Functions
    # region

    # The :SINGle command causes the oscilloscope to make a single acquisition when
    # the next trigger event occurs.
    def send_single(self):
        self.write("SING")

    # The :RUN command starts the oscilloscope running. When the oscilloscope is
    # running, it acquires waveform data according to its current settings. Acquisition 
    # runs repetitively until the oscilloscope receives a :STOP command
    def send_run(self):
        self.write("RUN")

    # The :STOP command causes the oscilloscope to stop acquiring data. To restart the
    # acquisition, use the :RUN or :SINGle command.
    def send_stop(self):
        self.write("STOP")

    # Causes the oscilloscope to evaluate all input waveforms
    # and find the optimum conditions for displaying the waveform. It searches each of 
    # the channels for input waveforms and shuts off channels where no waveform is 
    # found. It adjusts the vertical gain and offset for each channel that has a waveform 
    def send_autoscale(self):
        current_timeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        self.write("AUT")
        self.write(self.Common_SCPI["OperationComplete"])
        self.Device.settimeout(current_timeout)

    # Presets the Device
    def send_preset(self):
        current_timeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        self.write("SYST:PRES")
        self.write(self.Common_SCPI["OperationComplete"])
        self.Device.settimeout(current_timeout)
        self.get_all_settings()

    # endregion

    # Channel Settings
    # region

    # Sets a channel to use the specified units for the y-axis
    def send_define_yaxis_units(self, channel: int = 1, unit: str = "VOLT"):
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(self.Analog_Channels))
        unit = unit.upper
        if unit not in self.Yaxis_Units:
            sys.exit("Units must be one of the following: {}".format(self.Yaxis_Units))
        self.write("CHAN{}:UNIT {}".format(channel, unit))

    # Sets a channel to a specified reference level, vertical units and scale must be pre-defined
    def send_define_reference_level(self, channel: int = 1, ref_level: float = 0):
        # TODO set a limit on reference level
        # may convert into scientific string before sending to instrument
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(self.Analog_Channels))
        if ref_level <= -20 or ref_level >= 20:
            sys.exit("Reference Level must be within Scope limits")
        self.write("CHAN{}:OFFS {}".format(channel, ref_level))

    # Sets a channel's vertical scale, or units per division, to a specified value, vertical units must be pre-defined
    def send_define_vertical_scale(self, channel: int = 1, vertical_scale: float = 0.5):
        # TODO set a limit on vertical scale
        # may convert into scientific string before sending to instrument
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(self.Analog_Channels))
        if vertical_scale < 0:
            sys.exit("Vertical units per division must be greater than zero")
        self.write("CHAN{}:SCAL {}".format(channel, vertical_scale))

    # Sets the full scale vertical range of a specified channel to a specified value, vertical units must be pre-defined
    def send_define_vertical_range(self, channel: int = 1, vert_range: float = 10):
        # TODO set a limit on vertical range
        # may convert into scientific string before sending to instrument
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(self.Analog_Channels))
        if vert_range > 10000:
            sys.exit("Vertical range must be within reason.")
        self.write("CHAN{}:RANG {}".format(channel, vert_range))

    # Sets if a specified channel is in differential mode.
    # Channels 1 & 3 may form a differential channel, setting only CHAN1 will do this
    # Channels 2 & 4 may form a differential channel, setting only CHAN2 will do this
    def send_differential_mode(self, channel: int = 1, diff_mode: bool = False):
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(self.Analog_Channels))
        self.write("CHAN{}:DIFF {}".format(channel, diff_mode))

    # endregion

    # Acquisition and Export
    # region

    # Before you download data from the oscilloscope to your
    # computer, always query the points value with the :WAVeform:POINts? query
    # to determine the actual number of acquired points.
    def get_acquired_points(self):
        # TODO determine if number of acquired points can be determined thru ACQuire and WAVeform settings
        actual_points = int(self.read("WAV:POIN"))
        if actual_points > self.Settings["Acquisition_Points"]:
            sys.exit('Points of memory depth to be used must be less than {}'.format(actual_points))
        return actual_points

    # The :DISPlay:DATA? query returns information about the captured data.
    # TODO confirm this returns a screenshot in JPG format, and make file type and screenmode dynamic, add functions to
    #  format screen, window, and traces before taking the screenshot
    # The returned data is followed by a new line character
    def send_display_data(self):
        self.write("DISP:DATA? JPG,SCR")

    # This command initializes the selected channels or functions, then acquires
    # them according to the current oscilloscope settings. When all waveforms 
    # are completely acquired, the oscilloscope is stopped.
    def send_digitize(self, channels: str = "1"):
        # TODO incorporate DIG,DIFF,COMM,POD
        selection = []
        select_str = ""
        channels = channels.replace(",", "")
        channels = channels.translate({ord(i): None for i in string.whitespace})
        for element in range(len(channels)):
            if channels[element] not in self.Analog_Channels:
                sys.exit("The digitization of only the 4x analog channels is currently supported.")
            elif element == 0:
                selection.append("CHAN{}".format(channels[0]))
                select_str = "CHAN{}".format(channels[0])
            elif len(channels) == 1:
                selection.append("CHAN{}".format(channels))
                break
            else:
                selection.append("CHAN{}".format(channels[element]))
                select_str = select_str + ", CHAN{}".format(channels[element])
        self.write("DIG {}".format(select_str))
        return selection

    # Outputs waveform data to the computer over the remote interface.
    # The data is copied from a waveform memory, function, channel, bus, 
    # pod, or digital channel previously specified with the 
    # :WAVeform:SOURce command. This returns a 1D array of comma delimited strings.
    def get_data(self, channel: int = 0, datatype: str = 'SDAT'):
        self.Data.append(self.read("WAV:DATA"))
        return self.Data

    # Pulls x-axis info from scope and returns 1D list of floats
    # must predefine channel source, must be done post-aquisition
    def get_time_data(self):
        self.TimingData = []
        origin = float(self.read("WAV:XOR"))  # time value at first datapoint
        increment = float(self.read("WAV:XINC"))  # time diff between consecutive datapoints
        points = self.Settings["Acquisition_Points"]  # defined by user before aquisition, this is an integer
        for element in range(points):
            self.TimingData.append(origin + (increment * element))
        return self.TimingData

    # endregion
