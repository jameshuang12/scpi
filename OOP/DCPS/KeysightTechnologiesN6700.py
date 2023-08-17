# See ZVA_AVB_ZVT_OperatingManueal_en_33.pdf
from OOP.DCPS import DCPSClass


class KeysightTechnologiesN6700(DCPSClass):
    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.Endian = '>'
        self.BinaryEndsWithTermination = True

    "Commands that MAY need to be overwritten "
    # Update Initialize commands if needed

    #    def Additional_Initialization(self):
    #        self.Initialize_Values()
    #        self.send_SweepContinuous(False)

    "Commands that DO need to be overwritten"
    # Gets Model, Options, and Serial Number of specified module
    def get_module_information(self, module: int):
        self.Module_Information[module - 1] = {
            "Model": self.read("SYST:CHAN:MOD", " (@{})".format(module)),
            "Option": self.read("SYST:CHAN:OPT", " (@{})".format(module)),
            "Serial_Number": self.read("SYST:CHAN:SER", " (@{})".format(module))
        }

    # Initiates a sweep when the device is not in continuous sweep
    # TODO Update based on manual
    def send_power_on(self, module: int, on: bool = True):
        if self.Address != "TEST":
            self.log_info(self.ND.format("send_power_on {}".format(int(on))))

    # Reads the current response values of the active data trace, reads or writes a memory trace, and
    # reads or writes error terms.
    # TODO Update based on manual
    def get_data(self, channel: int = 1, datatype: str = 'SDAT'):
        data = ''
        data_types = {'FDAT', 'SDAT', 'MDAT', 'TSD'}
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_Data'))
        # else:
        #    Data = Default Data for Test based self.Points
        if datatype.upper() not in data_types:
            self.log_error('Format must be on of these:\n{}'.format(data_types))
        self.Data = data
        return data

    # Reads the current response values of all data and memory traces of the current test setup.
    # TODO Update based on manual
    def get_all_data(self, datatype: str = 'SDAT'):
        data = ''
        data_types = {'FDAT', 'SDAT', 'MDAT', 'TSD'}
        if self.Address != "TEST":
            self.log_info(self.ND.format('get_AllData'))
        # else:
        #    Data = Default Data for Test based self.Points
        if datatype.upper() not in data_types:
            self.log_error('Format must be on of these:\n{}'.format(data_types))
        self.Data = data
        return data
