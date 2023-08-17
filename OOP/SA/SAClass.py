import os
import string
import sys

import numpy as np

from OOP.BaseDevice import BaseDevice, string_to_list


class SAClass(BaseDevice):
    """Class that represents a Spectrum Analyzer"""

    def __init__(self, address: str, is_usb_connection=False):
        """Initializes device information and settings"""
        super().__init__(address, is_usb_connection)
        self.Measurements = []
        self.Frequencies = []
        self.Device_Type = "SA"
        self.Measurement_Source = [
            "RFIN", "RFIN2", "RFIO1",
            "RFIO2", "RFIO3", "RFIO4"
        ]
        self.Trigger_Source = [
            "EXT1", "EXT2", "IMM",
            "LINE", "FRAM", "RFB",
            "VID", "IF", "ALAR",
            "LAN", "IQM", "IDEM",
            "QDEM", "IINP", "QINP",
            "AIQM", "TV"
        ]
        self.Data_Format = {
            "ASC,0": 0,
            "INT,32": 32,
            "REAL,32": 32,
            "REAL,64": 64
        }
        self.Extra_Setting = {
            "Measurement_Source": "",
            "Sweep_Continuous": "",
            "Start_Frequency": "",
            "Stop_Frequency": "",
            "Center_Frequency": "",
            "Frequency_Span": "",
            "Points": "",
            "ResBW": "",
            "Reference_Level": "",  # TODO Ensure dynamic
            "Trigger_Source": "",
            "Trigger_Edge": "",
            "Trigger_Level": "",
            "Trigger_Delay": "",
            "Data_Format": ""
        }
        self.Settings = {
            "GeneralSettings": {
                "Measurement_Source": "RFIN",
                "Sweep_Continuous": False,
                "Start_Frequency": 1000000,
                "Stop_Frequency": 1700000,
                "Center_Frequency": 350000,
                "Frequency_Span": 700000,
                "Points": 8,
                "ResBW": 0,
                "Reference_Level": 0,
                "Trigger_Source": "",
                "Trigger_Edge": "",
                "Trigger_Level": 0,
                "Trigger_Delay": 0,
                "Data_Format": ""
            }
        }
        self.Settings_Format = {
            "Measurement_Source": str,
            "Sweep_Continuous": bool,
            "Start_Frequency": float,
            "Stop_Frequency": float,
            "Center_Frequency": float,
            "Frequency_Span": float,
            "Points": int,
            "ResBW": float,
            "Reference_Level": float,
            "Trigger_Source": str,
            "Trigger_Edge": str,
            "Trigger_Level": float,
            "Trigger_Delay": float,
            "Data_Format": str
        }
        self.Setting_Commands = {
            "Measurement_Source": "FEED:RF:PORT",
            "Sweep_Continuous": "INIT:CONT",
            "Start_Frequency": "FREQ:STAR",
            "Stop_Frequency": "FREQ:STOP",
            "Center_Frequency": "FREQ:CENT",
            "Frequency_Span": "FREQ:SPAN",
            "Points": "SWE:POIN",
            "ResBW": "BAND",
            "Reference_Level": "DISP:WIND:TRAC:Y:RLEV",  # TODO Ensure dynamic
            "Trigger_Source": "TRIG:SOUR",
            "Trigger_Edge": "TRIG:SLOP",
            "Trigger_Level": "TRIG:{}:LEV".format(
                self.Settings["Trigger_Source"]),  # TODO Ensure dynamic
            "Trigger_Delay": "TRIG:DEL",
            "Data_Format": "FORM"
        }

    def initialize_device(self):
        """Gets all values from the device and performs other initialization
        functions
        """
        self.initialize_logger(os.getcwd() + "/logs/", "SA")
        self.initialize_values()
        self.set_sweep_continuous(False)
        self.set_data_format("REAL,32")
        self.send_all_settings()

    # region

    def set_measurement_source(self, source: str):
        """Specifies the RF input port used, which will be sent to the device
        the next time that send_all_settings is used
        """
        source = source.upper()
        if source in self.Measurement_Source:
            self.New_Settings["GeneralSettings"]["Measurement_Source"] = source
        else:
            sources = None
            for key in self.Measurement_Source:
                if sources:
                    sources = str(key)
                else:
                    sources = "{},{}".format(sources, str(key))
            sys.exit("Measurement source must be one of the following: \
                     {}".format(self.Measurement_Source))

    def set_start_frequency(self, frequency: float):
        """Sets the frequency on the left side of the graticule, which will be
        sent to the device the next time that send_all_settings is used
        """
        if frequency <= -80 or frequency >= 26999999990:
            sys.exit("Start Frequency must be between -80 MHz and \
                     26.99999999 GHz.")
        else:
            self.New_Settings["GeneralSettings"]["Start_Frequency"] = \
                float(frequency)
            self.set_center_span()

    def set_stop_frequency(self, frequency: float):
        """Set the frequency on the right side of the graticule., which will be
        sent to the device the next time that send_all_settings is used
        """
        if frequency <= -79999999 or frequency >= 27000000000:
            sys.exit("Stop Frequency must be between -79.9999999 MHz and \
                     27 GHz.")
        else:
            self.New_Settings["GeneralSettings"]["Stop_Frequency"] = \
                float(frequency)
            self.set_center_span()

    def set_center_frequency(self, frequency: float):
        """Sets the center frequency., which will be sent to the device the
        next time that send_all_settings is used
        """
        if frequency <= -79999995 or frequency >= 26999999995:
            sys.exit(
                "Center Frequency must be between -79.999995 MHz and \
                    26.999999995 GHz.")
        else:
            self.New_Settings["GeneralSettings"]["Center_Frequency"] = \
                float(frequency)
            self.set_start_stop()

    def set_frequency_span(self, span: float):
        """Sets the frequency range symmetrically about the center frequency,
        which will be sent to the device the next time that send_all_settings
        is used
        """
        if span <= 10 or span >= 27000000000:
            sys.exit("Frequency Span must be between 10 Hz and 27 GHz.")
        else:
            self.New_Settings["GeneralSettings"]["Frequency_Span"] = \
                float(span)
            self.set_start_stop()

    def set_points(self, points: int):
        """Sets the number of points taken per sweep, which will be sent to the
        device the next time that send_all_settings is used
        """
        if points <= 1 or points >= 40001:
            sys.exit("Number of points must be between 1 and 40001.")
        else:
            self.New_Settings["GeneralSettings"]["Points"] = int(points)

    def set_res_bw(self, bw: float):
        """Sets the resolution bandwidth, which will be sent to the device the
        next time that send_all_settings is used
        """
        if bw < 1 or bw >= 8000000:
            sys.exit("The resolution bandwidth must be between 1 Hz and \
                     8 MHz.")
        else:
            self.New_Settings["GeneralSettings"]["ResBW"] = float(bw)

    def set_ref_level(self, power: float):
        """Specifies the amplitude represented by the top most graticule line,
        which will be sent to the device the next time that send_all_settings
        is used
        """
        if power <= -170 or power > 30:
            sys.exit("Reference level must be between -170 dBm and 30 dBm.")
        else:
            self.New_Settings["GeneralSettings"]["Reference_Level"] = \
                float(power)

    def set_trigger_source(self, trigger_source: str):
        """Sets the source for the trigger that controls the start of each new
        measurement, which will be sent to the device the next time that
        send_all_settings is used
        """
        trigger_source = trigger_source.upper
        if trigger_source in self.Trigger_Source:
            self.New_Settings["GeneralSettings"]["Trigger_Source"] = \
                trigger_source
        else:
            sources = None
            for key in self.Trigger_Source:
                if sources:
                    sources = str(key)
                else:
                    sources = "{},{}".format(sources, str(key))
            sys.exit("Trigger source must be one of the following: \
                     {}".format(self.Trigger_Source))

    def set_trigger_edge(self, trigger_edge: str):
        """Controls the trigger polarity. It is set positive to trigger on a
        rising edge and negative to trigger on a falling edge, which will be
        sent to the device the next time that send_all_settings is used
        """
        trigger_edge = trigger_edge.upper
        if trigger_edge == "POS" | "NEG":
            self.New_Settings["GeneralSettings"]["Trigger_Edge"] = trigger_edge
        else:
            sys.exit("Trigger Edge must be either POS or NEG.")

    def set_trigger_level(self, level: float):
        """Sets the power value where the trigger input will trigger a new
        sweep/measurement, which will be sent to the device the next time that
        send_all_settings is used
        """
        # TODO currently only supports EXT1/2 as trigger source
        if level < -5 or level > 5:
            sys.exit("Trigger level must be between -5 and 5.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Level"] = \
                float(level)

    def set_trigger_delay(self, delay: float = 0):
        """Controls a time delay during which the analyzer will wait to begin a
        sweep after meeting the trigger criteria. You can use negative delay to
        pre-trigger the instrument in time domain or FFT, but not in swept
        spans. This will be sent to the device the next time that
        send_all_settings is used
        """
        if delay < -0.15 or delay > 0.5:
            sys.exit("Trigger delay must be between -150 ms and 500 ms.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Delay"] = delay

    # endregion

    # Other Functions
    # region

    def get_data(self, channel: int = 0, datatype: str = ''):
        """Reads the current response values of the active data trace, reads or
        writes a memory trace, and reads or writes error terms.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_Data'))
        return self.Data

    def get_frequencies(self):
        """Generates a list of the measured frequencies based on the current
        settings
        """
        self.Frequencies = []
        for i in range(self.Settings["GeneralSettings"]["Points"]):
            np.array(self.Frequencies.append(
                self.Settings["GeneralSettings"]["Start_Frequency"] +
                (self.Settings["GeneralSettings"]["Frequency_Span"] /
                 (self.Settings["GeneralSettings"]["Points"] - 1)) * i))

    def get_max_amplitude(self):
        """Returns the frequency corresponding to the max amplitude and the max
        amplitude of the most recent data obtained
        """
        data_list = string_to_list(self.Data)
        amplitude = max(data_list)
        index = np.where(data_list == amplitude)[0]
        frequency = self.Frequencies[index[0]]
        self.log_info("({}, {})".format(frequency, amplitude))
        return frequency, amplitude

    def get_min_amplitude(self):
        """Returns the frequency corresponding to the min amplitude and the min
        amplitude of the most recent data obtained
        """
        data_list = string_to_list(self.Data)
        amplitude = min(data_list)
        index = np.where(data_list == amplitude)[0]
        frequency = self.Frequencies[index[0]]
        self.log_info("({}, {})".format(frequency, amplitude))
        return frequency, amplitude

    def get_amplitude_at_freq(self, frequency: float):
        """Returns the specified frequency and the corresponding amplitude of
        the most recent data obtained
        """
        data_list = string_to_list(self.Data)
        amplitude = np.interp(frequency, self.Frequencies, data_list)
        self.log_info("({}, {})".format(frequency, amplitude))
        return frequency, amplitude

    def get_peak_within_freq_range(self, min_freq: float, max_freq: float):
        """Returns the frequency corresponding to the peak amplitude and the
        peak amplitude of the most recent data obtained within a given
        frequency range
        """
        frequencies = []
        new_data = []
        data_list = string_to_list(self.Data)
        for element in range(len(self.Frequencies)):
            if (self.Frequencies[element] >= min_freq) and \
                    (self.Frequencies[element] <= max_freq):
                frequencies.append(self.Frequencies[element])
                new_data.append(data_list[element])
        amplitude = max(new_data)
        index = np.where(new_data == amplitude)[0]
        frequency = frequencies[index[0]]
        self.log_info("({}, {})".format(frequency, amplitude))
        return frequency, amplitude

    def measurement_info(self):
        """Sets header information for the save file
        """
        # self.Measurements must be defined in script calling library
        info_text = '\n!Measurements:'
        for Measurement in self.Measurements:
            info_text = "{}\t{}".format(info_text, Measurement)
        return info_text

    def create_data_text(self):
        """Creates table of Data for save file, excludes header info"""
        """Outputs string that is a tab delimited table of frequency and power
        data. If the datatype is ascii, input self.Data as a comma delimited
        string. Otherwise, data_format_conversion turns raw self.Data into an
        array.
        """
        self.get_frequencies()
        data_text = '\n\n!Frequency\tPower'
        if self.Settings["GeneralSettings"]["Data_Format"] != "ASC,0":
            data_list = self.data_format_conversion(self.Data)
        else:
            self.Data = self.Data.translate(
                {ord(i): None for i in string.whitespace})
            data_list = string_to_list(self.Data)
        for dataElement in range(len(data_list)):
            data_text = "{}\n{}\t{}".format(data_text,
                                            self.Frequencies[dataElement],
                                            data_list[dataElement])
        return data_text

# endregion
