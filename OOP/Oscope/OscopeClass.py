# Must define self.Measurements list in script calling oscope library.
# When getting data from more then one channel on scope, must define source,
# get_Data, Save_Data and then redefine source and get_Data/Save_Data again for
# each channel.
# Must define Trigger_Mode before defining trigger settings.
# Must define Trigger_Delay_Mode before defining tigger delay settings.
import os
import string
import sys

import numpy as np
from OOP.BaseDevice import BaseDevice


class OscopeClass(BaseDevice):
    """Class representing an Oscilloscope"""

    # Initialization and Global Settings
    # region

    def __init__(self, address: str, is_usb_connection=False):
        """Initializes device information and settings"""
        super().__init__(address, is_usb_connection)
        self.New_Settings = None
        self.Device_Type = "Oscope"
        self.Yaxis_Units = [
            "VOLT",
            "AMP",
            "WATT",
            "UNKN"
        ]
        self.Analog_Channels = [
            "1",
            "2",
            "3",
            "4"
        ]
        self.Trigger_Mode = [
            "EDGE", "GLIT", "PATT", "STAT",
            "DEL", "TIM", "TV", "COMM",
            "RUNT", "SEQ", "SHOL", "TRAN",
            "WIND", "PWID", "ADV",
            "SBUS1", "SBUS2", "SBUS3", "SBUS4"
        ]
        self.Trigger_Delay_Mode = [
            "EDEL",
            "TDEL"
        ]
        self.Trigger_Edge = [
            "POS",
            "NEG",
            "EITH"
        ]
        self.Acquisition_Mode = [
            "ETIM",
            "RTIM",
            "PDET",
            "HRES",
            "SEGM",
            "SEGP",
            "SEGH"
        ]
        self.Data_Format = {
            "ASC": 0,
            "BIN": 64,
            "BYTE": 8,
            "WORD": 16,
            "FLO": 32
        }
        self.Setting_Commands = {
            "Time_per_Division": "TIM:SCAL",
            "Trigger_Mode": "TRIG:MODE",
            # TODO make settings/commands dynamic across modes
            "Trigger_Delay_Mode": "TRIG:DEL:MODE",
            "Trigger_Delay_Source": "TRIG:DEL:TRIG:SOUR",
            "Trigger_Delay_Edge": "TRIG:DEL:TRIG:SLOP",
            "Trigger_Delay_Arm_Source": "TRIG:DEL:ARM:SOUR",
            "Trigger_Delay_Arm_Edge": "TRIG:DEL:ARM:SLOP",
            "Trigger_Delay_Event_Source": "TRIG:DEL:EDEL:SOUR",
            "Trigger_Delay_Event_Edge": "TRIG:DEL:EDEL:SLOP",
            "Trigger_Delay_Event_Count": "TRIG:DEL:EDEL:COUN",
            "Trigger_Delay_Time": "TRIG:DEL:TDEL:TIME",
            # TODO make this dynamic for other trigger modes (i.e. DELay)
            "Trigger_Edge_Source": "TRIG:EDGE:SOUR",
            # TODO make this dynamic for other trigger modes (i.e. DELay)
            "Trigger_Edge_Edge": "TRIG:EDGE:SLOP",
            "Trigger_Level": "TRIG:LEV",
            "Query_Headers": "SYST:HEAD",
            "Acquisition_Mode": "ACQ:MODE",
            "Acquisition_Complete": "ACQ:COMP",
            "Data_Source": "WAV:SOUR",
            "Data_Format": "WAV:FORM",
            "Acquisition_Count": "ACQ:COUN",
            "Acquisition_Points": "ACQ:POIN"
        }
        self.Extra_Setting = {
            "Time_per_Division": "",
            "Trigger_Mode": "",
            "Trigger_Delay_Mode": "",
            "Trigger_Delay_Source": "",
            "Trigger_Delay_Edge": "",
            "Trigger_Delay_Arm_Source": "",
            "Trigger_Delay_Arm_Edge": "",
            "Trigger_Delay_Event_Source": "",
            "Trigger_Delay_Event_Edge": "",
            "Trigger_Delay_Event_Count": "",
            "Trigger_Delay_Time": "",
            "Trigger_Edge_Source": "",
            "Trigger_Edge_Edge": "",
            "Trigger_Level": "{}".format(self.Settings["GeneralSettings"]
                                         ["Trigger_Source"]),
            "Query_Headers": "",
            "Acquisition_Mode": "",
            "Acquisition_Complete": "",
            "Data_Source": "",
            "Data_Format": "",
            "Acquisition_Count": "",
            "Acquisition_Points": ""
        }
        self.Settings = {
            "GeneralSettings": {
                "Time_per_Division": 0.001,
                "Trigger_Mode": self.Trigger_Mode[4],
                "Trigger_Delay_Mode": self.Trigger_Delay_Mode[1],
                "Trigger_Delay_Source": "CHAN{}".format(
                    self.Analog_Channels[0]),
                "Trigger_Delay_Edge": self.Trigger_Edge[0],
                "Trigger_Delay_Arm_Source": "CHAN{}".format(
                    self.Analog_Channels[0]),
                "Trigger_Delay_Arm_Edge": self.Trigger_Edge[0],
                "Trigger_Delay_Event_Source": "CHAN{}".format(
                    self.Analog_Channels[0]),
                "Trigger_Delay_Event_Edge": self.Trigger_Edge[0],
                "Trigger_Delay_Event_Count": 0,
                "Trigger_Delay_Time": 0,
                "Trigger_Edge_Source": "CHAN{}".format(
                    self.Analog_Channels[0]),
                "Trigger_Edge_Edge": self.Trigger_Edge[0],
                "Trigger_Level": 0,
                "Query_Headers": False,
                "Acquisition_Mode": self.Acquisition_Mode[1],
                "Acquisition_Complete": 100,
                "Data_Source": "CHAN{}".format(self.Analog_Channels[0]),
                "Data_Format": "ASC",
                "Acquisition_Count": 8,
                "Acquisition_Points": 50
            }
        }
        self.Settings_Format = {
            "Time_per_Division": float,
            "Trigger_Mode": str,
            "Trigger_Delay_Mode": str,
            "Trigger_Delay_Source": str,
            "Trigger_Delay_Edge": str,
            "Trigger_Delay_Arm_Source": str,
            "Trigger_Delay_Arm_Edge": str,
            "Trigger_Delay_Event_Source": str,
            "Trigger_Delay_Event_Edge": str,
            "Trigger_Delay_Event_Count": int,
            "Trigger_Delay_Time": float,
            "Trigger_Edge_Source": str,
            "Trigger_Edge_Edge": str,
            "Trigger_Level": float,
            "Query_Headers": bool,
            "Acquisition_Mode": str,
            "Acquisition_Complete": int,
            "Data_Source": str,
            "Data_Format": str,
            "Acquisition_Count": int,
            "Acquisition_Points": int
        }
        # TODO may want to use this to track channels or inputs
        # TODO instead of "measurements"
        self.Measurements = []
        self.TimingData = ""

    def initialize_device(self):
        """Gets all values from the device and performs other initialization
        functions"""
        self.initialize_logger(os.getcwd() + "/logs/", "Oscope")
        self.initialize_values()
        self.send_all_settings()  # I believe that this line does nothing

    def set_time_div(self, time_div: float):
        """Defines the horizontal axis duration between points, which will be
        sent to the device the next time that send_all_settings is used"""
        # TODO Can set a limit on time per division in a future version
        self.New_Settings["GeneralSettings"]["Time_per_Division"] = float(
            time_div)

    def set_trigger_mode(self, trigger_mode: str):
        """Selects the Trigger mode, which will be sent to the device the next
        time that send_all_settings is used"""
        trigger_mode = trigger_mode.upper
        if trigger_mode == "EDGE" or trigger_mode == "DEL":
            self.New_Settings["GeneralSettings"]["Trigger_Mode"] = trigger_mode
        elif trigger_mode in self.Trigger_Mode:
            self.log_warning("Only EDGE and DELay trigger mode settings can currently be modified.")
            self.New_Settings["GeneralSettings"]["Trigger_Mode"] = trigger_mode
        else:
            modes = None
            for key in self.Trigger_Mode:
                if modes:
                    modes = str(key)
                else:
                    modes = "{},{}".format(modes, str(key))
            sys.exit("Trigger Mode must be one of the following: {}".format(
                self.Trigger_Mode))

    def set_delay_trigger_mode(self, trigger_mode: str):
        """Selects the type of delay trigger mode to either events or time,
        which will be sent to the device the nexttime that send_all_settings is
        used"""
        trigger_mode = trigger_mode.upper
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif trigger_mode in self.Trigger_Delay_Mode:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Mode"] = \
                trigger_mode
        else:
            modes = None
            for key in self.Trigger_Delay_Mode:
                if modes:
                    modes = str(key)
                else:
                    modes = "{},{}".format(modes, str(key))
            sys.exit("Trigger Delay Mode must be one of the following: \
                     {}".format(self.Trigger_Delay_Mode))

    def set_delay_trigger_source(self, trigger_source: str):
        """Sets the Trigger On source for a Delay trigger event, which will be
        sent to the device the nexttime that send_all_settings is used"""
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif trigger_source in self.Analog_Channels:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Source"] = \
                "CHAN{}".format(trigger_source)
        else:
            sources = None
            for key in self.Analog_Channels:
                if sources:
                    sources = str(key)
                else:
                    sources = "{},{}".format(sources, str(key))
            sys.exit(
                "Trigger source must be one of the following: \
                    {}".format(sources))

    def set_delay_trigger_edge(self, trigger_edge: str):
        """Sets the trigger slope for the Delay trigger event.
        Trigger Delay Source must be predefined.
        This will be sent to the device the nexttime that send_all_settings is
        used"""
        trigger_edge = trigger_edge.upper
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif trigger_edge in self.Trigger_Edge:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Edge"] = \
                trigger_edge
        else:
            edges = None
            for key in self.Trigger_Edge:
                if edges:
                    edges = str(key)
                else:
                    edges = "{},{}".format(edges, str(key))
            sys.exit("Trigger edge must be one of the following: {}".format(
                self.Trigger_Edge))

    def set_delay_trigger_arm_source(self, trigger_source: str):
        """Sets the Arm On source for arming the trigger circuitry when the
        oscilloscope is in the Delay trigger mode. This will be sent to the
        device the nexttime that send_all_settings is used"""
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif trigger_source in self.Analog_Channels:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Arm_Source"] =\
                "CHAN{}".format(trigger_source)
        else:
            sources = None
            for key in self.Analog_Channels:
                if sources:
                    sources = str(key)
                else:
                    sources = "{},{}".format(sources, str(key))
            sys.exit(
                "Trigger source must be one of the following: \
                    {}".format(sources))

    def set_delay_trigger_arm_edge(self, trigger_edge: str):
        """Sets a positive or negative slope for arming the trigger circuitry
        when the oscilloscope is in the Delay trigger mode.
        Trigger Arm Source must be predefined.
        This will be sent to the device the nexttime that send_all_settings is
        used"""
        trigger_edge = trigger_edge.upper
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif trigger_edge in self.Trigger_Edge:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Arm_Edge"] = \
                trigger_edge
        else:
            edges = None
            for key in self.Trigger_Edge:
                if edges:
                    edges = str(key)
                else:
                    edges = "{},{}".format(edges, str(key))
            sys.exit("Trigger edge must be one of the following: {}".format(
                self.Trigger_Edge))

    def set_delay_trigger_event_source(self, trigger_source: str):
        """Sets the Event source for a Delay By Event trigger event, which will
        be sent to the device the nexttime that send_all_settings is used"""
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif self.Settings["GeneralSettings"]["Trigger_Delay_Mode"] != "EDEL":
            sys.exit("This setting can only be set in Delay by Event Mode.")
        elif trigger_source in self.Analog_Channels:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Event_Source"]\
                = "CHAN{}".format(trigger_source)
        else:
            sources = None
            for key in self.Analog_Channels:
                if sources:
                    sources = str(key)
                else:
                    sources = "{},{}".format(sources, str(key))
            sys.exit(
                "Trigger source must be one of the following: \
                    {}".format(sources))

    def set_delay_trigger_event_edge(self, trigger_edge: str):
        """Sets the trigger slope for a Delay By Event trigger event.
        Trigger Event Source must be predefined.
        This will be sent to the device the nexttime that send_all_settings is
        used"""
        trigger_edge = trigger_edge.upper
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif self.Settings["GeneralSettings"]["Trigger_Delay_Mode"] != "EDEL":
            sys.exit("This setting can only be set in Delay by Event Mode.")
        elif trigger_edge in self.Trigger_Edge:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Event_Edge"] =\
                trigger_edge
        else:
            edges = None
            for key in self.Trigger_Edge:
                if edges:
                    edges = str(key)
                else:
                    edges = "{},{}".format(edges, str(key))
            sys.exit("Trigger edge must be one of the following: {}".format(
                self.Trigger_Edge))

    def set_delay_trigger_event_count(self, trigger_count: int):
        """Sets the event count for a Delay By Event trigger event, which will
        be sent to the device the nexttime that send_all_settings is used"""
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif self.Settings["GeneralSettings"]["Trigger_Delay_Mode"] != "EDEL":
            sys.exit("This setting can only be set in Delay by Event Mode.")
        elif trigger_count >= 0 or trigger_count <= 16000000:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Event_Count"]\
                = int(trigger_count)
        else:
            sys.exit("Trigger Count must be between 0 and 16 Million.")

    def set_delay_trigger_delay_time(self, delay_time: float):
        """Sets the delay for a Delay By Time trigger event., which will be
        sent to the device the nexttime that send_all_settings is used"""
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "DEL":
            sys.exit("This setting can only be set in DELay Trigger Mode.")
        elif self.Settings["GeneralSettings"]["Trigger_Delay_Mode"] != "TDEL":
            sys.exit("This setting can only be set in Delay by Time Mode.")
        elif delay_time > 1e-8 or delay_time < 10:
            self.New_Settings["GeneralSettings"]["Trigger_Delay_Time"] = \
                float(delay_time)
        else:
            sys.exit("Trigger Delay Time must be between 10ns and 10s.")

    def set_edge_trigger_source(self, trigger_source: str):
        """Selects the source for edge mode triggering, which will be sent to
        the device the nexttime that send_all_settings is used"""
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "EDGE":
            sys.exit("This setting can only be set in EDGE Trigger Mode.")
        elif trigger_source in self.Analog_Channels:
            self.New_Settings["GeneralSettings"]["Trigger_Edge_Source"] = \
                "CHAN{}".format(trigger_source)
        else:
            sources = None
            for key in self.Analog_Channels:
                if sources:
                    sources = str(key)
                else:
                    sources = "{},{}".format(sources, str(key))
            sys.exit(
                "Trigger source must be one of the following: \
                    {}".format(sources))

    def set_edge_trigger_edge(self, trigger_edge: str):
        """Sets the slope of the trigger source previously selected.
        Trigger Source must be predefined.
        This will be sent to the device the nexttime that send_all_settings is
        used"""
        trigger_edge = trigger_edge.upper
        if self.Settings["GeneralSettings"]["Trigger_Mode"] != "EDGE":
            sys.exit("This setting can only be set in EDGE Trigger Mode.")
        elif trigger_edge in self.Trigger_Edge:
            self.New_Settings["GeneralSettings"]["Trigger_Edge_Edge"] = \
                trigger_edge
        else:
            edges = None
            for key in self.Trigger_Edge:
                if edges:
                    edges = str(key)
                else:
                    edges = "{},{}".format(edges, str(key))
            sys.exit("Trigger edge must be one of the following: {}".format(
                self.Trigger_Edge))

    def set_trigger_level(self, level: float):
        """Specifies the trigger level on the specified channel for the trigger
        source. Only one trigger level is stored in the oscilloscope for each
        channel.
        Trigger Source must be predefined.
        This will be sent to the device the nexttime that send_all_settings is
        used"""
        # TODO Can set a limit on trigger level in a future version
        self.New_Settings["GeneralSettings"]["Trigger_Level"] = float(level)

    def set_query_headers(self, headers: bool):
        """Defines whether query responses will include a command header.
        Must be off for expected numeric responses.
        This will be sent to the device the nexttime that send_all_settings is
        used"""
        self.New_Settings["GeneralSettings"]["Query_Headers"] = bool(headers)

    def set_acquisition_mode(self, acquire_mode: str):
        """Sets the sampling/acquisition mode of the oscope, which will be sent
        to the device the nexttime that send_all_settings is used"""
        acquire_mode = acquire_mode.upper
        if acquire_mode in self.Trigger_Mode:
            self.New_Settings["GeneralSettings"]["Acquisition_Mode"] = \
                acquire_mode
        else:
            modes = None
            for key in self.Acquisition_Mode:
                if modes:
                    modes = str(key)
                else:
                    modes = "{},{}".format(modes, str(key))
            sys.exit("Acquisition Mode must be one of the following: \
                     {}".format(self.Acquisition_Mode))

    def set_acquisition_complete(self, acquisition_percentage: float):
        """Sets the percentage of time buckets to be filled for the aquisition
        to be considered complete.
        This will be sent to the device the nexttime that send_all_settings is
        used"""
        if acquisition_percentage < 0 or acquisition_percentage > 100:
            sys.exit("Acquisition completion criteria must be entered as a \
                     percentage.")
        else:
            self.New_Settings["GeneralSettings"]["Acquisition_Complete"] = \
                float(acquisition_percentage)

    def set_data_source(self, data_source: str):
        """Sets channel that the data will be recorded from, which will be sent
        to the device the nexttime that send_all_settings is used"""
        # TODO handle all other data sources
        if data_source in self.Analog_Channels:
            self.New_Settings["GeneralSettings"]["Data_Source"] = \
                "CHAN{}".format(data_source)
        else:
            sources = None
            for key in self.Analog_Channels:
                if sources:
                    sources = str(key)
                else:
                    sources = "{},{}".format(sources, str(key))
            sys.exit("Data source must be one of the following analog \
                     channels: {}".format(self.Analog_Channels))

    def set_acquisition_count(self, acquire_count: int):
        """Sets how many data values are to be averaged per time bucket, which
        will be sent to the device the nexttime that send_all_settings is
        used"""
        # TODO Can set a limit on values needed to be averaged per time bucket
        # in a future version
        self.New_Settings["GeneralSettings"]["Acquisition_Count"] = \
            int(acquire_count)

    def set_acquisition_points(self, acquisition_points: int):
        """Sets the requested analog memory depth for an acquisition, which
        will be sent to the device the nexttime that send_all_settings is
        used"""
        # TODO will need to test how this actually works
        # TODO Can set a limit on points of memory depth to be used in a future
        # version
        self.New_Settings["GeneralSettings"]["Acquisition_Points"] = \
            int(acquisition_points)

    # endregion

    # Basic Functions
    # region

    def send_single(self):
        """The :SINGle command causes the oscilloscope to make a single
        acquisition when the next trigger event occurs."""
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_Single"))

    def send_run(self):
        """The :RUN command starts the oscilloscope running. When the
        oscilloscope is running, it acquires waveform data according to its
        current settings. Acquisition runs repetitively until the oscilloscope
        receives a :STOP command."""
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_Run"))

    def send_stop(self):
        """The :STOP command causes the oscilloscope to stop acquiring data. To
        restart the acquisition, use the :RUN or :SINGle command."""
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_Stop"))

    def send_autoscale(self):
        """Causes the oscilloscope to evaluate all input waveforms and find the
        optimum conditions for displaying the waveform. It searches each of the
        channels for input waveforms and shuts off channels where no waveform
        is found. It adjusts the vertical gain and offset for each channel that
        has a waveform and sets the time."""
        current_timeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_Autoscale"))
        self.Device.settimeout(current_timeout)

    # endregion

    # Channel Settings
    # region

    def send_define_yaxis_units(self, channel: int = 1, unit: str = "VOLT"):
        """Sets a channel to use the specified units for the y-axis."""
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(
                self.Analog_Channels))
        unit = unit.upper
        if unit not in self.Yaxis_Units:
            sys.exit("Units must be one of the following: {}".format(
                self.Yaxis_Units))
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_DefineYaxisUnits'))

    def send_define_reference_level(self, channel: int = 1,
                                    ref_level: float = 0):
        """Sets a channel to a specified reference level, vertical units and
        scale must be pre-defined."""
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(
                self.Analog_Channels))
        if ref_level <= -20 or ref_level >= 20:
            sys.exit("Reference Level must be within Scope limits")
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_DefineReferenceLevel'))

    def send_define_vertical_scale(self, channel: int = 1,
                                   vertical_scale: float = 0.5):
        """Sets a channel's vertical scale, or units per division, to a
        specified value, vertical units must be pre-defined."""
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(
                self.Analog_Channels))
        if vertical_scale < 0:
            sys.exit("Vertical units per division must be greater than zero")
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_DefineVerticalScale'))

    def send_define_vertical_range(self, channel: int = 1,
                                   vert_range: float = 10):
        """Sets the full scale vertical range of a specified channel to a
        specified value,vertical units must be pre-defined."""
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(
                self.Analog_Channels))
        if vert_range > 10000:
            sys.exit("Vertical range must be within reason.")
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_DefineVerticalRange'))

    def send_differential_mode(self, channel: int = 1,
                               diff_mode: bool = False):
        """Sets if a specified channel is in differential mode.
        Channels 1 & 3 may form a differential channel, setting only CHAN1 will
        do this.
        Channels 2 & 4 may form a differential channel, setting only CHAN2 will
        do this."""
        channel = str(channel)
        if channel not in self.Analog_Channels:
            sys.exit("Channel must be one of the following: {}".format(
                self.Analog_Channels))
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_DifferentialMode'))

    # endregion

    # Acquisition and Export
    # region

    def get_acquired_points(self):
        """Before you download data from the oscilloscope to your computer,
        always query the points value with the :WAVeform:POINts? query to
        determine the actual number of acquired points."""
        if self.Address != "TEST":
            self.log_info(self.ND.format("get_AcquiredPoints"))

    def send_display_data(self):
        """The :DISPlay:DATA? query returns information about the captured
        data."""
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_DisplayData"))

    def send_digitize(self, channels: str = "1"):
        """This command initializes the selected channels or functions, then
        acquires them according to the current oscilloscope settings. When all
        waveforms are completely acquired, the oscilloscope is stopped."""
        # TODO incorporate DIG,DIFF,COMM,POD
        selection = []
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Digitize'))
        else:
            channels = channels.replace(",", "")
            channels = channels.translate(
                {ord(i): None for i in string.whitespace})
            for element in range(len(channels)):
                if channels[element] not in self.Analog_Channels:
                    sys.exit("The digitization of only the 4x analog channels \
                             is currently supported.")
                elif len(channels) == 1:
                    selection[0] = "CHAN{}".format(channels)
                    break
                else:
                    selection.append("CHAN{}".format(channels[element]))
        return selection

    def get_data(self, channel: int = 0, datatype: str = ''):
        """Outputs waveform data to the computer over the remote interface. The
        data is copied from a waveform memory, function, channel, bus, pod, or
        digital channel previously specified with the :WAVeform:SOURce
        command."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_Data'))
        return self.Data

    def get_time_data(self):
        """Pulls x-axis info from scope, and returns 1D list of floats."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_TimeData'))
        else:
            self.TimingData = []
            origin = 0  # time value at first datapoint
            # time diff between consecutive datapoints
            increment = float("0.1")
            # defined by user before acquisition, this is an integer
            points = self.Settings["GeneralSettings"]["Acquisition_Points"]
            for element in range(points):
                self.TimingData.append(origin + (increment * element))
        return self.TimingData

    def measurement_info(self):
        """Sets header information for the save file"""
        info_text = '\n!Measurements:'
        for element in range(len(self.Measurements)):
            info_text = '\t' + self.Measurements[element]
        return info_text

    def create_data_text(self):
        """Creates table of Data for save file, excludes header info"""
        """Inputs self.Measurements as 1D list of strings and time as 1D list
        of floats. Outputs string that is a tab delimited table of time and
        measurement data. If the datatype is ascii, input self.Data as 1D list
        of comma delimited strings. Otherwise, data_format_conversion turns raw
        self.Data into an array."""
        for block in range(len(self.Data)):
            self.Data[block] = self.Data[block].translate(
                {ord(i): None for i in string.whitespace})
            self.Data[block] = self.Data[block].split(',')
            self.Data[block] = [i for i in self.Data[block] if i != '']
            self.Data[block] = np.array([float(i) for i in self.Data[block]])
        data_text = "\n\n!Time"
        if self.Settings["GeneralSettings"]["Data_Format"] != "ASC":
            # TODO handle oscope datatypes (use Data_Format_Bits)
            data_list = self.data_format_conversion(self.Data)
            self.TimingData = self.data_format_conversion(self.TimingData)
            # TODO handle oscope datatypes (use Data_Format_Bits)
        else:
            data_list = self.Data
        for measurement in self.Measurements:
            data_text = "{}\t{}".format(data_text, measurement)
        for timeElement in range(len(self.TimingData)):
            data_text = "{}\n{}".format(
                data_text, self.TimingData[timeElement])
            for dataElement in range(len(self.Measurements)):
                data_text = "{}\t{}".format(
                    data_text, data_list[dataElement][timeElement])
        return data_text

    # endregion
