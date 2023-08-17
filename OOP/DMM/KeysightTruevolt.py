from .DMMClass import DMMClass


class KeysightTruevolt(DMMClass):
    """ This is a manual class that used to tell the digital muiltimeter to 
    perform various action. 

    This class inherits the DMMClass where the settings are replicated for use.
    The class is capable of telling the digital multimeter to get a
    single read. It is also able to collect the data from the specifed reading.
    """

    def __init__(self, address: str, is_usb_connection=False):
        """ Initialize the class """
        super().__init__(address, is_usb_connection)

    def send_abort(self):
        """ 
        Purpose: Sends abort command to digital multimeter
        which aborts all actions.   
        """
        self.write("ABOR")

    def send_single_read(self):
        """ 
        Purpose: Specifying ONCE performs an immediate autorange
        and then turns autoranging off.
        """
        function = self.Settings["GeneralSettings"]['Measurement_Function']
        command = self.Setting_Commands["Auto_Measurement_Level"]
        self.write(f"{function}:{command} ONCE")

    def get_data(self):
        """ 
        Purpose: Selects the secondary measurement 
        function for current measurements.
        """
        function = self.Settings["GeneralSettings"]['Measurement_Function']
        self.write(f"{function}:SEC CALC:DATA")
        self.Data = self.read("READ?;DATA2?")
        return self.Data
