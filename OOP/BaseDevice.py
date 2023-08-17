import sys
from tkinter import messagebox, Tk
from OOP.ScpiDevice import ScpiDevice
import numpy as np


def string_to_list(string_to_convert: str):
    """Changes a comma delimited string to a list"""
    string_list = string_to_convert.split(',')
    string_list = [i for i in string_list if i != '']
    string_list = np.array([float(i) for i in string_list])
    return string_list


class BaseDevice(ScpiDevice):
    """This class has default functions that most classes use"""

    def __init__(self, address: str, is_usb_connection=False):
        """Initializes some variables"""
        super().__init__(address, is_usb_connection)
        self.New_Settings = None
        self.Data = None
        self.channel_data = None
        self.Settings_Format = None
        self.Settings = None
        self.Extra_Setting = None
        self.Setting_Commands = None

    def initialize_values(self):
        """Gets the current settings from the device and makes them the values
        of Settings and New_Settings"""
        self.get_all_settings()
        self.New_Settings = {}
        for key in self.Settings:
            # Sets a the two settings up with New_Settings
            self.New_Settings[key] = self.Settings[key].copy()

    def set_sweep_continuous(self, continuous: bool):
        """Sets whether the measurement on the device will be continuous or not
        Continuous measurements usually means that timing will be an issue, as
        data will be collected at an unknown time. Continuous measurements will
        also slow down control of the device. This will be sent to the device
        the next time that send_all_settings is used"""
        self.New_Settings["GeneralSettings"]["Sweep_Continuous"] = continuous

    def save_channel(self, channel, data):
        """ Saves data to the specified channel in memory.
        To save to a file, use save_data()
        """
        self.Data = data
        self.channel_data[channel] = data

    def set_start_stop(self, channel: str = "GeneralSettings"):
        """Allows use of both start/stop frequency and center/span frequency
        control of the device. This can allow fewer commands from being sent to
        the device, therefore, speeding up control. This will be sent to the
        device the next time that send_all_settings is used"""
        self.New_Settings[channel]["Start_Frequency"] = \
            float(self.New_Settings[channel]["Center_Frequency"]) - \
            (float(self.New_Settings[channel]["Frequency_Span"]) / 2)
        self.New_Settings[channel]["Stop_Frequency"] = \
            float(self.New_Settings[channel]["Center_Frequency"]) + \
            (float(self.New_Settings[channel]["Frequency_Span"])
             / 2)

    def set_center_span(self, channel: str = "GeneralSettings"):
        """Allows use of both start/stop frequency and center/span frequency
        control of the device. This can allow fewer commands from being sent to
        the device, therefore, speeding up control. This will be sent to the
        device the next time that send_all_settings is used"""
        self.New_Settings[channel]["Center_Frequency"] = \
            (float(self.New_Settings[channel]["Stop_Frequency"]) +
             (float(self.New_Settings[channel]["Start_Frequency"])))\
            / 2
        self.New_Settings[channel]["Frequency_Span"] = \
            float(self.New_Settings[channel]["Stop_Frequency"]) - \
            float(self.New_Settings[channel]["Start_Frequency"])

    def set_start_frequency(self, frequency: float):
        """Sets start frequecy in New_Settings which will be sent to the device
        the next time that send_all_settings is used"""
        raise Exception("Not Implemented")

    def set_stop_frequency(self, frequency: float):
        """Sets stop frequecy in New_Settings which will be sent to the device
        the next time that send_all_settings is used"""
        raise Exception("Not Implemented")

    def set_center_frequency(self, frequency: float):
        """Sets center frequecy in New_Settings which will be sent to the
        device the next time that send_all_settings is used"""
        raise Exception("Not Implemented")

    def set_frequency_span(self, frequency: float):
        """Sets frequecy span in New_Settings which will be sent to the device
        the next time that send_all_settings is used"""
        raise Exception("Not Implemented")

    def set_points(self, points: int):
        """Sets number of points to be taken in a single measurement in
        New_Settings, which will be sent to the device the next time that
        send_all_settings is used"""
        raise Exception("Not Implemented")

    def set_res_bw(self, bw: float):
        """Sets the resolution bandwidth for the measurement in New_Settings,
        which will be sent to the device the next time that
        send_all_settings is used"""
        raise Exception("Not Implemented")

    def set_trigger_source(self, trigger_source: str):
        """Sets the trigger source for the trigger in New_Settings, which
        is used for synchronizing measurements to some sort of stimulus.
        This will be sent to the device the next time that
        send_all_settings is used"""
        raise Exception("Not Implemented")

    def set_trigger_edge(self, trigger_edge: str):
        """Sets the trigger edge for the trigger in New_Settings, which
        is used for synchronizing measurements to some sort of stimulus.
        This will be sent to the device the next time that
        send_all_settings is used"""
        raise Exception("Not Implemented")

    def set_data_format(self, data_format: str):
        """Sets the data format that the device will return. This usually
        just means the actual data and not setting values. This will be sent to
        the device the next time that send_all_settings is used"""
        data_format = data_format.upper()
        if data_format in self.Data_Format:
            self.New_Settings["GeneralSettings"]["Data_Format"] = data_format
        else:
            # TODO the below commented code does nothing, should it be deleted?
            # formats = None
            # data_format = self.Data_Format
            # for key in self.Data_Format:
            #     if formats:
            #         formats = str(key)
            #     else:
            #         formats = f"{formats},{key}"
            sys.exit(f"Format must be one of the following:{self.Data_Format}")

    def initialize_device(self):
        "Initializes the device to a known state that's ready tp be set up"
        raise Exception("Not Implemented")

    def send_preset(self):
        """Presets the Device to default values based on device preset
        settings"""
        current_timeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Preset'))
        self.Device.settimeout(current_timeout)

    def send_abort(self):
        """ Aborts a running measurement and resets the trigger system.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_Abort'))

    def send_initiate(self):
        """ Initiates a sweep when the device is not in continuous sweep
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_Initiate"))

    def get_data(self, channel: str = ""):
        """ Reads the current response values of the active data trace,
        reads or writes a memory trace, and reads or writes error terms.
        TODO Find the difference between get_Data, get_AllData, and get_SData
        """
        raise Exception("Not Implemented")

    def show_okay_gui(self, title=None, message=None):
        """ Creates an information message box
        """
        tk = Tk()
        tk.withdraw()
        messagebox.showinfo(title=title, message=message)

    def show_yes_no_gui(self, title=None, message=None):
        """ Creates a response message box
        """
        tk = Tk()
        tk.withdraw()
        return messagebox.askquestion(title=title, message=message)

    def show_warning_gui(self, title=None, message=None):
        """ Creates a warning message box
        """
        tk = Tk()
        tk.withdraw()
        messagebox.showwarning(title=title, message=message)
