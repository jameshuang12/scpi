import os

from OOP.BaseDevice import BaseDevice


# File: Pulse Generator Class
# Author: Jacobs Engineerng Group
# Date: June 2023
# Copyright: Written by Jacobs Engineering Group with Jacobs proprietary and
# general purpose rights. All rights reserved. Look into copying for details.


class PGClass(BaseDevice):
    """ The device class that sets up the general and waveform settings.

    This class inherits all of the functions in the Scpidevice class that
    replicate some of the core functionality of the SCPI Class. The class is
    able to choose the waveform type that will generate a pulse. The class
    has a general setting for trigger actions and specific waveform setting
    for the waveform type that was chosen.

    # TODO JIRA ISSUE SDO-47
    TASK: Set up the leading/trailing edge time where they are able to
    change values in Settings once set to a new value in New_Settings.
    BACKGROUND INFO: The setting's command for leading/trailing both work
    as they were tested with the hardware. However, the values are not
    changing in Settings whenever send_all_settings is called.
    Currently, the 2 settings are commented out.
    """

    def __init__(self, address: str, is_usb_connection=False):
        """Initializes device information and settings"""
        super().__init__(address, is_usb_connection)
        self.device_type = "PG"

        self.waveform_list = [
            'SIN', 'SQU', 'RAMP',
            'TRI', 'NRAM', 'NOIS',
            'PRBS', 'DC', 'PULS'
        ]
        self.trigger_source = [
            'EXT', 'IMM', 'TIM', 'BUS'
        ]
        self.polarity = [
            'POS', 'NEG'
        ]

        self.output = False
        self.modulation = False
        self.sweep = False
        self.burst = False

        self.New_Settings = {}
        self.Settings_Format = None
        self.Settings = None
        self.Extra_Setting = None
        self.Setting_Commands = None

        self.Setting_Commands = {
            "Waveform_Type": "FUNC",
            "Voltage_Low": "VOLT:LOW",
            "Voltage_High": "VOLT:HIGH",
            "Frequency": "FREQ",
            # "Leading_Edge_Time" : "FUNC:PULS:TRAN:LEAD",
            # "Trailing_Edge_Time" : "FUNC:PULS:TRAN:TRA",
            "Edge_Time": "FUNC:PRBS:TRAN",
            "Duty_Cycle": "FUNC:SQU:DCYC",
            "Ramp_Symmetry": "FUNC:RAMP:SYMM",
            "Continuous_Waveform": "INIT:CONT",
            "Trigger_Source": "TRIG:SOUR",
            "Trigger_Delay": "TRIG:DEL",
            "Trigger_Output": "OUTP:TRIG",
            "Trigger_Polarity": "TRIG:SLOP",
            "Burst_Cycles": "BURS:NCYC",
            "Phase_Parameter": "SOUR:PHAS",
            "Pulse_Width": "FUNC:PULS:WIDT",
            "Bandwidth_Parameter": "FUNC:NOIS:BWID"
        }
        self.Extra_Setting = {
            "Waveform_Type": "",
            "Voltage_Low": "",
            "Voltage_High": "",
            "Frequency": "",
            # "Leading_Edge_Time" : "",
            # "Trailing_Edge_Time" : "",
            "Edge_Time": "",
            "Duty_Cycle": "",
            "Ramp_Symmetry": "",
            "Continuous_Waveform": "",
            "Trigger_Source": "",
            "Trigger_Delay": "",
            "Trigger_Output": "",
            "Trigger_Polarity": "",
            "Burst_Cycles": "",
            "Phase_Parameter": "",
            "Pulse_Width": "",
            "Bandwidth_Parameter": ""
        }
        self.Settings = {
            "GeneralSettings": {
                "Waveform_Type": '',
                "Continuous_Waveform": False,
                "Trigger_Source": '',
                "Trigger_Delay": 0.0,
                "Trigger_Output": False,
                "Trigger_Polarity": '',
                "Burst_Cycles": 0.0
            },
            "WaveformSettings": {
            }
        }
        self.SIN_Settings = {
            "Frequency": 0.0,
            "Voltage_Low": -0.05,
            "Voltage_High": 0.05,
            "Phase_Parameter": 0.0
        }
        self.SQU_Settings = {
            "Frequency": 0.0,
            "Voltage_Low": -0.05,
            "Voltage_High": 0.05,
            "Duty_Cycle": 0.0
        }
        self.RAMP_Settings = {
            "Frequency": 0.0,
            "Voltage_Low": -0.05,
            "Voltage_High": 0.05,
            "Ramp_Symmetry": 0.0
        }
        self.PULS_Settings = {
            "Frequency": 0.0,
            "Voltage_Low": -0.05,
            "Voltage_High": 0.05,
            # "Leading_Edge_Time" :0.0,
            # "Trailing_Edge_Time" :0.0,
            "Pulse_Width": 0.0
        }
        self.NOIS_Settings = {
            "Frequency": 0.0,
            "Voltage_Low": -0.05,
            "Voltage_High": 0.05,
            "Bandwidth_Parameter": 0.0
        }
        self.PRBS_Settings = {
            # Missing bit rate and PRBS data
            "Frequency": 0.0,
            "Voltage_Low": -0.05,
            "Voltage_High": 0.05,
            "Edge_Time": 0.0
        }
        self.DC_Settings = {
            "Voltage_Low": -0.05,
            "Voltage_High": 0.05
        }
        self.Waveform_Options = {
            # Will be called in set_Waveform_Type() to set up new waveform
            # the waveform will be added into the waveform settings.
            "SIN": self.SIN_Settings,
            "SQU": self.SQU_Settings,
            "RAMP": self.RAMP_Settings,
            "TRI": self.RAMP_Settings,
            "PULS": self.PULS_Settings,
            "NRAM": self.RAMP_Settings,
            "NOIS": self.NOIS_Settings,
            "PRBS": self.PRBS_Settings,
            "DC": self.DC_Settings
        }
        self.Settings_Format = {
            "Waveform_Type": str,
            "Voltage_Low": float,
            "Voltage_High": float,
            "Frequency": float,
            # "Leading_Edge_Time" : float,
            # "Trailing_Edge_Time" : float,
            "Edge_Time": float,
            "Duty_Cycle": float,
            "Continuous_Waveform": bool,
            "Trigger_Source": str,
            "Trigger_Delay": float,
            "Trigger_Output": bool,
            "Trigger_Polarity": str,
            "Burst_Cycles": float,
            "Phase_Parameter": float,
            "Pulse_Width": float,
            "Bandwidth_Parameter": float,
            "Ramp_Symmetry": float,
        }

        self.initialize_device()

    """  Waveform Setting Functions  """

    def set_voltage_low(self, voltage: float) -> None:
        """ 
        Purpose: Sets the new voltage value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Set the waveform's low voltage levels.
        Command: VOLTage:LOW <voltage>

        Default is -0.05 V or 50 mV
        Unit: Voltage must be in V
        Parameter: -5 V to +5 V
        """
        if voltage < -5 or voltage > 5:
            raise ValueError(f"{voltage} must be greater than or equal to"
                             " -5 V in voltage low.")
        else:
            self.New_Settings["WaveformSettings"]["Voltage_Low"] = voltage

    def set_voltage_high(self, voltage: float) -> None:
        """ 
        Purpose: Sets the new voltage value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Set the waveform's high voltage levels.
        Command: VOLTage:HIGH <voltage>

        Default: 0.05 V or -50 mV
        Unit: Voltage must be in V
        Parameter: -5 V to +5 V
        """
        low = self.New_Settings["WaveformSettings"]["Voltage_Low"]

        if voltage > 5 or voltage < -5 or voltage < low:
            raise ValueError(f"{voltage} must be less than or equal to"
                             " 5 V in voltage high.")
        else:
            self.New_Settings["WaveformSettings"]["Voltage_High"] = voltage

    def set_waveform_type(self, waveform: str) -> None:
        """ 
        Purpose: Sets the new waveform name to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Selects the output function
        Command: FUNCtion <function>

        Default: SIN
        Parameter: A list of waveform is added to ensure that waveform is valid
        """
        if waveform not in self.waveform_list or waveform == "":
            raise ValueError(f"{waveform} isn't in the waveform list, set to the "
                             "same waveform, or is an empty string in waveform type.")
        else:
            # Deletes the current waveform to set up the new waveform
            del self.New_Settings["WaveformSettings"]
            del self.Settings["WaveformSettings"]

            # Sets the waveform type in the new setting
            self.New_Settings["GeneralSettings"]["Waveform_Type"] = waveform
            # self.Settings["WaveformSettings"].update(
            #     self.Waveform_Options[waveform]
            # )
            # self.New_Settings["WaveformSettings"].update(
            #     self.Waveform_Options[waveform]
            # )
            # Sets the waveform setting to the current waveform type
            # in general settings by copying it. Gets all settings sets it up.
            self.New_Settings["WaveformSettings"] = \
                self.Waveform_Options[waveform].copy()
            self.Settings["WaveformSettings"] = \
                self.Waveform_Options[waveform].copy()
            # Updates the settings information
            self.get_all_settings()

    def set_frequency(self, frequency: float) -> None:
        """ 
        Purpose: Sets the new frequency value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the output frequency. This command is paired with
        FUNC:PULS:PER; whichever one is executed last overrides the other.
        Command: FREQuency <frequency>

        Default: 0 Hz
        Unit: frequency must be in Hz
        Parameter: 1 mul Hz to max instrument frequency
        """
        waveform = self.Settings["GeneralSettings"]["Waveform_Type"]
        if (frequency < 0 or (frequency > 200 and waveform == "RAMP") or
                (frequency > 1000000 and waveform == "PULS")):
            raise ValueError(f"{frequency} value must be greater than or equal"
                             " to 0 in frequency period. Another issue is"
                             " either ramp/pulse's frequency is greater than"
                             " expected in set frequency.")
        else:
            self.New_Settings["WaveformSettings"]["Frequency"] = frequency

    def set_leading_edge_time(self, leading: float) -> None:
        """ 
        Purpose: Sets the new leading value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the pulse edge time on the leading edge of a pulse.
        Command: FUNCtion:PULSe:TRANsition:LEADing <seconds>

        Default: 10 ns or 1e-10 s
        Unit: Leading must be in s
        Parameter: 8.4 ns to 1 mul s
        """
        if leading < 8.4e-9 or leading > 1e-6:
            raise ValueError(f"{leading} must be greater than 8.4 ns or"
                             " less than 1 microseconds in the leading edge time")
        else:
            self.New_Settings["WaveformSettings"]["Leading_Edge_Time"] \
                = leading

    def set_trailing_edge_time(self, trailing: float) -> None:
        """ 
        Purpose: Sets the new trailing value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the pulse edge time on the trailing edge of a pulse.
        Command: FUNCtion:PULSe:TRANsition:TRAiling <seconds>

        Default: 10 ns or 1e-10 s
        Unit: Trailing must be in s
        Parameter: 8.4 ns to 1 mul s
        """
        if trailing < 8.4e-9 or trailing > 1e-6:
            raise ValueError(f"{trailing} must be greater than 8.4 ns or less"
                             " than 1 microseconds in the trailing edge time")
        else:
            self.New_Settings["WaveformSettings"]["Trailing_Edge_Time"] \
                = trailing

    def set_edge_time(self, edge: float) -> None:
        """
        Purpose: Sets the new edge value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets PRBS transition edge time on both edges of a 
        PRBS transition.
        Command:FUNCtion:PRBS:TRANsition[:BOTH] <seconds>

        Default: 8.4 ns or 8.4e-9 s
        Unit: Edge must be in s
        Parameter: 8.4 ns to 1 mul s
        """
        if edge < 8.4e-9 or edge > 1e-6:
            raise ValueError(f"{edge} must be greater than 8.4 ns or"
                             " less than 1 microseconds in the edge time")
        else:
            self.New_Settings["WaveformSettings"]["Edge_Time"] = edge

    def set_duty_cycle(self, cycle: float) -> None:
        """ 
        Purpose: Sets the new cycle value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets duty cycle percentage for square wave
        Command: FUNCtion:SQUare:DCYCle <percent>

        Default: 30 %
        Unit: Cycle must be a percentage
        Parameter: 0.01 tp 99.99 percent
        """
        if cycle < 0 or cycle > 100:
            raise ValueError(f"{cycle} must be greater than 0 or less than"
                             " 100 in the duty cycle.")
        else:
            self.New_Settings["WaveformSettings"]["Duty_Cycle"] = cycle

    def set_ramp_symmetry(self, symmetry: float) -> None:
        """ 
        Purpose: Sets the new symmetry value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the symmetry percentage for ramp waves.
        Command: FUNCtion:RAMP:SYMMetry <percent>

        Default: 100 %
        Unit: Symmetry must be a percentage
        Parameter: 0 to 100 percent
        """
        if symmetry < 0 or symmetry > 100:
            raise ValueError(f"{symmetry} must be greater than 0"
                             + "or less than 100 in the ramp symmetry.")
        else:
            self.New_Settings["WaveformSettings"]["Ramp_Symmetry"] = symmetry

    def set_phase_parameter(self, phase: float) -> None:
        """ 
        Purpose: Sets the new phase value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets waveform's phase offset angle
        Command: PHASe <angle>

        Default: 0 degrees
        Unit: Phase must be in degrees
        Parameter -360 to +360 degrees: 
        """
        if phase < -360 or phase > 360:
            raise ValueError(f"{phase} is less than -360 or greater than"
                             + "360 degrees in phase parameter.")
        else:
            self.New_Settings["WaveformSettings"]["Phase_Parameter"] = phase

    def set_pulse_width(self, pulse_width: float) -> None:
        """ 
        Purpose: Sets the new pulse width value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        CAUTIONS from the manual:
        - The specified pulse width must also be less than the difference
        between the period and the edge time as shown low.

        - The instrument will adjust pulse edge time first and
        then limit pulse width as needed to accommodate the period.

        Pulse Width ≤ [Period - ((Leading + Trailing) * 0.625)]

        - The pulse width must also be greater than the total time of one edge.

        Pulse Width ≥ [(Leading + Trailing) * 0.625)]

        Behavior: Sets pulse width.
        Command: FUNCtion:PULSe:WIDTh <seconds>

        Default: 100 μs or 1e-6 s
        Unit: Pulse width must be in s
        Parameter: 16 ns to approx. 1,000,000 s
        """
        if (pulse_width < 1.6e-8) or (pulse_width > 1e6):
            raise ValueError(f"{pulse_width} must be greater than 16 ns"
                             " or less than 1 milisecond in pulse width")
        else:
            self.New_Settings["WaveformSettings"]["Pulse_Width"] = pulse_width

    def set_bandwidth_parameter(self, bandwidth: float) -> None:
        """ 
        Purpose: Sets the new bandwidth value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets bandwidth of noise function.
        Commmand: FUNCtion:NOISe:BANDwidth|BWIDth <bandwidth>

        Default: 100 kHz or 100000 Hz
        Unit: Bandwidth must be in Hz
        Parameter: 1 mHz to instrument's max frequency
        """
        if bandwidth < 1 or bandwidth > 20000000:
            raise ValueError(f"{bandwidth} must be greater than 1 or less"
                             " than the instrument's max frequency in"
                             " bandwidth parameter")
        else:
            self.New_Settings["WaveformSettings"]["Bandwidth_Parameter"] \
                = bandwidth

    """ General Setting Functions """

    def set_continuous_waveform(self, continous: bool) -> None:
        """ 
        Purpose: Sets continuous to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior:Specifies whether the trigger system for one or both channels
        (ALL) always returns to the "wait-for-trigger" state (ON) or remains 
        in the "idle" state (OFF), ignoring triggers until 
        INITiate:IMMediate is issued.
        Command: INITiate[1|2]:CONTinuous ON|1|OFF|0
        """
        self.New_Settings["GeneralSettings"]["Continuous_Waveform"] \
            = continous

    def set_trigger_source(self, source: str) -> None:
        """ 
        Purpose: Sets the new source value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Selects the trigger source for list, burst or sweep. 
        The instrument accepts an immediate or timed internal trigger, an
        external hardware trigger from the front-panel Ext Trig connector, 
        or a software (bus) trigger.
        Command: TRIGger[1|2]:SOURce IMMediate|EXTernal|TIMer|BUS

        Parameter: A list of trigger sources is added to ensure source is valid
        """
        if source not in self.trigger_source or source == "":
            raise ValueError(f"{source} is not in the sources list or"
                             + "is an empty string in the trigger source.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Source"] = source

    def set_trigger_delay(self, delay: float) -> None:
        """ 
        Purpose: Sets the new delay value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets trigger delay, (time from assertion of trigger 
        to occurrence of triggered event).
        Command: TRIGger[1|2]:DELay <seconds>

        Default: 0 s
        Unit: Delay must be in s
        Parameter: 0 to 1000 s
        """
        if delay < 0 or delay > 1000:
            raise ValueError(f"{delay} is greater than 1000 seconds or"
                             " less than 0 seconds in trigger delay.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Delay"] = delay

    def set_trigger_output(self, output: bool) -> None:
        """ 
        Purpose: Saves the new general settings of the trigger output.

        Behavior: Disables or enables the "trigger out" signal for 
        sweep and burst modes.
        Command: OUTPut:TRIGger[:STATe] ON|1|OFF|0
        """
        self.New_Settings["GeneralSettings"]["Trigger_Output"] = output

    def set_trigger_polarity(self, polarity: str) -> None:
        """ 
        Purpose: Sets the new polarity value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Selects whether the instrument uses the rising edge 
        or falling edge for the "trigger out" signal
        Command: OUTPut:TRIGger:SLOPe POSitive|NEGative

        Parameter: A list of polarity is added to ensure that polarity is valid
        """
        if polarity not in self.polarity or polarity == "":
            raise ValueError(f"{polarity} is not in the polarity list or"
                             " is an empty string in trigger polarity.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Polarity"] \
                = polarity

    def set_burst_cycles(self, cycle: float) -> None:
        """ 
        Purpose: Sets the new cycle value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the number of cycles to be output per burst
          (triggered burst mode only).
        Command: BURSt:NCYCles <num_cycles>

        Default is 1 cycle
        Unit: Cycle must be numerical
        Parameter: 1 to 100,000,000 cycles
        """
        if cycle < 1 or cycle > 1e8:
            raise ValueError(f"{cycle} is less than 1 or greater than"
                             " 100 million for burst cycles")
        else:
            self.New_Settings["GeneralSettings"]["Burst_Cycles"] = cycle

    """ Initialize/Parent Functions """

    def initialize_device(self):
        """ Initializes all values and sends settings directly to the hardware.
        """
        self.initialize_logger(os.getcwd() + "/logs/", "PG")
        self.initialize_values()
        self.send_all_settings()

    def send_pulse_output(self):
        """ Controls when the pulse gets sent.

        Operation will be overloaded by the same function in the manual class
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_pulse_output'))

    def send_modulation_output(self):
        """ Controls the modulation on turning it on or off.
        Will not enable modulation if sweep or bust is enabled.

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_modulation_output'))

    def send_sweep_output(self):
        """ Controls the sweep on turning it on or off.
        Will not enable sweep if modulation or bust is enabled.

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_sweep_output'))

    def send_burst_output(self):
        """ Controls the burst on turning it on or off.
        Will not enable burst if sweep or modulation is enabled.

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_burst_output'))

    def create_data_text(self, channel_name: str):
        """ Create a data text of all settings for the pulse generator.
        """
        data_text = "\n"
        for waveform_setting in self.New_Settings["WaveformSettings"]:
            waveform = self.New_Settings["WaveformSettings"][waveform_setting]
            data_text = f"{data_text}\n{waveform_setting}\t{waveform}"
        return data_text

    def print_settings(self):
        """ Prints out the general and waveform settings in the terminal.
        """
        self.log_info("General Settings for the Pulse Generator: "
                      + "\n Settings: "
                      + str(self.Settings["GeneralSettings"])
                      + "\n New_Settings: "
                      + str(self.New_Settings["GeneralSettings"]))

        if self.New_Settings["GeneralSettings"]["Waveform_Type"] != "":
            self.log_info("Waveform Settings for the Pulse Generator: "
                          + "\n Settings: "
                          + str(self.Settings["WaveformSettings"])
                          + "\n New_Settings: "
                          + str(self.New_Settings["WaveformSettings"]))
