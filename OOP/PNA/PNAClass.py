import os
import string
import sys

from OOP.BaseDevice import BaseDevice, string_to_list


class PNAClass(BaseDevice):
    """Class that represents a Phase Noise Analyzer"""

    def __init__(self, address: str, is_usb_connection=False):
        """Initializes device information and settings"""
        super().__init__(address, is_usb_connection)
        self.SpurData = []
        self.Range_Value = 1
        self.Device_Type = "PNA"
        self.Measurement_Types = [
            "BAS",
            "PNO"
        ]
        self.Sweep_Mode = [
            "MAN",
            "NORM",
            "FAST",
            "AVER"
        ]
        self.Trace_Mode = [
            "WRIT",
            "AVER",
            "MAXH",
            "MINH",
            "VIEW",
            "BLAN",
            "WRH"
        ]
        self.Data_Format = {
            "ASC,0": 0,
            "REAL,32": 32,
            "REAL,64": 64
        }
        self.Setting_Commands = {
            "Measurement_Select": "CONF:PNO:MEAS",
            "Sweep_Continuous": "INIT:CONT",
            "Carrier_Frequency": "FREQ:CENT",
            "Start_Frequency": "FREQ:STAR",
            "Stop_Frequency": "FREQ:STOP",
            "Trace_Mode": "DISP:TRAC:MODE",
            "Sweep_Count": "SWE:COUN",
            "Sweep_Mode": "SWE:MODE",
            "ResBW_Factor": "LIST:BWID:RES:RAT",
            "ResBW": "LIST:RANG{}:BWID".format(self.Range_Value),
            "XCorr_Factor": "SWE:XFAC",
            "XCorr": "LIST:RANG{}:XCO".format(self.Range_Value),
            "Data_Format": "FORM:DATA",
            "Frequency_Search": "ADJ:CONF:FREQ:AUT:STAT",
            "Frequency_Count": "ADJ:CONF:FREQ:COUN"
        }
        self.Extra_Setting = {
            "Measurement_Select": "",
            "Sweep_Continuous": "",
            "Carrier_Frequency": "",
            "Start_Frequency": "",
            "Stop_Frequency": "",
            "Trace_Mode": "",
            "Sweep_Count": "",
            "Sweep_Mode": "",
            "ResBW_Factor": "",
            "ResBW": "",
            "XCorr_Factor": "",
            "XCorr": "",
            "Data_Format": "",
            "Frequency_Search": "",
            "Frequency_Count": ""
        }
        self.Settings = {
            "GeneralSettings": {
                "Measurement_Select": "",
                "Sweep_Continuous": False,
                "Carrier_Frequency": 0,
                "Start_Frequency": 0,
                "Stop_Frequency": 0,
                "Trace_Mode": "",
                "Sweep_Count": 0,
                "Sweep_Mode": "",
                "ResBW_Factor": 0,
                "ResBW": 0,
                "XCorr_Factor": 0,
                "XCorr": 0,
                "Data_Format": "",
                "Frequency_Search": True,
                "Frequency_Count": True
            }
        }
        self.Settings_Format = {
            "Measurement_Select": str,
            "Sweep_Continuous": bool,
            "Carrier_Frequency": float,
            "Start_Frequency": float,
            "Stop_Frequency": float,
            "Trace_Mode": str,
            "Sweep_Count": int,
            "Sweep_Mode": str,
            "ResBW_Factor": float,
            "ResBW": float,
            "XCorr_Factor": float,
            "XCorr": float,
            "Data_Format": str,
            "Frequency_Search": bool,
            "Frequency_Count": bool
        }

    def initialize_device(self):
        """Gets all values from the device and performs other initialization
        functions"""
        self.initialize_logger(os.getcwd() + "/logs/", "PNA")
        self.initialize_values()
        self.set_measurement_select(self.Measurement_Types[1])
        self.set_sweep_continuous(False)
        self.set_data_format("ASC,0")
        self.send_all_settings()

    def set_measurement_select(self, measurement_select: str):
        """Sets the measurement to be made, which will be sent to the device
        the next time that send_all_settings is used"""
        # TODO support baseband measurements
        measurement_select = measurement_select.upper()
        if measurement_select in self.Measurement_Types:
            self.New_Settings["GeneralSettings"]["Measurement_Select"] = \
                measurement_select
        else:
            measurements = None
            for key in self.Measurement_Types:
                if measurements:
                    measurements = str(key)
                else:
                    measurements = "{},{}".format(measurements, str(key))
            sys.exit("Measurement type must be one of the following: \
                     {}".format(self.Measurement_Types))

    def set_carrier_frequency(self, frequency: float):
        """Sets center/carrier frequency, which will be sent to the device the
        next time that send_all_settings is used"""
        if frequency < 0:
            sys.exit("Carrier/center Frequency must be greater than or equal to \
                     0")
        else:
            self.New_Settings["GeneralSettings"]["Carrier_Frequency"] = float(
                frequency)

    def set_start_frequency(self, frequency: float):
        """Sets start frequency offset, which will be sent to the device the
        next time that send_all_settings is used"""
        if frequency < 0:
            sys.exit("Start Offset Frequency must be greater than or equal to \
                     0")
        else:
            self.New_Settings["GeneralSettings"]["Start_Frequency"] = float(
                frequency)

    def set_stop_frequency(self, frequency: float):
        """Sets stop frequency offset, which will be sent to the device the
        next time that send_all_settings is used"""
        if frequency < 0:
            sys.exit("Stop Offset Frequency must be greater than or equal to \
                     0")
        else:
            self.New_Settings["GeneralSettings"]["Stop_Frequency"] = \
                float(frequency)

    def set_trace_mode(self, trace_mode: str = "AVER"):
        """Sets trace mode of the half bandwidth table, which will be
        sent to the device the next time that send_all_settings is used"""
        if trace_mode not in self.Trace_Mode:
            sys.exit("Trace Mode must be one of the following: {}"
                     .format(self.Trace_Mode))
        else:
            self.New_Settings["GeneralSettings"]["Trace_Mode"] = trace_mode

    def set_sweep_count(self, count: int = 0):
        """Sets number of measurements that will be used to average traces,
        which will be sent to the device the next time that send_all_settings
        is used"""
        if count < 0 or count > 200000:
            sys.exit("Sweep Count must be between 0 and 200000.")
        else:
            self.New_Settings["GeneralSettings"]["Sweep_Count"] = int(count)

    def set_sweep_mode(self, sweep_mode: str = "NORM"):
        """Sets configuration mode of the half bandwidth table, which will be
        sent to the device the next time that send_all_settings is used"""
        if sweep_mode not in self.Sweep_Mode:
            sys.exit("Sweep Mode must be one of the following: {}"
                     .format(self.Sweep_Mode))
        else:
            self.New_Settings["GeneralSettings"]["Sweep_Mode"] = sweep_mode

    def set_res_bw(self, rbw: float, hd_range: int = 1):
        """Manually configure resolution bandwidth, which will be
        sent to the device the next time that send_all_settings is used"""
        if self.Settings["GeneralSettings"]["Sweep_Mode"] == "NORM":
            if rbw <= 0 or rbw > 30:
                sys.exit(
                    "Bandwidth factor must be greater than or equal to 0% \
                        and less than 30%.")
            else:
                self.New_Settings["GeneralSettings"]["ResBW_Factor"] = float(
                    rbw)
        elif self.Settings["GeneralSettings"]["Sweep_Mode"] == "MAN":
            if rbw <= 0:
                sys.exit("Bandwidth must be greater than zero.")
            elif hd_range <= 0:
                sys.exit("Half Decade Range must be selected when in Manual mode.")
            else:
                self.Range_Value = hd_range
                self.New_Settings["GeneralSettings"]["ResBW"] = float(rbw)
                self.Range_Value = 0
        else:
            sys.exit("Must be in Manual or Normal Sweep Mode to change \
                resolution bandwidth.")

    def set_x_corr(self, x_corr: float, hd_range: int = 1):
        """Manually configure number of cross correlation operations at each
        half decade, which will be sent to the device the next time that
        send_all_settings is used"""
        if self.Settings["GeneralSettings"]["Sweep_Mode"] == "NORM":
            if x_corr <= 0:
                sys.exit("Cross-correlation factor must be greater than zero.")
            else:
                self.New_Settings["GeneralSettings"]["XCorr_Factor"] = \
                    float(x_corr)
        elif self.Settings["GeneralSettings"]["Sweep_Mode"] == "MAN":
            if x_corr <= 0:
                sys.exit("Cross-correlation value must be greater than zero.")
            elif hd_range <= 0:
                sys.exit("Half Decade Range must be selected when in Manual mode.")
            else:
                self.Range_Value = hd_range
                self.New_Settings["GeneralSettings"]["XCorr_Factor"] = float(
                    x_corr)
                self.Range_Value = 0
        else:
            sys.exit("Must be in Manual or Normal Sweep Mode to change \
                number of cross correlations.")

    def set_frequency_search(self, frequency_search: bool = True):
        """This toggles auto carrier frequency search, which will be sent to
        the device the next time that send_all_settings is used"""
        # TODO Can add feature that toggles auto carrier frequency search
        self.New_Settings["GeneralSettings"]["Frequency_Search"] = \
            frequency_search

    def set_frequency_count(self, frequency_count: bool = True):
        """Toggles signal frequency counter and verification, which will
        be sent to the device the next time that send_all_settings is used"""
        if frequency_count is False and \
                self.Settings["GeneralSettings"]["Frequency_Search"] is True:
            sys.exit("Frequency Counter must be on when auto carrier \
            frequency search is on.")
        else:
            self.New_Settings["GeneralSettings"]["Frequency_Count"] = float(
                frequency_count)

    # Gets the currently set center/carrier frequency
    def get_carrier_freq(self):
        if self.Address != "TEST":
            self.log_info(self.ND.format("get_carrier_freq"))

    def get_spurs(self):
        """Queries the location and level of all spurs that have been detected.
        Returns the coordinates of detected spurs as a list of alternating
        frequency and power values."""
        if self.Address != "TEST":
            self.log_info(self.ND.format("get_Spurs"))
        self.SpurData = self.SpurData.translate(
            {ord(i): None for i in string.whitespace})
        self.SpurData = string_to_list(self.SpurData)
        spur_freq = self.SpurData[::2]
        self.log_info(max(spur_freq))
        spur_power = self.SpurData[1::2]
        self.log_info(max(spur_power))
        return self.SpurData

    def get_data(self, channel: int = 0, datatype: str = ''):
        """Returns the coordinates of the trace as alternating frequency and
        power values in a comma delimited string beginning at the nearest
        offset frequency."""
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_Data'))
        return self.Data

    def measurement_info(self):
        """Sets header information for the save file"""
        # TODO could use this to display spur information
        info_text = '\n!Measurements:\t' + \
            self.Settings["GeneralSettings"]["Measurement_Select"]
        return info_text

    def create_data_text(self):
        """Creates table of Data for save file, excludes header info"""
        """Formats trace data into tab delimited table."""
        data_text = '\n\n!Frequency\tNoise'
        if self.Settings["GeneralSettings"]["Data_Format"] != "ASC,0":
            self.Data = self.data_format_conversion(self.Data)
        else:
            self.Data = self.Data.translate(
                {ord(i): None for i in string.whitespace})
            self.Data = string_to_list(self.Data)
        for element in range(int(len(self.Data) / 2)):
            data_text = "{}\n{}\t{}".format(
                data_text, self.Data[element * 2], self.Data[element * 2 + 1])
        return data_text
