import sys
from .SGClass import SGClass


class RohdeSchwarzSMB(SGClass):
    """ The manual class that is used to tell the signal generator to
    perform various actions.

    The class inherits the SGClass where the settings are replicated for use.
    The class is capable of controlling the settings of the pulse, open a
    saved file to apply the file's data into the hardware, and can calibrate 
    the instrument if needed.

    The R&S SMB is a high-performance signal generator developed 
    to meet requirements asked by users. The hardware is capable to create 
    RF waveforms. These waveforms can be simple or complex. 
    """

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)

    def send_preset(self):
        """ 
        Purpose: Sends a preset to the device
        """
        current_timeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        self.write("SYST:PRES")
        self.write(self.Common_SCPI["WaitToContinue"])
        self.Device.settimeout(current_timeout)
        self.get_all_settings()

    def send_abort(self):
        """ 
        Purpose: Sends abort command to pulse generator which aborts 
        all actions.
        """
        self.write("ABOR")

    def send_sweep(self):
        """ 
        Purpose: Sends the sweep command which activates the sweep
        """
        self.write("SOUR:FREQ:MODE", "SWE")

    def send_rf_output(self):
        """ 
        Purpose: Controls whether to send an rf output or not.
        """
        # if Output is true
        if not self.rf_output:
            self.write("OUTP", True)
            self.rf_output = True
        else:
            self.write("OUTP", False)
            self.rf_output = False

    def send_data_file(self, filename: str):
        """ 
        Purpose: Able to use a data file to set the waveform settings. 
        The function would be able to move a file to the signal generator 
        from the computer and select that designated file to execute.

        Command: LIST:DEXC:AFILE:SEL <Filename>
        Parameter: <ascii_file_name>
        """
        self.write("LIST:DEXC:MODE", "IMP")
        # determines that ASCII files with frequency and level value pairs
        # are imported into list mode lists.
        self.write("LIST:DEXC:AFIL:EXT", "TXT")
        # determines the extension *.txt for the query.
        self.write("LIST:DEXC:AFIL:CAT?")
        # queries the available files with extension *.txt.
        # Response: 'list1,list2'
        # the ASCII files list1.txt and list2.txt exist.
        self.write("LIST:DEXC:AFIL:SEL", filename)
        # selects list.csv for import.
        self.write("LIST:DEXC:SEL", 'C:\\Data\\Test')
        # determines the destination file list_imp.
        self.write("LIST:DEXC:EXEC")
        # imports the ASCII file data into the list file

    def send_separator_file(self, filename: str, separator: str):
        """ 
        Purpose: Selects the separator between the frequency 
        and level column of the ASCII table.

        Command: LIST:DEXC:AFIL:SEP:COL <Column>
        Parameters: TAB | SEM | COMM | SPAC
        """
        self.write("LIST:DEXC:MODE", "EXP")
        # selects that the list is exported into an ASCII file.
        self.write("LIST:DEXC:AFIL:SEL", '/var/list.csv')
        # determines ASCII file list.csv as destination for the list mode list
        # data.
        self.write("LIST:DEXC:AFIL:SEP:COL", separator)
        # defines a tabulator to separate the frequency and level values
        # pairs.
        self.write("LIST:DEXC:AFIL:SEP:DEC", "DOT")
        # selects the decimal separator dot.
        self.write("LIST:DEXC:SEL", filename)
        # determines the source file list_imp for export into the ASCII file
        # list.csv.
        self.write("LIST:DEXC:SEL", 'C:\\Data\\Test')
        # determines the destination file list_imp.
        self.write("LIST:DEXC:EXEC")
        # exports the list file data into the ASCII file.

    def send_calibration(self):
        """ 
        Purpose: Sends a calibration to start alll internal adjustments that do 
        no require external measurement equipment.

        Attention: A level of more than 20 dBm will be present at the RF
        output of the instrument during the adjustment. Please connect a 
        50 Ohm termination to the RF output of the instrument.
        """
        response = self.show_yes_no_gui(
            title="Signal Generator's Send Calibration Function",
            message="Attention: A level of more than 20 dBm will be present"
            " at the RF output of the instrument during the adjustment. Did"
            " you connect a 50 Ohm termination to the RF output?")

        if response == 'yes':
            level = self.Settings['GeneralSettings']['Output_Amplitude']
            if level > 20:
                self.write("CAL:ALL", True)
        else:
            sys.exit("The 50 Ohm termination needs to be connected"
                     " to the RF output before calibrating, exiting code...")
