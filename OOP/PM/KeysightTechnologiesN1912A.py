from .KeysightPSeriesPowerMeters import KeysightPSeriesPowerMeter

# KeySight_N1911A_1912A_Manual.pdf


class KeysightTechnologiesN1912A(KeysightPSeriesPowerMeter):
    """ The make/model classs for the PowerMeters is N1912A.
    """

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.number_of_channels = 2
        # "(TRIG:SOUR)"
        self.trigger_source = "IMM"  # Immediate
        # "(SENS:AVER:COUN:AUTO)"
        self.filter = True
        # state(SENS:AVER:STAT)
        self.filtet = True
        # (TRIG:DEL:AUTO)
        self.trigger_delay = True
