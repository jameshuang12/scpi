import os

from OOP.BaseDevice import BaseDevice


# File: Signal Generator Class
# Author: Jacobs Engineerng Group
# Date: June 2023
# Copyright: Written by Jacobs Engineering Group with Jacobs proprietary and
# general purpose rights. All rights reserved. Look into copying for details.


class SGClass(BaseDevice):
    """ The device class that sets up the general and RF waveform settings.

    The class inherits all of the functions in the Scpidevice class that 
    replicate some of the core functionality of the SCPI Class.

    The device class mainly has functions that set up the settings for the
    device itself. The class also has parent functions for the
    manual class that will be inherited by the children functions. 

    The class offers signal characteristic and straightforward intuitive 
    operation. It's capable of making the signal generation efficent and quick.
    """

    def __init__(self, address: str, is_usb_connection=False):
        """Initializes device information and settings"""
        super().__init__(address, is_usb_connection)
        self.device_type = "SG"

        self.waveform_shape = [
            "SINE", "SQU", "TRI",
            "SAWT", "ISAW"
        ]
        self.sweep_mode = [
            "AUTO", "MAN", "STEP"
        ]
        self.sweep_space = [
            "LOG", "LIN"
        ]
        self.pulse_mode = [
            "SING", "DOUB", "PTR"
        ]
        self.trigger_mode = [
            "SING", "EXT", "AUTO"
        ]

        self.rf_output = False
        self.New_Settings = {}
        self.Settings_Format = None
        self.Settings = None
        self.Extra_Setting = None
        self.Setting_Commands = None

        self.Setting_Commands = {
            # NOTE: amplitide == level
            "Output_Amplitude": ":POW:POW",
            "Waveform_Shape": "LFO:SHAP",
            "Frequency": "FREQ",
            "Power_Control": "POW:SPC:CRAN",
            "Start_Frequency": "FREQ:STAR",
            "Stop_Frequency": "FREQ:STOP",
            "Center_Frequency": "FREQ:CENT",
            "Frequency_Span": "FREQ:SPAN",
            "Frequency_Sweep": "SWE:MODE",
            "Sweep_Space": "SWE:SPAC",
            "Space_Step_Width": "SWE:STEP",
            "LF_Generator_Output": "LFO",
            "LF_Frequency_Sweep": "SOUR:LFO:FREQ:MODE",
            "Amplitude_Modulation": "AM:STAT",
            "Frequency_Modulation": "FM:STAT",
            "Phase_Modulation": "PM:STAT",
            "Pulse_Mode": "PULM:MODE",
            "RF_Frequency_Sweep_Cycle": "TRIG:FSW:SOUR",
            "Pulse_Generator_State": "PGEN:STAT",
            "Screen_Saver_Mode": "DISP:PSAV"
        }
        self.Extra_Setting = {
            "LF_Generator_Output": "",
            "Output_Amplitude": "",
            "Waveform_Shape": "",
            "Frequency": "",
            "Power_Control": "",
            "Start_Frequency": "",
            "Stop_Frequency": "",
            "Center_Frequency": "",
            "Frequency_Span": "",
            "Frequency_Sweep": "",
            "Sweep_Space": "",
            "Space_Step_Width": "",
            "LF_Frequency_Sweep": "",
            "Amplitude_Modulation": "",
            "Frequency_Modulation": "",
            "Phase_Modulation": "",
            "Pulse_Mode": "",
            "RF_Frequency_Sweep_Cycle": "",
            "Pulse_Generator_State": "",
            "Screen_Saver_Mode": ""
        }
        self.Settings = {
            "GeneralSettings": {
                "Output_Amplitude": 0.0,
                "Waveform_Shape": "",
                "Frequency": 0,
                "Power_Control": 0,
                "Start_Frequency": 300e6,
                "Stop_Frequency": 300e6,
                "Center_Frequency": 0,
                "Frequency_Span": 0,
                "Frequency_Sweep": "",
                "Sweep_Space": "",
                "Space_Step_Width": 0,
                "Pulse_Mode": "",
                "RF_Frequency_Sweep_Cycle": "",
                "Pulse_Generator_State": False,
                "Screen_Saver_Mode": True
            },
            "ModGeneratorSettings": {
                "LF_Generator_Output": False,
                "LF_Frequency_Sweep": ""
            },
            "ModulationSettings": {
                "Amplitude_Modulation": False,
                "Frequency_Modulation": False,
                "Phase_Modulation": False
            }
        }
        self.Settings_Format = {
            "Output_Amplitude": float,
            "Waveform_Shape": str,
            "Frequency": float,
            "Power_Control": float,
            "Start_Frequency": float,
            "Stop_Frequency": float,
            "Center_Frequency": float,
            "Frequency_Span": float,
            "Frequency_Sweep": str,
            "Sweep_Space": str,
            "Space_Step_Width": float,
            "LF_Generator_Output": bool,
            "LF_Frequency_Sweep": str,
            "Amplitude_Modulation": bool,
            "Frequency_Modulation": bool,
            "Phase_Modulation": bool,
            "Pulse_Mode": str,
            "RF_Frequency_Sweep_Cycle": str,
            "Pulse_Generator_State": bool,
            "Screen_Saver_Mode": bool
        }

        self.initialize_device()

    """  ModGenerator Setting Functions  """

    def set_lf_generator_output(self, output: bool) -> None:
        """ 
        Purpose: Sets output to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: Activates/deactivates the LF output.
        Command: LFO <State>
        """
        self.New_Settings["ModGeneratorSettings"]["LF_Generator_Output"] \
            = output

    def set_lf_frequency_sweep(self, sweep: str) -> None:
        """ 
        Purpose: Sets the new sweep value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Selects the LF frequency sweep mode.
        Command: SOUR:LFO:FREQ:MODE <Mode>

        Default is CW
        Unit: The unit must be in a str
        """
        if sweep == '':
            raise ValueError(
                f"{sweep} is an empty string for LF frequency sweep.")
        else:
            self.New_Settings["ModGeneratorSettings"]['LF_Frequency_Sweep'] \
                = sweep

        """  Modulation Setting Functions  """

    def set_amplitude_modulation(self, amplitude: bool) -> None:
        """ 
        Purpose: Sets amplitude to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: Activates amplitude modulation.
        Command: AM:STATe <State>
        """
        self.New_Settings["ModulationSettings"]["Amplitude_Modulation"] \
            = amplitude

    def set_frequency_modulation(self, frequency: bool) -> None:
        """ 
        Purpose: Sets frequency to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: Activates frequency modulation.
        Note: Activation of FM deactivates phase modulation (PM).
        Command: FM:STATe <State>
        """
        self.New_Settings["ModulationSettings"]["Frequency_Modulation"] \
            = frequency

    def set_phase_modulation(self, phase: bool) -> None:
        """ Sets phase to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: Activates phase modulation.
        Note: Activation of PM deactivates frequency modulation (FM).
        Command: PM:STATe <State>
        """
        self.New_Settings["ModulationSettings"]["Phase_Modulation"] = phase

        """  General Setting Functions  """

    def set_output_amplitude(self, level: float) -> None:
        """ 
        Purpose: Sets the new level value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Standard Setting Ranges: 
        frequency = 100 kHz ≤ f ≤ 200 kHz <=> amplitude = -20 dBm to +4 dBm
        frequency = 200 kHz < f ≤ 300 kHz <=> amplitude = -20 dBm to +9 dBm 
        frequency = 300 kHz < f ≤ 1 MHz <=> amplitude = -20 dBm to +12 dBm
        frequency = 1 MHz < f ≤ 40 GHz <=> amplitude = -20 dBm to 3 dB above 
        max. specified output power

        Behavior: Sets the RF level of the RF output connector.
        Command: :POWer:POWer <Power>

        Default: 0 dBm
        Unit: Output must be in dBm
        Parameter: -20 to 12 dBm
        """
        if level < -20 or level > 12:
            raise ValueError(f"{level} is greater than 12 or less than -20 for"
                             " output amplitude. The value also may be out of range"
                             " due to the frequency value.")
        else:
            self.New_Settings["GeneralSettings"]['Output_Amplitude'] = level

    def set_waveform_shape(self, shape: str) -> None:
        """ 
        Purpose: Sets the new shape value to the new settings that will
        be sent to the current settings, throw a value error if invalid value


        Behavior: Selects the shape of the LF signal.
        Command: LFOutput:SHAPe <Shape>

        Parameter: A list of waveform is added to ensure that shape is valid
        """
        if shape not in self.waveform_shape or shape == "":
            raise ValueError(f"{shape} is not in the waveform list or"
                             " is an empty string in waveform shape.")
        else:
            self.New_Settings["GeneralSettings"]["Waveform_Shape"] = shape

    def set_frequency(self, frequency: float) -> None:
        """ 
        Purpose: Sets the new frequency value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Standard Setting Ranges: 
        frequency = 100 kHz ≤ f ≤ 200 kHz <=> amplitude = -20 dBm to +4 dBm
        frequency = 200 kHz < f ≤ 300 kHz <=> amplitude = -20 dBm to +9 dBm 
        frequency = 300 kHz < f ≤ 1 MHz <=> amplitude = -20 dBm to +12 dBm
        frequency = 1 MHz < f ≤ 40 GHz <=> amplitude = -20 dBm to 3 dB above 
        max. specified output power

        Behavior: Sets the frequency of the RF output signal.
        Command: FREQuency[:CW|FIXed] <Fixed

        Default: 1 GHz
        Unit: Frequency must be in Hz
        Parameter: Minimum to maximum device frequency
        """
        if frequency < 1e5 or frequency > 4e10:
            raise ValueError(f"{frequency} must be greater than 100 kHz or less than"
                             " 40 GHz for frequency.")
        else:
            self.New_Settings["GeneralSettings"]["Frequency"] = frequency

    def set_power_control(self, power: float) -> None:
        """ 
        Purpose: Sets the new power value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Defines the capture range of the power control system
        Command: POWer:SPC:CRANge <PowCntrlCRange>

        Default: 30 dB
        Unit: Power must be in dB
        Parameter: 0 to 50 dB
        """
        if power < 0 or power > 50:
            raise ValueError(f"{power} must be greater than 0 or"
                             " less than 50 for power control.")
        else:
            self.New_Settings["GeneralSettings"]["Power_Control"] = power

    def set_start_frequency(self, start: float) -> None:
        """ 
        Purpose: Sets the new start value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the start frequency for the RF sweep.
        Command: FREQ:STAR <Start>

        Default: 300 MHz
        Unit: Hz
        Parameter: 100 kHz to 40 Ghz
        """
        stop_frequency = self.New_Settings["GeneralSettings"]["Stop_Frequency"]

        if start < 1e5 or start > 4e10:
            raise ValueError("Start frequency must be greater than 100 kHZ or less"
                             f" than 40 GHz. Value: {start}")

        elif start > stop_frequency:
            self.set_stop_frequency(start)

        else:
            self.New_Settings["GeneralSettings"]["Start_Frequency"] = start
            self.set_center_span()

    def set_stop_frequency(self, stop: float) -> None:
        """ 
        Purpose: Sets the new stop value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the stop frequency for the RF sweep.
        Command: FREQ:STOP <Start>

        Default: 300 MHz
        Unit: Hz
        Parameter: 100 kHz to 40 GHz
        """
        start_freq = self.New_Settings['GeneralSettings']["Start_Frequency"]

        if stop < 1e5 or stop > 4e10:
            raise ValueError("Stop Frequency must be greater than 100 kHz or"
                             " less than 40 GHz for start frequency."
                             f" Value: {stop}")

        elif stop < start_freq:
            self.set_start_frequency(start_freq)

        else:
            self.New_Settings["GeneralSettings"]["Stop_Frequency"] = stop
            self.set_center_span()

    def set_center_frequency(self, center: float) -> None:
        """ 
        Purpose: Sets the new center value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the center frequency for the RF sweep.
        Command: FREQ:CENT <Start>

        Default: 300 MHz
        Unit: Hz
        Parameter: 100 kHz to 40 GHz
        """
        start = self.New_Settings["GeneralSettings"]["Start_Frequency"]
        stop = self.New_Settings["GeneralSettings"]["Stop_Frequency"]

        if center < 1e5 or center > 4e10:
            raise ValueError("Center Frequency must be greater than 100 kHz or less"
                             f" than 40 GHz. Value: {center}")

        elif center == ((start + stop) / 2):
            self.New_Settings["GeneralSettings"]['Center_Frequency'] = center
            self.set_frequency_span(stop - start)
            self.set_start_stop()

        else:
            self.set_frequency_span(stop - start)
            self.New_Settings["GeneralSettings"]["Center_Frequency"] = center

    def set_frequency_span(self, span: float) -> None:
        """ 
        Purpose: Sets the new span value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Determines the extent of the frequency sweep range.
        Command: FREQ:SPAN <Span>

        Default: 0 Hz
        Unit: Hz
        Parameter: span =  stop - start, start > stop is permitted
        """
        start = self.New_Settings["GeneralSettings"]["Start_Frequency"]
        stop = self.New_Settings['GeneralSettings']['Stop_Frequency']

        if span < 0 or span != (stop - start):
            raise ValueError("Frequency Span must be greater than 0 or the "
                             "span is not equal to stop frequency - start "
                             f"frequency. Start: {start}, Stop: {stop} "
                             f", Span: {span}")
        else:
            self.New_Settings["GeneralSettings"]["Frequency_Span"] = span
            self.set_start_stop()

    def set_frequency_sweep(self, sweep: str) -> None:
        """ 
        Purpose: Sets the new sweep value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the sweep mode
        Command: SWEep[:FREQuency]:MODE <Mode>

        Default: AUTO
        Parameter: A list of sweep mode is used to check if sweep is valid
        """
        if sweep not in self.sweep_mode or sweep == "":
            raise ValueError(f"{sweep} is not in the sweep mode list or"
                             " is an empty string for frequency sweep.")
        else:
            self.New_Settings["GeneralSettings"]["Frequency_Sweep"] = sweep

    def set_sweep_space(self, space: str) -> None:
        """ 
        Purpose: Sets the new space value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Selects the mode for the calculation of the frequency sweep 
        intervals. The frequency increases or decreases at each step
        Command: SWEep[:FREQuency]:SPACing <Spacing>

        Default: LIN
        A list of sweep space is used to check if space is valid
        """
        if space not in self.sweep_space or space == "":
            raise ValueError(f"{space} is not in the sweep space list or"
                             + " is an empty string for sweep space.")
        else:
            self.New_Settings["GeneralSettings"]["Sweep_Space"] = space

    def set_space_step_width(self, step: float) -> None:
        """ 
        Purpose: Sets the new step value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the step size for linear RF frequency sweep steps.
        Command: SWEep[:FREQuency]:STEP[:LINear] <Linear>

        Default is 1 MHz
        Unit: step must be in Hz
        Parameter: 100 to infinity kHz
        """
        if step < 1e5:
            raise ValueError(f"{step} value must be greater than 100 kHz"
                             " for space step width.")
        else:
            self.New_Settings["GeneralSettings"]["Space_Step_Width"] = step

    def set_pulse_mode(self, pulse: str) -> None:
        """ 
        Purpose: Sets the new pulse value to the new settings that will
        be sent to the current settings, throw a value error if invalid value.

        Behavior: Sets the mode of the pulse generator.
        Command: PULM:MODE <Mode>

        Default: SING
        Parameter: A list of pulse mode is used to check if pulse is valid
        """
        if pulse not in self.pulse_mode or pulse == "" or pulse not in self.Options:
            raise ValueError(f"{pulse} is not the pulse mode list, not "
                             "connected, or is an empty string in pulse mode.")
        else:
            self.New_Settings["GeneralSettings"]["Pulse_Mode"] = pulse

    def set_rf_frequency_sweep_cycle(self, sweep_cycle: str) -> None:
        """ 
        Purpose: Sets the new sweep cycle value to the new settings that will
        be sent to the current settings, throw a value error if invalid value

        Behavior: Sets the trigger source for the RF frequency sweep.
        Command: TRIGger<hw>:FSWeep:SOURce <Source>

        Parameter: A list of sweep cycle is used to check if sweepcycle is valid
        """
        if sweep_cycle not in self.trigger_mode or sweep_cycle == "":
            raise ValueError(f"{sweep_cycle} is not the trigger mode list or "
                             "is an empty string in RF frequency sweep cycle.")
        else:
            self.New_Settings["GeneralSettings"]["RF_Frequency_Sweep_Cycle"] \
                = sweep_cycle

    def set_pulse_generator_state(self, state: bool) -> None:
        """ 
        Purpose: Sets state to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: Activates/deactivates the output of the video/sync signal 
        at the [PULSE VIDEO] connector at the rear of the instrument.
        Command: PGENerator:STATe <State>
        """
        if self.New_Settings["GeneralSettings"]["Pulse_Mode"] == "":
            raise ValueError("Need to setup pulse mode first before turning on. Make"
                             " sure the pulse generator is connected before setting up")
        self.New_Settings["GeneralSettings"]["Pulse_Generator_State"] = state

    def set_screen_saver_mode(self, mode: bool) -> None:
        """ 
        Purpose: Sets mode to ON or OFF for the new settings that will
        be sent to the current settings

        Behavior: Activates the screen-save mode of the display.
        Command: DISPlay:PSAVe[:STATe] <State>
        """
        self.New_Settings["GeneralSettings"]["Screen_Saver_Mode"] = mode

    """  Initialize/Parent Functions  """

    def initialize_device(self):
        """ Initialize all vallues and sends settings directly to the hardware.
        """
        self.initialize_logger(os.getcwd() + "/logs/", "SG")
        self.initialize_values()
        self.send_all_settings()

    def send_rf_output(self):
        """ Controls when the pulse gets sent.

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format('send_rf_output'))

    def send_sweep(self):
        """ Activates the sweep

        Operation will be overloaded by the same function in the manual class. 
        """
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_sweep"))

    def send_data_file(self, filename: str):
        """ Able to use a data file to set the waveform settings. The function
        would be able to move a file to the signal generator from the 
        computer and select that designated file to execute.

        Operation will be overloaded by the same function in the manual class.
        """
        if self.Address != "TEST" or filename == "":
            self.log_info(self.ND.format('send_data_file'))

    def send_separator_file(self, filename: str):
        """ Selects the separator between the frequency 
        and level column of the ASCII table.

        Operation will be overlaoded by the same function in the manual class.
        """
        if self.Address != "TEST" or filename == "":
            self.log_info(self.ND.format("send_separator_file"))

    def send_calibration(self):
        """ Send a calibration to perform internal adjustments
        """
        if self.Address != "Test":
            self.log_info(self.ND.format("send_calibration"))

    def create_data_text(self, channel_name: str):
        """ Creates a data text of the two other settings for
        the signal generator.
        """
        data_text = "\n"
        for modgenerator_setting in self.New_Settings["ModGeneratorSettings"]:
            modgenerator = self.New_Settings["ModGeneratorSettings"][modgenerator_setting]
            data_text = f"{data_text}\n{modgenerator_setting}\t{modgenerator}"

        for modulation_setting in self.New_Settings["ModulationSettings"]:
            modulation = self.New_Settings["ModulationSettings"][modulation_setting]
            data_text = f"{data_text}\n{modulation_setting}\t{modulation}"
        return data_text

    def print_settings(self):
        """ Prints out the general, modulation generator, and
        modulation settings in the terminal.
        """
        self.log_info("General Settings for the Signal Generator: "
                      + "\n Settings: "
                      + str(self.Settings["GeneralSettings"])
                      + "\n New_Settings: "
                      + str(self.New_Settings["GeneralSettings"]) + "\n")

        self.log_info("Modulation Generator Settings for the Signal Generator: "
                      + "\n Settings: "
                      + str(self.Settings["ModGeneratorSettings"])
                      + "\n New_Settings: "
                      + str(self.New_Settings["ModGeneratorSettings"]) + "\n")

        self.log_info("Modulation Settings for the Signal Generator: "
                      + "\n Settings: "
                      + str(self.Settings["ModulationSettings"])
                      + "\n New_Settings: "
                      + str(self.New_Settings["ModulationSettings"]) + "\n")
