from .PGClass import PGClass


class KeysightEDU(PGClass):
    """ This is a manual class that used to tell the pulse generator to 
    perform various action. 

    This class inherits the PGClass where the settings are replicated for use.
    The class is capable of controlling the setting of the pulses. Plus, it
    is able to control the on/off for channel, modulation, sweep, and burst. 

    Only channel is able to activate an action. Look info TODO for more actions

    The class is also able to control where the pulse gets set in terms of the
    waveform specified in the PGClass' setting. 
    Lastly, the class can abort actions in the hardware, print out the general
    and specific waveform settings, and save the settings into a .txt file. 
    """

    def __init__(self, address: str, is_usb_connection=False):
        """ Initialize the class"""
        super().__init__(address, is_usb_connection)
    def send_abort(self):
        """ 
        Purpose; Sends abort command to pulse generator which 
        aborts all actions.   
        """
        self.write("ABOR")

    def send_pulse_output(self):
        """ 
        Purpose: Controls whether to output a continuous pulse or a
        singlur pulse.

        Addtional Performance of APPLy Command:
        1. Sets Trigger Source to IMM
        2. Turns off modulation,sweep, or burst if on
        3. Turns on channel output (OUTPut ON)
        4. Overrides voltage autorange and enables autoranging (VOLT:RANG:AUTO)
        """
        # Checks if continuous waveform is true
        if self.Settings["GeneralSettings"]["Continuous_Waveform"]:

            # Check if the output is true
            if not self.output:
                self.write("OUTP ", True)
                self.output = True
            else:
                self.write("OUTP ", False)
                self.output = False

        # Sends a singular pulse
        else:
            self.write("INIT:IMM")

    # TODO Need to call the subsystem to write directly to the hardware.
    #      def send_modulation_output(self) currently turns on/off the button.
    #      TASK: Implement SCPI Programming subsystem for modulation
    def send_modulation_output(self):
        """ 
        Purpose: Controls the modulation on turning it on or off

        Will not enable modulation if sweep or burst is enabled
        """
        # Checks if the modulation is true
        if not self.modulation:

            # Enables the AMplitudemodulation:STATe to on
            self.write("SOUR:AM:STAT", True)
            self.modulation = True
            self.write('SOUR:SWE:STAT', False)
            self.write('SOUR:BURS:STAT', False)

        else:
            self.write("SOUR:AM:STAT", False)
            self.modulation = False

    # TODO Need to call the subsystem to write directly to the hardware.
    #      def send_sweep_output(self) currently turns on/off the button.
    #      TASK: Implement SCPI Programming subsystem for sweep
    def send_sweep_output(self):
        """ 
        Purpose: Controls the sweep on turning it on or off

        Will not enable sweep if modulation or bust is enabled
        """
        # Checks if the sweep is true
        if not self.sweep:

            # Enables the SWEep:STATe to on
            self.write("SOUR:SWE:STAT", True)
            self.sweep = True
            self.write('SOUR:AM:STAT', False)
            self.write('SOUR:BURS:STAT', False)

        else:
            self.write('SOUR:SWE:STAT', False)
            self.sweep = False

    # TODO Need to call the subsystem to write directly to the hardware.
    #      def send_surst_output(self) currently turns on/off the button.
    #      TASK: Implement SCPI Programming subsystem for burst
    def send_burst_output(self):
        """ 
        Purpose: Controls the burst on turning it on or off

        Will not enable burst if sweep or modulation is enabled
        """
        # Checks if the burst is true
        if not self.burst:

            # Enables the BURSt:STATe to on
            self.write("SOUR:BURS:STAT", True)
            self.burst = True
            self.write('SOUR:SWE:STAT', False)
            self.write('SOUR:AM:STAT', False)

        else:
            self.write('SOUR:BURS:STAT', False)
            self.burst = False
