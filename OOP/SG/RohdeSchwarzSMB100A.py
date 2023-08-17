from .RohdeSchwarzSMB import RohdeSchwarzSMB


# SMB100A_OperatingManual_en_23.pdf

# Model numbers
# ● R&S®SMB-B140/-B140L/-B140N

class RohdeSchwarzSMB100A(RohdeSchwarzSMB):
    """ The make/model class that gives specific details to the model
    the lab is utilizing.

    The model the lab is using on the RX/TX tile is B140L.
    """

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.max_frequency = 4e10  # Hz or 40 GHz
        self.min_frequency = 1e5  # Hz or 100 kHz
        # Both of the SSB has a 108 dBc (typ.)
        self.ssb_phase_noise_offset_ghz = 1e10  # Hz or 10 GHz
        self.ssb_phase_noise_offset_khz = 2e4  # Hz or 20 khz
        # Both Wideband has a 138 dBc
        self.wideband_noise_ghz = 1e10  # Hz or 10 GHz
        self.wideband_noise_mhz = 3e8  # Hz or 30 Mhz
        self.high_output_power = 27  # dbm
