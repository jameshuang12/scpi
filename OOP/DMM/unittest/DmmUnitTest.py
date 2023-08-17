import unittest
from Connect import connect


class DmmUnitTest(unittest.TestCase):
    """ This module is used to return unit testing on the DMM class
    """

    def setUp(self) -> None:
        """ Function in unittest.TestCase that is initialized
        everytime a test case function is executed.
        """
        self.test = connect("TestDmm")
        self.test.initialize_device()

    def test_initialization(self):
        """ Test if the initialization is set up properly
        """
        self.assertTrue(self.test.New_Settings == self.test.Settings)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Measurement_Function"], '')
        self.assertTrue(
            self.test.New_Settings["GeneralSettings"]["Continuous_Read"], True)

    def test_value_assignment(self):
        """ Test if the New_Settings set up the value correctly
        """
        self.test.set_measurement_function('CAP')
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Measurement_Function"], '"CAP"')

        self.test.set_auto_measurement_level(False)
        self.assertEqual(
            self.test.New_Settings["MeasurementSettings"]["Auto_Measurement_Level"], False)

        self.test.set_trigger_level(100)
        self.assertEqual(
            self.test.New_Settings['GeneralSettings']["Trigger_Level"], 100)

        self.test.set_measurement_range(2e-9)
        self.assertEqual(
            self.test.New_Settings['MeasurementSettings']['Measurement_Range'], 2e-9)

        self.test.set_continuous_read(False)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Continuous_Read"], False)
        self.assertFalse(
            self.test.New_Settings["GeneralSettings"]["Continuous_Read"], True)

        self.test.set_data_format("REAL,64")
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Data_Format"], "REAL,64")

    def test_saving_data_closing_device(self):
        """ Test if the Save Data saves the correct values into a text file """
        self.test.set_measurement_function("CAP")
        self.test.set_auto_measurement_level(False)
        self.test.set_trigger_level(100)
        self.test.set_measurement_range(2e-9)
        self.test.set_continuous_read(True)
        self.test.set_data_format("REAL,64")
        # Send all settings to the device, skipping settings not changed
        self.test.send_all_settings()
        # Save Data
        self.test.save_data('C:..\\Downloads', "Testing DMM Devices")
        # Use this command to close out from using the device
        # Plan to only open and close the connection once
        self.test.close()
