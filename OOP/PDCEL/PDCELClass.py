import os
import sys

from OOP.BaseDevice import BaseDevice


# File: Programmable DC Electronic Class
# Author: Jacobs Engineerng Group
# Date: June 2023
# Copyright: Written by Jacobs Engineering Group with Jacobs proprietary and
# general purpose rights. All rights reserved. Look into copying for details.


class PDCELClass(BaseDevice):
    """ The device class that sets up the general settings for PDCEL.

    The class inherits all of the functions in the Scpidevice class that 
    replicate some of the core functionality of the SCPI Class.

    The device class mainly has functions that set up the settings for the
    device itself. The class also has parent functions for the
    manual class that will be inherited by the children functions.
    """

    # TODO FIX THE FLOAT AND STRING for setting comands like Current_Slew_Positive
    # TODO FIX THE CAPATTALIZATION ISSUES FOR FUNCTIONS, use set_trigger_timer
    # as a reference. This will resolve the python syntax formatting issue.
    def __init__(self, address: str):
        super().__init__(address)
        self.device_type = "PDCEL"

        self.Setting_Commands = {
            "Trigger_Timer": "TRIG:TIM",
            "Trace_Delay": "TRAC:DELA",
            "Trigger_Source": "TRIG:SOUR",
            "Trace_Feed": "TRAC:FEED",
            "Trace_Points": "TRAC:POIN",
            "Trace_Feed:Control": "TRAC:FEED:CONT",
            "Current_Slew" : "CURR:SLEW",
            "Current_Slew_Positive" : "CURR:SLEW:POS",
            "Current_Slew_Negative" : "CURR:SLEW:NEG"
        }
        self.Extra_Setting = {
             "Trigger_Timer": "",
             "Trace_Delay": "",
             "Trigger_Source": "",
             "Trace_Feed": "",
             "Trace_Points": "",
             "Trace_Feed:Control": "",
             "Current_Slew": "",
             "Current_Slew_Positive": "",
             "Current_Slew_Negative": ""
        }
        self.Settings = {
            "GeneralSettings": {
                "Trigger_Timer": 0,
                "Trace_Delay": 0,
                "Trigger_Source": "",
                "Trace_Feed": "",
                "Trace_Points": 0,
                "Trace_Feed:Control": "",
                "Current_Slew_Positive": "",
                "Current_Slew_Negative": "" 
            }
        }
        self.Settings_Format = {
            "Trigger_Timer": float,
            "Trace_Delay": float,
            "Trigger_Source": str,
            "Trace_Feed": str,
            "Trace_Points": float,
            "Trace_Feed:Control": str,
            "Current_Slew": float,
            "Current_Slew_Positive": float,
            "Current_Slew_Negative": float
        }

        # Creates a shallow copy of Settings with New Settings
        # Iterates through Settings as there may be more than 1 setting
        for key in self.Settings:
            self.New_Settings[key] = self.Settings[key].copy()

    """  General Setting Functions  """

    def set_trigger_timer(self, timer: float):
        """ Checks edge cases and sets the new value for trigger
        timer in the new general settings."""

        if timer > 1 or timer  <1:
            sys.exit(f"{timer} is out of range of trigger timer")
        else:
            self.New_Settings["GeneralSettings"]['Trigger_Timer'] = timer

    def set_trace_delay(self, Delay: float):
        """ Checks edge cases and sets the new value for Trace Delay
          in the new general settings."""
        if Delay > 1 or Delay > 1:
            sys.exit(f"{Delay} is out of range of trace delay")
        else:
            self.New_Settings["GeneralSettings"]['trace_delay'] = Delay

    def set_trigger_source(self, Source: str):
        """ Checks edge cases and sets the new value for trigger
        source in the new general settings.

        Default is an empty string
        Unit: Source is an str
        """
        if Source == "":
            sys.exit(f"{Source} is not in the trigger source list"
                     " or is an empty string.")
        else:
            self.New_Settings["GeneralSettings"]["Trigger_Source"] = Source

    def Trace_Feed(self, Feed: str):
        """ Checks edge cases and sets the new value for Trace Feed
          in the new general settings."""
        if Feed == "":
            sys.exit(f"{Feed} is out of range of Trace_Feed")
        else:
            self.New_Settings["GeneralSettings"]['Trace_Feed'] = Feed

    def Trace_Points(self, Point: float):
        """ Checks edge cases and sets the new value for trigger
        source in the new general settings.

        Default is an empty string
        Unit: Source is an Float
        """
        if Point > 1 or Point > 1:
            sys.exit(f"{Point} is not in the Trace_Points list"
                     " or is an empty string.")
        else:
            self.New_Settings["GeneralSettings"]["Trace_Points"] = Point

    def Trace_Feed_Control(self, Feed_Control: str):
        """ Checks edge cases and sets the new value for Trace Feed
          in the new general settings."""
        if Feed_Control =="":
            sys.exit(f"{Feed_Control} is out of range of Trace_Feed_Control")
        else:
            self.New_Settings["GeneralSettings"]['Trace_Feed_Control'] = Feed_Control

    def Current_Slew(self, Slew: float):
        """ Checks edge cases and sets the new value for Current Slew
         in the new general settings."""
        if Slew > 1 or Slew < 1:
            sys.exit(f"{Slew} is out of range of Current Slew")
        else:
            self.New_Settings["GeneralSettings"]['Current_Slew'] = Slew

    def Current_Slew_Pos(self, slew_pos: float):
        """ Checks edge cases and sets the new value for Current Slew Pos
         in the new general settings."""

        if slew_pos > 1 or slew_pos > 1:
            sys.exit(f"{slew_pos} is out of range of Current Slew_Pos")
        else:
            self.New_Settings["GeneralSettings"]['Current_Slew_Pos'] = slew_pos

    def Current_Slew_Neg(self, slew_neg: float):
        """ Checks edge cases and sets the new value for Current Slew Neg
         in the new general settings."""

        if slew_neg > 1 or slew_neg > 1:
            sys.exit(f"{slew_neg} is out of range of Current Slew_Neg")
        else:
            self.New_Settings["GeneralSettings"]['Current_Slew_Pos'] = slew_neg
