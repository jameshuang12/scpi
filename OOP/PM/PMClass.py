import os

from OOP.BaseDevice import BaseDevice


# Files: Power Meter Class
# Author: Jacobs Engineering Group
# Date: June 2023
# Copyright: written by Jacobs Engineering Group with Jacobs proprietary and
# general purpose rights. all rights resevered. look into copying for details.


class PMClass(BaseDevice):
    """ The device class that sets up the general settings.

    The class inherits all of the functions in the Scpidevice class that
    replicates some of the core functionality of the SCPI Class.

    The device class mainly has functions that set up the settings for the
    device itself. The class also has parent functions for the manual class 
    that will be inherited by the children functions.

    The power meter helps determine settings to optimize performance.
    """

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.device_type = "PM"

        self.power_types = [
            'AC', 'REL',
            'DIFF', 'RAT'
        ]
        self.trigger_slopes = [
            'POS', 'NEG'
        ]
        self.activate_trigger = [
            'OFF', 'ON', 'ONCE'
        ]
        self.trigger_sources = [
            'IMM', 'EXT', 'HOLD', 'BUS',
            'INIT:IMM', 'INT1', 'INT2'
        ]
        self.data_formats = [
            "ASCii", "REAL"
        ]

        self.calibrate = False
        self.SParameters = []
        self.Stimulus = ""
        self.New_Settings = {}
        self.Settings_Format = None
        self.Settings = None
        self.Extra_Setting = None
        self.Setting_Commands = None

        self.Setting_Commands = {
            # TODO ERROR in testing : wrong format settings
            # NOTE: May need to add dynamic channel setting Ex. CONF{}:POW
            "Power_Type": "CONF{}:POW",
            "Trigger_Cycle": "INIT:CONT",
            # TODO ERROR in testing : settings error
            "Trigger_Slope": "TRIG:SEQ:SLOP",
            "Activate_Trigger": "TRIG:SEQ:LEV:AUTO",
            # TODO ERROR in testing : illegal parameter value
            "Trigger_Level": "TRIG:SEQ:LEV",
            "Trigger_Source": "TRIG:SOUR",
            "Trigger_Delay": "TRIG:SEQ:DEL",
            "Data_Format": "FORM:READ:DATA",
            "Start_Frequency": "FREQ:STAR",
            "Frequency_Sweep": "FREQ:STEP",
            "Stop_Frequency": "FREQ:STOP"
        }
        self.Extra_Setting = {
            "Power_Type": "",
            "Trigger_Cycle": "",
            "Trigger_Slope": "",
            "Activate_Trigger": "",
            "Trigger_Level": "",
            "Trigger_Source": "",
            "Trigger_Delay": "",
            "Data_Format": "",
            "Start_Frequency": "",
            "Frequency_Sweep": "",
            "Stop_Frequency": ""
        }
        self.Settings = {
            "GeneralSettings": {
                "Power_Type": "",
                "Trigger_Cycle": False,
                "Trigger_Slope": "",
                "Activate_Trigger": False,
                "Trigger_Level": 0,
                "Trigger_Source": "",
                "Trigger_Delay": 0,
                "Start_Frequency": 0,
                "Frequency_Sweep": 0,
                "Stop_Frequency": 0,
                "Data_Format": ""
            }
        }
        self.Settings_Format = {
            "Power_Type": str,
            "Trigger_Cycle": bool,
            "Trigger_Slope": str,
            "Activate_Trigger": bool,
            "Trigger_Level": float,
            "Trigger_Source": str,
            "Trigger_Delay": float,
            "Data_Format": str,
            "Start_Frequency": float,
            "Frequency_Sweep": float,
            "Stop_Frequency": float
        }

        self.initialize_device()

    def set_power_type(self, power: str) -> None:
        """ 
        Purpose: Sets the new power value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior:This command sets the expected power level of the measurement.
        Command: CONF:POW <type>

        Default: "AC"
        Parameter: A list of power type is added to ensure that power is valid
        """
        if power not in self.power_types or power == "":
            raise ValueError(f"{power} is not in the power list"
                             " or is an empty string in power list.")
        else:
            self.New_Settings["GeneralSettings"]["Power_Type"] = power

    def set_trigger_cycle(self, cycle: bool) -> None:
        """  
        Purpose: Sets cycle to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: This command sets the power meter for either a single trigger
        cycle or continuous trigger cycles
        A trigger cycle means that the power meter exits the wait for
        trigger state and starts a measurement.
        Command: INIT:CONT <"ON/OFF">
        """
        self.New_Settings["GeneralSettings"]["Trigger_Cycle"] = cycle

    def set_trigger_slope(self, slope: str) -> None:
        """ 
        Purpose: Sets the new slope value to the new settings that will
        be sent to the current settings, throw a value error if invalid value.

        Behavior: This command sets the trigger event to be recognized on the 
        falling edge of the triggering signal.
        Trigger type specifies whether a trigger event is recognized on the 
        rising or falling edge of a signal.
        Command: TRIG:SEQ:SLOP <"POS/NEG">

        Default: POS
        Parameter: A list of slopes is added to ensure that slope is valid
        """
        if slope == self.trigger_slopes or slope == "":
            raise ValueError(f"{slope} is not in the trigger slope list or"
                             " is an empty string in trigger slope.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Slope"] = slope

    def set_activate_trigger(self, trigger: bool) -> None:
        """ 
        Purpose: Sets trigger to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: This command disables or enables the automatic 
        setting of the trigger level. 
        Command: TRIG:SEQ:LEV:AUTO <"ON/OFF">
        """
        self.New_Settings["GeneralSettings"]["Activate_Trigger"] = trigger

    def set_trigger_level(self, level: float) -> None:
        """ 
        Purpose: Sets the new level value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: This command sets the power level for a trigger event
        Command: TRIG:SEQ:LEV <value>

        Default: 0 dBm 
        Unit: dBm
        Parameter: -40 to 20 dBm
        """
        if level < -40 or level > 20:
            raise ValueError(f"{level} has to be greater than -40 or less than 20"
                             " dBm in trigger level.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Level"] = level

    def set_trigger_source(self, source: str) -> None:
        """ 
        Purpose: Sets the new source value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: This command configures the trigger system to respond to the 
        specified source.This command only selects the trigger source. Use the 
        INITiate command to place the power meter in the wait for 
        trigger state.
        NOTE:
        - For dual channel power meters: if the leader is changed to IMM, BUS 
        or HOLD, error -221 “Settings Conflict” occurs. In such situations 
        the follower's TRIG:SOUR must be changed so that it is no longer
        a follower.

        - If the trigger source is changed to INT1, INT2 or EXT and SENS:SPEED 
        has value of 200, error - 221 “Settings Conflict” occurs.

        - If the trigger source is changed to INT1 or INT2 and SENS:DET:FUNC
          is set to AVERage, error -221 “Settings Conflict” occurs.

        - If the trigger source is set to INT1 or INT2 when 8480, N8480, 
        E4410, E9300 or E9320 (Average mode only) is connected, error -221 
        “Settings Conflict” occurs.

        - For dual channel power meters: if the adjacent sensor is in peak 
        mode, setting the trigger source of 8480, N8480, E4410, E9300 or E9320 
        (Average mode only) to EXTernal causes error -221 “Settings Conflict”.
        Command: TRIG:SOUR <source>

        Default: IMM
        Parameter: A list of sources is added to ensure that sources is valid
        """
        if source not in self.trigger_sources or source == "":
            raise ValueError(f"{source} is not in the trigger source list"
                             " or is an empty string.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Source"] = source

    def set_trigger_delay(self, delay: float) -> None:
        """ 
        Purpose: Sets the new delay value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: This command sets the delay between the recognition of a 
        trigger event and the start of a measurement.

        NOTE: Trigger delay is not applicable when the power meter is 
        set to power sweep mode or frequency sweep mode
        Command: 

        Default: 0 s
        Unit: seconsds
        Parameter: -1 to 1 s
        """
        if delay > 1 or delay < -1:
            raise ValueError(f"{delay} is out of range for trigger delay")
        else:
            self.New_Settings["GeneralSettings"]['Trigger_Delay'] = delay

    def set_data_format(self, data: str) -> None:
        """ 
        Purpose: Sets the new format value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: This command sets the data format for transferring numeric 
        information to either ASCii or REAL:

        -When the format type is ASCii, numeric data is output as ASCII bytes 
        in the <NR3> format.

        -When the format type is REAL, numeric data is output as IEEE 754
        64 bit floating point numbers in a definite length block. The result 
        is an 8 byte block per number. Each complete block is terminated by 
        a line feed character.

        Note: the N1912A power meter the same FORMat is used on both channels.
        Format data formatting is not affected by TRACe subsystem data 
        formatting.

        Default: ""
        Parameter: A list of data formats is added to ensure data is valid
        """
        if data not in self.data_formats or data == "":
            raise ValueError(f"{data} is an empty string or is not"
                             " the correct data format in data format.")
        else:
            self.New_Settings["GeneralSettings"]['Data_Format'] = data

    def set_start_frequency(self, start: float) -> None:
        """ 
        Purpose: Sets the new start value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: This command sets the start frequency of average or peak 
        frequency sweep. It must be used in conjunction with external trigger.

        If frequency sweep is disabled (frequency sweep step set to 0), 
        start frequency will be set but will not take effect.

        NOTE: This command is only applicable when used with E4410, N8480
        (excluding Option CFT), E9300. E9320 or N1920 sensor

        - When frequency sweep mode is configured with frequency step size 
        within its allowable range, 1 to 2048, the following applies:

        - If frequency stop point is greater than frequency start point, 
        the frequency range will be swept in an ascending order.

        - If frequency stop point is less than frequency start point, the 
        frequency range will be swept in a descending order.

        - If frequency stop point and frequency start point are equal, it is
        the same as power sweep mode
        Command: FREQuency[:CW|:FIXed]:STARt <value>

        Default: 50 MHz
        Unit: Hz
        Parameter: 1 kHz to 1000 GHz
        """
        stop_frequency = self.New_Settings["GeneralSettings"]["Stop_Frequency"]

        if start < 1e3 or start > 1e12:
            raise ValueError("Start frequency must be greater than 1 kHZ or"
                             f" less than 1000 GHz. Value: {start}")

        elif start > stop_frequency:
            self.set_stop_frequency(start)

        else:
            self.New_Settings["GeneralSettings"]["Start_Frequency"] = start
            self.set_center_span()

    def set_frequency_sweep(self, sweep: float) -> None:
        """
        Purpose: Sets the new sweep value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: This command sets the number of steps in average or peak
        frequency sweep. It must be used in conjunction with external trigger.

        The frequency sweep range will be equally divided by the frequency 
        step. If trace display is turned on, the measurement window will be
        restored to single numeric or analog depends on the number of
        measurement channel.

        Note: This command is only applicable when used with E4410, N8480
        (excluding Option CFT), E9300, E9320 or N1920 sensor.

        Frequency start, stop , and step are allowed to be set in any desirable
        sequence.Frequency step size calculated will be rounded to the nearest
        kHz with the minimum size of 1 kHz. When frequency range is less than
        frequency sweep step, the remaining steps will be repeated with the
        last frequency point.
        Command: FREQ:STEP <value>

        Default: 0 
        Unit: number
        Parameter: 0 to 2048
        """
        if sweep < 0 or sweep > 2048:
            raise ValueError(f"{sweep} must be greater than 0 or less than"
                             " 2048 in frequency sweep")
        else:
            self.New_Settings["GeneralSettings"]["Frequency_Sweep"] = sweep
            self.set_center_span()

    def set_stop_frequency(self, stop: float) -> None:
        """ 
        Purpose: Sets the new stop value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: This command sets the stop frequency of average or peak
        frequency sweep. It must be used in conjunction with external trigger.

        If frequency sweep is disabled (frequency sweep step set to 0), stop
        frequency will be set but will not take effect.

        NOTE: SENS:FREQ:STAR, SENS:FREQ:STOP and SENS:FREQ:STEP are allowed to
        be set in any desirable sequence.
        When frequency sweep mode is configured with frequency step size within
        its allowable range, 1 to 2048, the following applies:
        - If frequency stop point is greater than frequency start point, the
        frequency range will be sweep in an ascending order.
        - If frequency stop point is less than frequency start point, the
        frequency range will be sweep in a descending order.
        - If frequency stop point and frequency start point are equal, it is
        the same as power sweep mode
        Command: FREQ:STOP <value>

        Default is 50 Hz
        Unit: Hz
        Parameter: 1 kHz to 1000 GHz
        """
        start_freq = self.New_Settings['GeneralSettings']["Start_Frequency"]
        print(stop)
        if stop < 1e3 or stop > 1e12:
            raise ValueError("Stop Frequency must be greater than 1 kHz or"
                             " less than 1000 GHz for start frequency."
                             f" Value: {stop}")

        elif stop < start_freq:
            self.set_start_frequency(start_freq)

        else:
            self.New_Settings["GeneralSettings"]["Stop_Frequency"] = stop
            self.set_center_span()

    """ Initialize/Parent Functions  """

    def initialize_device(self):
        """ Initialize all vallues and sends settings directly to the hardware.
        """
        self.initialize_logger(os.getcwd() + "/logs/", "PM")
        self.initialize_values()
        self.send_all_settings()

    def send_trigger(self):
        """ A trigger is activated

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "Test":
            self.log_info(self.ND.format("send_trigger"))

    def send_calibration(self):
        """ Calibrates the power meter which performs internal adjustments

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_calibration'))

    def send_abort(self):
        """ Aborts a running measurement and resets the trigger system.

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_abort'))

    def get_data(self):
        """ Checks to ensure the code is not throwing any errors and gets
        the response values of the active data trace. Also reads or 
        writes a memory trace plus error terms. 

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_data'))

    def create_data_text(self, channel_name: str):
        """ Creates a data text for power meter
        """
        data_text = "\n"
        for setting in self.New_Settings["GeneralSettings"]:
            setting_name = self.New_Settings["GeneralSettings"][setting]
            data_text = f"{data_text}\n{setting_name}\t{setting}"

        return data_text

    def print_settings(self):
        """ prints out the general and specific settings in the terminal.
        """
        self.log_info("General Settings for the Signal Generator: "
                      + "\n Settings: "
                      + str(self.Settings["GeneralSettings"])
                      + "\n New_Settings: "
                      + str(self.New_Settings["GeneralSettings"]) + '\n')

        self.log_info("Specific Settings for the Signal Generator: "
                      + "\n Settings: "
                      + str(self.Settings["SpecificSettings"])
                      + "\n New_Settings: "
                      + str(self.New_Settings["SpecificSettings"]))
