from .KeysightEDU import KeysightEDU


# EDU22210-Series-Trueform-Arbitrary-Waveform-Generator-Programming-Guide.pdf


class KeysightTechnologiesEDU33211A(KeysightEDU):
    """ The make/model class for the EDU33211A. Below is 
    specific details to the model the lab is utilizing.
    """

    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.max_frequency = 2e7  # Hz or 20 MHz
        self.number_of_channels = 1
        self.arbitrary_waveform = True
        self.memory_per_channel = 8e6  # Sa or 8 MSa

# This is another instrument model that our lab will not be utilizing
# class keysight_EDU33212A(Keysight_EDU):
#     """ The make/model class for the EDU33212A.
#     """
#     Max_Frequency = 2e7 # Hz or 20 MHz
#     Number_of_Channels = 2
#     Arbitrary_Waveforms = True
#     Memory_per_Channel = 8e6 # Sa or 8 MSa
