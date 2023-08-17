from .RohdeSchwarzFspn import RohdeSchwarzFSPN


# See FSPN_UserManual_en_02.pdf

class RohdeSchwarzFSPN26(RohdeSchwarzFSPN):
    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.MaxFrequency_GHz = 26.5
        self.DCMinFrequency_MHz = 1  # TODO there is a lower min for DC coupled Baseband Noise
        self.ACMinFrequency_MHz = 10
        # the FSPN26 has a built-in attenuator at the RF input that the FSPN8 does not have
        self.Attenuator = True
