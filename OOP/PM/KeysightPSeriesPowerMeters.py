from .PMClass import PMClass


class KeysightPSeriesPowerMeter(PMClass):
    """
    The power meter helps determine settings to optimize performance. 
    This is the manual class that has implemented the required subsystems.
    """

    def __init__(self, address: str, is_usb_connection=False):
        """ Initialize the class """
        super().__init__(address, is_usb_connection)

    # Presets the Device
    def send_preset(self):
        current_timeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        self.write("SYST:PRES")
        self.write(self.Common_SCPI["WaitToContinue"])
        self.Device.settimeout(current_timeout)
        self.get_all_settings()

    def send_trigger(self):
        """ Sends a trigger activation if called, if not, reset the trigger
        """
        if self.Settings['GeneralSettings']["Activate_Trigger"] is False:  # OFF
            self.write("ABOR")
        elif self.Settings['GeneralSettings']["Activate_Trigger"] is True:  # ON
            self.write("INIT:IMM:ALL")
        else:  # ONCE
            self.write("DISP:WIND2:STAT")

    def send_calibration(self):
        """ Sends a calibration to the power meter and performs 
        interal adjustments
        """
        if self.calibrate is True:  # ON
            self.write("CAL:ZERO:AUTO ONCE")
            self.write("CAL:AUTO ONCE")

    def get_data(self):
        """ Reads the current response values of the active data trace, 
        reads or writes a memory trace, and reads or writes error terms.
        """
        power_type = self.Settings['GeneralSettings']['Power_Type']
        self.Data = self.read("CALC:DATA:ALL", power_type)
        return self.Data
