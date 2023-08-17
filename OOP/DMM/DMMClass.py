import os

from OOP.BaseDevice import BaseDevice


# File: Digital Multimeter Class
# Author: Jacobs Engineering Group
# Date: June 2023
# Copyright: Written by Jacobs Engineering Group with Jacobs proprietary and
# general purpose rights. All rights reserved. Look into copying for details.


class DMMClass(BaseDevice):
    """ The device class that sets up the general and specific settings. 

    This class inherits all of the functions in the BaseDevice and ScpiDevice 
    class that replicates some of the core functionality of both
    the BaseDevice class and ScpiDevice class.

    The device class mainly has functions that set up the settings for the
    device itself. The class also has parent functions for the manual class
    that will be inherited by the children functions.

    The class is able to read data and collect data for the user. The class
    gets the measurement type and level to compute. 
    """

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.device_type = "DMM"

        self.measurement_function = [
            "CAP", "CONT",
            "CURR:AC", "CURR:DC",
            "DIOD", "FREQ", "FRES",
            "PER", "RES", "TEMP",
            "VOLT", "VOLT:AC",
            "VOLAT:DC", "VOLTA:DC:RAT"
        ]
        self.data_format = {
            "ASC,9": 0,
            "REAL,64": 64
        }

        self.New_Settings = {}
        self.Settings_Format = None
        self.Settings = None
        self.Extra_Setting = None

        self.Setting_Commands = {
            "Measurement_Function": "FUNC",
            "Trigger_Level": "TRIG:LEV",
            "Continuous_Read": "TRIG:DEL:AUTO",
            "Data_Format": "FORM:DATA",
            # TODO Need to by dynamic commands Ex. {}:RANG:AUTO
            "Auto_Measurement_Level": "VOLT:RANG:AUTO",
            "Measurement_Range": "VOLT:RANG",
        }
        self.Extra_Setting = {
            "Measurement_Function": "",
            "Auto_Measurement_Level": "",
            "Trigger_Level": "",
            "Measurement_Range": "",
            "Continuous_Read": "",
            "Data_Format": ""
        }
        self.Settings = {
            "GeneralSettings": {
                "Measurement_Function": "",
                "Trigger_Level": 0,
                "Continuous_Read": True,
                "Data_Format": ""
            },
            "MeasurementSettings": {
                "Auto_Measurement_Level": True,
                "Measurement_Range": 0
            }
        }
        self.Settings_Format = {
            "Measurement_Function": str,
            "Auto_Measurement_Level": bool,
            "Trigger_Level": float,
            "Measurement_Range": float,
            "Continuous_Read": bool,
            "Data_Format": str
        }

        self.initialize_device()

    """  General Setting Functions  """

    def set_measurement_function(self, function: str) -> None:
        """ 
        Purpose: Sets the new function value to the new settings that will
        be sent to the current settings, throw a value error if invalid value.

        Behavior: Selects the measurement function 
        (all function-related measurement attributes are retained).
        Command: FUNCtion[:ON] "<function>

        Default: VOLT
        Parameter: A list of valid parameters are listed in
        self.measurement_function
        """
        if function not in self.measurement_function or function == "":
            raise ValueError(f"{function} is not in the measurement function "
                             "list or is an empty string in measurement function.")
        else:
            # Sets the new measurement function in the general settings
            self.New_Settings["GeneralSettings"]["Measurement_Function"] \
                = f'"{function}"'

            # Updates the commands to the new function value
            self.Setting_Commands.update(
                {
                    "Auto_Measurement_Level": f"{function}:RANG:AUTO",
                    "Measurement_Range": f"{function}:RANG"
                }
            )
            self.get_all_settings()

    def set_auto_measurement_level(self, auto: bool) -> None:
        """ 
        Purpose: Sets auto to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: Disables or enables the autoranging mode
        Command: [self.Settings["Measurement_Function"]:RANG:AUTO <option>

        Default: OFF
        Unit: auto must be a string
        """
        self.New_Settings["MeasurementSettings"]["Auto_Measurement_Level"] \
            = auto

    def set_trigger_level(self, level: float) -> None:
        """ 
        Purpose: Sets the new level value to the new settings that will
        be sent to the current settings, throw a value error if invalid value.

        Behavior: Sets the level on which a trigger occurs when level 
        triggering is enabled (TRIGger:SOURce set to INTernal)
        Command: TRIG:LEV <level>

        Default: 0.0
        Unit: level is in Volts
        Parameter: The minimum to the maximum voltage allowed on the device

        @param: level is the new value being added into New_Settings
        @return: +2.0E+01 
        """
        if level < 0:
            raise ValueError(
                f"{level} must be greater than 0 in trigger level.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Level"] = level

    def set_measurement_range(self, mrange: float) -> None:
        """ 
        Purpose: Sets the new range value to the new settings that will
        be sent to the current settings, throw a value error if invalid value.


        Behavior: Selects a fixed range for the measurements.
        Command: [self.Settings["Measurement_Function"]:RANGe <range>

        Default: AUTO
        Unit: level is based on measurement
        Parameter: All different for each measurement

        @param: range is the new value being added into New_Settings
        @return: range value
        """
        if mrange < 0:
            raise ValueError(
                f"{mrange} must be greater than 0 in measurement range.")
        else:
            self.New_Settings["MeasurementSettings"]["Measurement_Range"] \
                = mrange

    def set_continuous_read(self, read: bool) -> None:
        """
        Purpose: Sets read to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: Disables or enables automatic trigger delay. 
        If enabled,  the instrument determines the delay based on function,
        range, and integration time or bandwidth.
        Command: TRIGger:DELay:AUTO {ON|1|OFF|0}

        Default: ON
        Unit: read is a boolean
        @param: read is the new boolean being added into New_Settings
        @return: 0 (OFF) or 1 (ON)
        """
        self.New_Settings["GeneralSettings"]["Continuous_Read"] = read

    def set_data_format(self, data: str) -> None:
        """ 
        Purpose: Sets the new data value to the new settings that will
        be sent to the current settings, throw a value error if invalid value.

        Behavior: Specifies the data format to be either ASCII or REAL. 
        Affects the data format of the MEASure?, READ?, FETCh?,
        DATA:REMove? and R? commands only
        Command: FORMat[:DATA] <format>

        Default: ASC,9
        Unit: data must be a string
        Parameter: A list of valid parameters are listed in 
        self.data_format

        @param: data is the new vakue being added into New_Settings
        @return: data
        """
        if data not in self.data_format or data == "":
            raise ValueError(f"{data} is not in the data format list or "
                             "is an empty string in data format.")
        else:
            self.New_Settings["GeneralSettings"]["Data_Format"] = data

    """ Initialize/Parent Functions  """

    def initialize_device(self):
        """ Initializes all values and sends settings directly to the hardware.
        """
        self.initialize_logger(os.getcwd() + "/logs/", "DMM")
        self.initialize_values()
        self.show_okay_gui(
            title="Digital Multimeter Setup",
            message=" Make sure all cords are connected to the correct"
            " inputs in the digital multimeter before testing begins."
        )
        self.send_all_settings()

    def send_abort(self):
        """ Sends abort command which aborts all actions in the multimeter

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_abort"))

    def send_single_read(self):
        """ Sends a single read activation

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_single_read"))

    def get_data(self):
        """ Returns all of the data collected

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_data'))

    def measurement_info(self, channel_name: str):
        """ Creates a measurement info of all 
        settings for the digital multimeter.

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('measurement_info'))

    def create_data_text(self, channel_name: str):
        """ Creates a data text of all settings for the digital multimeter.
        """
        data_text = "\n"
        for measurement_setting in self.New_Settings["MeasurementSettings"]:
            function = self.New_Settings["MeasurementSettings"][measurement_setting]
            data_text = f"{data_text}\n{measurement_setting}\t{function}"
        return data_text

    def print_settings(self):
        """ Prints out the general and specific settings in the terminal.
        """
        self.log_info("General Settings for the Digital Multimeter: "
                      + "\n Settings: "
                      + str(self.Settings["GeneralSettings"])
                      + "\n New_Settings: "
                      + str(self.New_Settings["GeneralSettings"]) + "\n")

        self.log_info("Measurement Settings for the Digital Multimeter: "
                      + "\n Settings: "
                      + str(self.Settings["MeasurementSettings"])
                      + "\n New_Settings: "
                      + str(self.New_Settings["MeasurementSettings"]))
