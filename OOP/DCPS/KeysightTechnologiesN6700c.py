from OOP.DCPS import DCPSClass


# See ZVA_AVB_ZVT_OperatingManueal_en_33.pdf

class KeysightTechnologiesN6700c(DCPSClass):

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.Number_of_Possible_Modules = 4
