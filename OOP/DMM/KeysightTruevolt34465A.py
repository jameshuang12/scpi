from .KeysightTruevolt import KeysightTruevolt

# The Truevolt Digital Multimeter (DMM) models are:
#  34460A - 6½-digit Basic DMM
#  34461A - 6½-digit 34401A Replacement DMM
#  34465A - 6½-digit DMM
#  34470A - 7½-digit DMM

# Keysight+34465A+Guide.pdf


class KeysightTruevolt34465A(KeysightTruevolt):
    """ The make/model class for the digital multimeter the lab
    is utilizing is 34465A
    """

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        # Aperature = 1 s
        self.min_resolution = 0.1  # ppm
        # Aperature = 1 ms
        self.max_resolution = 100  # ppm
        # Aperature = 10 ms
        self.default = 10  # ppm
