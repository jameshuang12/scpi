from .RohdeSchwarzZvaZvbZvt import RohdeSchwarzZvaZvbZvt


# See ZVA_AVB_ZVT_OperatingManueal_en_33.pdf

class RohdeSchwarzZva244port(RohdeSchwarzZvaZvbZvt):
    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.number_of_ports = 4
