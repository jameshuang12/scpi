import os

from OOP.BaseDevice import BaseDevice


class DCPSClass(BaseDevice):
    """Class that represents a DC Power Supply"""
    """Commands that do NOT need to be overwritten"""

    def __init__(self, address: str, is_usb_connection=False):
        """Initializes device information and settings"""
        super().__init__(address, is_usb_connection)
        self.VoltageOut = None
        self.CurrentOut = None
        self.Data = None
        self.New_Settings = None
        self.Settings = {
            "GeneralSettings": {
                "Power_On": [],
                "Voltage_Level": [],
                "Current_Limit": [],
                "Data_Format": ""
            }
        }
        self.Settings_Format = {
            "Power_On": bool,
            "Voltage_Level": float,
            "Current_Limit": float,
            "Data_Format": str
        }
        self.Device_Type = "DCPowerSupply"
        self.Data_Format = {
            "ASC": 0,
            "REAL": 32
        }
        self.Setting_Commands = {
            "Power_On": "OUTP:STAT {}, (@{})",
            "Voltage_Level": "SOUR:VOLT:LEV:IMM:AMPL {}, (@{})",
            "Current_Limit": "SOUR:CURR:LEV:IMM:AMPL {}, (@{})",
            "Data_Format": "FORM {}"
        }
        self.Extra_Setting = {
            "Power_On": "",
            "Voltage_Level": "",
            "Current_Limit": "",
            "Data_Format": ""
        }
        self.MeasurementType = []
        self.MeasuredOut = []
        self.Module_Names = []
        self.Module_Information = []

    # def get_all_settings(self):
    # # TODO Fix settings to new settings methodology
    #     for key in self.Settings:
    #         value = self.read(self.Setting_Commands[key])
    #         if self.Settings_Format[key] == str:
    #             value = value[:len(value) - 1]  # Removes /n
    #         elif self.Settings_Format[key] == bool:
    #             if value[0] == "1" or value.upper() == "ON":
    #                 value = True
    #             elif value[0] == "0" or value.upper() == "OFF":
    #                 value = False
    #             else:
    #                 print("{} ERROR".format(key))
    #         self.Settings[key] = self.Settings_Format[key](value)

    # def check_settings(self):
    #     # Returns True if same
    #     # TODO make able to handle all modules, If can be dynamic move to
    #     # SCPI_Device
    #     self.get_all_settings()
    #     for key in self.Settings:
    #         if self.Settings[key] != self.New_Settings[key]:
    #             return False
    #     return True

    # def send_all_settings(self):
    #     # TODO make able to handle all modules,
    #     # If can be dynamic move to SCPI_Device
    #     start_stop_diff = []
    #     center_span_diff = []
    #     for key in self.New_Settings:
    #         same = self.New_Settings[key] == self.Settings[key]
    #         if key == "Start_Frequency" and not same:
    #             start_stop_diff.append(key)
    #         elif key == "Stop_Frequency" and not same:
    #             start_stop_diff.append(key)
    #         elif key == "Center_Frequency" and not same:
    #             center_span_diff.append(key)
    #         elif key == "Frequency_Span":
    #             if not same:
    #                 center_span_diff.append(key)
    #             if len(start_stop_diff) > len(center_span_diff):
    #                 for diff in start_stop_diff:
    #                     self.write(self.Setting_Commands[diff],
    #                                self.New_Settings[diff])
    #             elif len(start_stop_diff) < len(center_span_diff):
    #                 for diff in center_span_diff:
    #                     self.write(
    #                         self.Setting_Commands[diff],
    #                         self.New_Settings[diff])
    #             elif len(start_stop_diff) == len(center_span_diff) and \
    #                 len(start_stop_diff) > 0:
    #                 for diff in center_span_diff:
    #                     self.write(
    #                         self.Setting_Commands[diff],
    #                         self.New_Settings[diff])
    #         elif not same:
    #             self.write(self.Setting_Commands[key],
    #                        self.New_Settings[key])
    #     if not self.check_settings():
    #          self.log_error("Device did not setup properly")

    # def initialize_values(self):
    #     self.Settings["GeneralSettings"]["Data_Format"] = self.read("FORM")

    # def init_module(self, module: int, voltage_level: float,
    #     # TODO Fix this to work with the new Settings format, if still needed
    #                 current_limit: float, module_name: str = ""):
    #     index = len(self.Module_Names)
    #     if index < module:
    #         while index < module:
    #             for key in self.Settings:
    #                 if key != "Data_Format":
    #                     self.Settings[key].append(None)
    #             self.VoltageOut.append(None)
    #             self.CurrentOut.append(None)
    #             self.Module_Names.append(None)
    #             self.Module_Information.append(None)
    #             index = index + 1
    #     self.Module_Names[module - 1] = module_name
    #     self.get_module_information(module)
    #     self.Settings["GeneralSettings"]["Power_On"][module - 1] = False
    #     self.Settings["GeneralSettings"]["Voltage_Level"][module -
    #                                                       1] = voltage_level
    #     self.Settings["GeneralSettings"]["Current_Limit"][module -
    #                                                       1] = current_limit
    #     self.New_Settings = {}
    #     for key in self.Settings:
    #         if key != "Data_Format":
    #             for value in range(len(self.Settings[key])):
    #                 if self.Settings[key][value] is not None:
    #                     self.New_Settings[key][value] = \
    #                         self.Settings_Format[key](
    #                             self.Settings[key][value])
    #         else:
    #             self.New_Settings[key] = self.Settings_Format[key](
    #                 self.Settings[key])

    def set_power_on(self, module: int, on: bool = True):
        # TODO Fix this to work with the new Settings format
        self.New_Settings["GeneralSettings"]["Power_On"][module - 1] = on

    def set_voltage_level(self, module: int, voltage: float):
        # TODO Fix this to work with the new Settings format
        self.New_Settings["GeneralSettings"]["Voltage_Level"][module - 1] = \
            voltage

    def set_current_limit(self, module: int, current: float):
        # TODO Fix this to work with the new Settings format
        self.New_Settings["GeneralSettings"]["Current_Limit"][module - 1] = \
            current

    "Commands that MAY need to be overwritten"

    def initialize_device(self):
        """Gets all values from the device and performs other initialization
        functions"""
        self.initialize_logger(os.getcwd() + "/logs/", "DCPS")
        # TODO Ensure this initializes the device properly
        self.send_reset()
        self.initialize_values()

    "Commands that DO need to be overwritten"

    def get_module_information(self, module: int):
        """Gets Model, Options, and Serial Number of specified module"""
        if self.Address != "TEST":
            self.log_info(self.ND.format("get_ModuleInformation"))
        self.Module_Information[module - 1] = {
            "Model": "Test{}".format(module),
            "Option": "Option",
            "Serial_Number": "SN{}".format(module)
        }

    def send_power_on(self, module: int, on: bool = True):
        """Initiates a sweep when the device is not in continuous sweep"""
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_power_on"))

    def get_voltage(self, modules: str):
        """This query initiates and triggers a measurement, and returns the
        average output voltage in volts."""
        data = ''
        data_types = {'FDAT', 'SDAT', 'MDAT', 'TSD'}
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_Data'))
        # else:
        #    Data = Default Data for Test based self.Points
        if data.upper() not in data_types:
            self.log_error('Format must be on of these:\n{}'.format(data_types))
        self.Data = data
        return data

    def get_current(self, modules: str):
        """This query initiates and triggers a measurement, and returns the
        average output current in amperes."""
        data = ''
        data_types = {'FDAT', 'SDAT', 'MDAT', 'TSD'}
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_AllData'))
        # else:
        #    Data = Default Data for Test based self.Points
        if data.upper() not in data_types:
            self.log_error('Format must be on of these:\n{}'.format(data_types))
        self.Data = data
        return data
