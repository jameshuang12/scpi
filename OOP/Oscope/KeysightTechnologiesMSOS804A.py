from .KeysightInfiniiumScope import KeysightInfiniiumScope


# See ZVA_AVB_ZVT_OperatingManueal_en_33.pdf

class KeysightTechnologiesMSOS804A(KeysightInfiniiumScope):

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.Number_of_Channels = 4
        self.Digital_Option = True
        self.Digital_Channels = 16
        self.Bandwidth = 8000000000  # Hz
