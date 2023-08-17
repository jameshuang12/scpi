import os
import sys

from OOP.BaseDevice import BaseDevice


class VNAClass(BaseDevice):
    """Class that represents a Vector Network Analyzer"""

    def __init__(self, address: str, is_usb_connection=False):
        """Initializes device information and settings"""
        super().__init__(address, is_usb_connection)
        self.Setting_Commands = {
            "channel": "",
            "Sweep_Continuous": "INIT:CONT",
            "Points": "SWE:POIN",
            "Data_Format": "FORM:DATA",
            "Start_Frequency": "SENS{}:FREQ:STAR",
            "Stop_Frequency": "SENS{}:FREQ:STOP",
            "Center_Frequency": "SENS{}:FREQ:CENT",
            "Frequency_Span": "SENS{}:FREQ:SPAN",
            "ResBW": "SENS{}:BAND:RES",
            # TODO Ensure Source_Power_Level is dynamic
            "Source_Power_Level": "SOUR{}:POW",
            "Trigger_Source": "TRIG{}:SOUR",
            "Trigger_Edge": "TRIG{}:SLOP",
            # TODO Ensure I have all commands here
        }
        # TODO Ensure Source_Power_Level is dynamic
        self.Extra_Setting = {
            "channel": "",
            "Sweep_Continuous": "",
            "Start_Frequency": "",
            "Stop_Frequency": "",
            "Center_Frequency": "",
            "Frequency_Span": "",
            "Points": "",
            "ResBW": "",
            "Source_Power_Level": "",
            "Trigger_Source": "",
            "Trigger_Edge": "",
            "Data_Format": ""
        }
        self.Device_Type = "VNA"
        self.Data_Format = {
            "ASC,0": 0,
            "REAL,32": 32,
            "REAL,64": 64
        }
        self.SParameters = []
        self.channel_data = {
            "ASC,0": 0,
            "REAL,32": 32,
            "REAL,64": 64
        }
        self.Stimulus = ""
        self.Settings = {
            "GeneralSettings": {
                "Sweep_Continuous": False,
                "Points": 0,
                "Data_Format": ""
            },
        }
        self.Channel_Settings = {
            "channel": 1,
            # TODO UNCOMMENT AND FIX
            # "traces": [],
            # "SParameters": [],
            # "stimulus": [],
            "Start_Frequency": 0,
            "Stop_Frequency": 0,
            "Center_Frequency": 0,
            "Frequency_Span": 0,
            "ResBW": 0,
            "Source_Power_Level": -50,
            "Trigger_Source": "",
            "Trigger_Edge": ""
        }
        self.Settings_Format = {
            "channel": str,
            "Sweep_Continuous": bool,
            "Start_Frequency": float,
            "Stop_Frequency": float,
            "Center_Frequency": float,
            "Frequency_Span": float,
            "Points": int,
            "ResBW": float,
            "Source_Power_Level": float,
            "Trigger_Source": str,
            "Trigger_Edge": str,
            "Data_Format": str
        }
        self.Device_Type = "VNA"
        self.Data_Format = {
            "ASC,0": 0,
            "REAL,32": 32,
            "REAL,64": 64
        }

    def set_start_frequency(self, frequency: float):
        """Sets start frequency, which will be sent to the device the next time
        that send_all_settings is used"""
        if frequency < 0:
            sys.exit("Start Frequency must be greater than or equal to 0")
        else:
            self.New_Settings["GeneralSettings"]["Start_Frequency"] = float(
                frequency)
            self.set_center_span()

    def set_stop_frequency(self, frequency: float):
        """Sets stop frequency, which will be sent to the device the next time
        that send_all_settings is used"""
        if frequency < 0:
            sys.exit("Stop Frequency must be greater than or equal to 0")
        else:
            self.New_Settings["GeneralSettings"]["Stop_Frequency"] = float(
                frequency)
            self.set_center_span()

    def set_center_frequency(self, frequency: float):
        """Sets center frequency, which will be sent to the device the next
        time that send_all_settings is used"""
        if frequency <= 0:
            sys.exit("Center Frequency must be greater than0")
        else:
            self.New_Settings["GeneralSettings"]["Center_Frequency"] = float(
                frequency)
            self.set_start_stop()

    def set_frequency_span(self, frequency: float):
        """Sets frequency span, which will be sent to the device the next time
        that send_all_settings is used"""
        if frequency <= 0:
            sys.exit("Frequency Span must be greater than to 0")
        else:
            self.New_Settings["GeneralSettings"]["Frequency_Span"] = float(
                frequency)
            self.set_start_stop()

    def set_points(self, points: int):
        """Sets number of points in measurement, which will be sent to the
        device the next time that send_all_settings is used"""
        if points < 3:
            sys.exit("Number of points must be greater than or equal to 3")
        else:
            self.New_Settings["GeneralSettings"]["Points"] = int(points)

    def set_power(self, power: float):
        """Sets output power of the VNA, which will be sent to the device the
        next time that send_all_settings is used"""
        if power <= -50 or power > 27:
            sys.exit("Power level must be greater than or equal to -50 but \
                     less than 27")
        else:
            self.New_Settings["GeneralSettings"]["Source_Power_Level"] = float(
                power)

    def set_res_bw(self, bw: float):
        """Sets resolution bandwidth, which will be sent to the device the next
        time that send_all_settings is used"""
        # TODO Can add feature that specifies allowed Bandwidths
        if bw <= 0:
            sys.exit("Bandwidth must be greater than 0")
        else:
            self.New_Settings["GeneralSettings"]["ResBW"] = float(bw)

    def set_trigger_source(self, trigger_source: str):
        """Sets trigger source, which will be sent to the device the next time
        that send_all_settings is used"""
        # TODO Can add feature that specifies allowed Trigger Sources
        self.New_Settings["GeneralSettings"]["Trigger_Source"] = trigger_source

    def set_trigger_edge(self, trigger_edge: str):
        """Sets Trigger Edge, which will be sent to the device the next time
        that send_all_settings is used"""
        # TODO Can add feature that specifies allowed Trigger Sources
        self.New_Settings["GeneralSettings"]["Trigger_Edge"] = trigger_edge

    def measurement_info(self):
        """Sets header information for the save file"""
        info_text = '\n!Measurements:'
        for Measurement in self.SParameters:
            info_text = "{}\t{}".format(info_text, Measurement)
        return info_text

    def create_extension(self, channel_name: str):
        # TODO make this actually check the SParameters to ensure that
        # the correct number of ports are used
        ports = len(self.Settings[channel_name]["SParameters"]) ** 0.5
        if ports == ports.__floor__():
            return f"s{ports}p"
        return "txt"

    def create_data_text(self, channel_name: str):
        """Creates table of Data for save file, excludes header info"""
        data_text = '\n\n!Frequency'
        index = 0
        if self.Settings["GeneralSettings"]["Data_Format"] != "ASC,0":
            data_list = self.data_format_conversion(self.Data)
            freq_list = self.data_format_conversion(self.Stimulus)
        else:
            data_list = self.Data.split(',')
            data_list = [float(i) for i in data_list]
            freq_list = self.Stimulus.split(',')
            freq_list = [float(i) for i in freq_list]
        for Measurement in self.SParameters:
            data_text = "{}\t{}(real)\t{}(imaginary)".format(
                data_text, Measurement, Measurement)
        for frequency in freq_list:
            data_text = "{}\n{}".format(data_text, frequency)
            for _ in self.SParameters:
                data_text = "{}\t{}\t{}".format(
                    data_text, data_list[index], data_list[index + 1])
                index = index + 2
        return data_text

    "Commands that MAY need to be overwritten"

    def initialize_device(self):
        """Gets all values from the device and performs other initialization
        functions
        """
        self.initialize_logger(os.getcwd() + "/logs/", "VNA")
        # self.get_channels()
        # self.get_traces()
        self.initialize_logger(os.getcwd() + "/logs/", "VNA")
        self.initialize_values()
        self.set_sweep_continuous(False)
        self.set_data_format("ASC,0")
        self.send_all_settings()

    "Commands that DO need to be overwritten"

    def get_data(self, channel_name: str, datatype: str = 'SDAT'):
        """Reads the current response values of the active data trace, reads or
        writes a memory trace, and reads or writes error terms."""
        # TODO Find out the difference between get_Data and get_AllData
        # and get_SData
        data = ''
        data_types = {'FDAT', 'SDAT', 'MDAT', 'TSD'}
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_Data'))
        # else:
        #    Data = Default Data for Test based self.Points
        if datatype.upper() not in data_types:
            self.log_warning(
                'Format must be on of these:\n{}'.format(data_types))
        self.Data = data
        self.channel_data[channel_name] = data
        return data

    def get_all_data(self, channel_name: str, datatype: str = 'SDAT'):
        """Reads the current response values of all data and memory traces of
        the current test setup."""
        data = ''
        data_types = {'FDAT', 'SDAT', 'MDAT', 'TSD'}
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_AllData'))
        # else:
        #    Data = Default Data for Test based self.Points
        if datatype.upper() not in data_types:
            self.log_warning(
                'Format must be on of these:\n{}'.format(data_types))
        self.Data = data
        return data

    def get_s_data(self, channel_name: str):
        """Reads the current response values of all S-parameter data traces in
        channel no. <Ch>. If a full n-port system error correction (TOSM, TOM,
        TRL ...) is active in this channel, the command reads the full nxn
        Smatrix of the calibrated ports (there is no need to create or display
        the S-parameter traces). Use CALCulate<Ch>:DATA:CALL:CATalog? to query
        the available traces."""
        data = ''
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_SData'))
        # else:
        #    Data = Default Data for Test based self.Points
        self.Data = data
        self.channel_data[channel_name] = data
        return data

    def get_s_catalog(self, channel_name: str):
        """Returns all traces which are available for CALCulate<Ch>:DATA:CALL?
        in channel no. <Ch>."""
        catalog = ''
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_SCatalog'))
        # else:
        #    Catalog = Default Data for Test based self.Points
        return catalog

    def get_group_s_data(self, channel_name: str, datatype='SDAT'):
        """Reads the current response values of all S-parameters associated to
        a group of logical ports (S-parameter group). The S-parameter group
        must be created before using CALCulate<Ch>:PARameter:DEFine:SGRoup."""
        data = ''
        data_types = {'FDAT', 'SDAT', 'MDAT'}
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_GrouptSData'))
        # else:
        #    Data = Default Data for Test based self.Points
        if datatype.upper() not in data_types:
            self.log_warning(
                'Format must be on of these:\n{}'.format(data_types))
        self.Data = data
        self.channel_data[channel_name] = data
        return data

    def get_stimulus(self, channel_name: str):
        """Reads the stimulus values of the active data or memory trace."""
        stimulus = 0
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_Stimulus'))
        # else:
        #    Stimulus = Default Stimulus? for Test based self.Points
        return stimulus

    def send_display_format(self, display_format: str = 'MLOG'):
        """Defines how the measured result at any sweep point is post-processed
        and presented in the graphical display."""
        valid_format = {'MLIN', 'MLOG', 'PHAS', 'UPH', 'POL', 'SMIT', 'ISM',
                        'GDEL', 'REAL', 'IMAG', 'SWR', 'COMP', 'MAGN'}
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_DisplayFormat'))
        if display_format.upper() not in valid_format:
            self.log_warning(
                'Format must be on of these:\n{}'.format(valid_format))

    def get_catalog(self, channel_name: str):
        """Returns the trace names and measured quantities of all traces
        assigned to a particular channel."""
        catalog = ''
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_Catalog'))
        # else:
        #    Stimulus = Default Catalog for Test
        return catalog

    def send_define_trace(self, channel_name: str, trace_name: str = '',
                          measured_quantity: str = ''):
        """Creates a trace and assigns a channel number, a name and a measured
        quantity to it. The trace is not displayed. To display a trace defined
        via CALCulate<Ch>:PARameter:DEFine, a window must be created
        (DISPlay:WINDow<Wnd>[:STATe] ON) and the trace must be assigned to this
        window (DISPlay:WINDow<Wnd>:TRACe:FEED); see example below"""
        # if channel == 1:
        # channel = ''
        if trace_name == '' or measured_quantity == '':
            sys.exit('TraceName and MeasuredQuantity must not be blank')
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_DefineTrace'))

    def get_all_usb_cal_units(self):
        """Queries the names (USB addresses) of all connected calibration
        units."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_DefineTrace'))

    def send_delete_trace(self, channel_name: str, trace_name: str = ''):
        """Deletes a trace with a specified trace name and channel."""
        # if channel == 1:
        #       # channel = ''
        if trace_name == '':
            sys.exit('TraceName must not be blank')
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_delete_Trace'))

    def send_open_window(self, window: int, on: bool = True):
        """Creates or deletes a diagram area, identified by its area number
        <Wnd>."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_open_Window'))

    def send_assign_trace(self, window: int, trace_name: str):
        """Assigns an existing trace (CALCulate<Ch>:PARameter:SDEFine
        <Trace_Name>) to a diagram area <Wnd>, and displays the trace.
        Use DISPlay[:WINDow<Wnd>]:TRACe<WndTr>:FEED to assign the trace to a
        diagram area using a numeric suffix (e.g. in order to use the
        DISPlay[:WINDow<Wnd>]:TRACe<WndTr>:Y:OFFSet command)."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_assign_trace'))

    def send_trace_power_division(self, power_per_division: float,
                                  trace_name: str):
        """Sets the value between two grid lines (value “per division”) for the
        diagram area <Wnd>. When a new PDIVision value is entered, the current
        RLEVel is kept the same, while the top and bottom scaling is adjusted
        for the new PDIVision value."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Trace_Power_Division'))

    def send_trace_reference_level(self, reference_level: float,
                                   trace_name: str):
        """Sets the reference level (or reference value) for a particular
        displayed trace. Setting a new reference level does not affect the
        value of PDIVision. The trace can be referenced either by its number
        <WndTr> or by its name <trace_name>."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Trace_Reference_Level'))

    def send_trace_reference_position(self, reference_position: float,
                                      trace_name: str):
        """Sets the point on the y-axis to be used as the reference position as
        a percentage of the length of the y-axis. The reference position is the
        point on the y-axis which should equal the RLEVel."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Trace_Reference_Position'))

    def send_annotate_frequencies(self, on: bool = True):
        """Shows or hides all frequency stimulus values in the diagrams."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Annotate_Frequencies'))

    def send_annotate_channels(self, on: bool = True):
        """Shows or hides the channel list below the diagrams"""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Annotate_Channels'))

    def send_calbrate_vna(self, cal_kit_file: str = '', ports: str = "1,2"):
        """Initiates a one-port, two-port, three-port or four-port automatic
        calibration at arbitrary analyzer and cal unit ports."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Calbrate_VNA'))

    def send_calibrate_vna_settings(self, cal_type: str = 'FNP',
                                    cal_kit_file: str = ''):
        """Selects a calibration type and a cal unit characterization (cal kit
        file) for an automatic calibration with multiple port assignments."""
        cal_types = {'FNP', 'FOP', 'OPTP'}
        if cal_type.upper() not in cal_types:
            self.log_error(
                'Cal type must be on of these:\n{}'.format(cal_types))
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Calibrate_VNA_Settings'))

    def send_change_directory(self, directory_name: str = ''):
        """Changes the current directory for mass memory storage."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Change_Directory'))

    def send_create_directory(self, directory_name: str):
        """Creates a new subdirectory for mass memory storage in an existing
        directory."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Create_Directory'))

    def send_create_directory_path(self, directory_name: str):
        """Follows and creates directories as needed to create full path"""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Create_Directory_Path'))

    def send_store_configuration_data(self, file_name: str):
        """Stores the configuration data of the current setup to a specified
        setup file."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Store_Configuration_Data'))

    def get_channels(self):
        """ Returns the numbers and names of all channels in the current setup.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_channels'))

    def get_traces(self, channel_name: str):
        """Returns the numbers and names of all traces in the current setup.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_traces'))

    def send_configure_channel(self, name: str, on: bool = True):
        """Creates or deletes channel no. <Ch> and selects it as the active
        channel.
        """
        channels = []
        for key in self.Settings:
            if key != "GeneralSettings":
                channels.append(int(self.Settings[key]["channel"]))
        i = 1
        while i in channels:
            i += 1
        channel = 1
        self.Settings[name] = self.Channel_Settings.copy()
        self.Settings[name]["channel"] = channel
        self.write(f"CONF:CHAN{self.Settings[name]['channel']}", on)
        self.send_channel_rename(name, channel)
