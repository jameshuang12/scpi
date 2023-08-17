import unittest
from Connect import connect


class PmUnitTest(unittest.TestCase):
    """ This module is used to run unit testing on the PM Class.
    """

    def setUp(self) -> None:
        """ Function in unittest.Testcase that is initialized
        everytime a test case function is executed
        """
        self.test = connect("TestPm")
        self.test.initialize_device()

    def test_initailization(self):
        """ Test if the initialization is set up properly
        """
        self.assertTrue(self.test.New_Settings == self.test.Settings)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Power_Type"], "")
        self.assertFalse(
            self.test.New_Settings['GeneralSettings']["Trigger_Cycle"], False)

    def test_value_assignment(self):
        """ Test if the New_Settings set up the value correctly
        """
        self.test.set_power_type("AC")
        self.assertTrue(
            self.test.New_Settings["GeneralSettings"]["Power_Type"], "AC")

        self.test.set_trigger_cycle(False)
        self.assertFalse(
            self.test.New_Settings["GeneralSettings"]['Trigger_Cycle'], False)

        self.test.set_trigger_slope("POS")
        self.assertTrue(
            self.test.New_Settings["GeneralSettings"]['Trigger_Slope'], "POS")

        self.test.set_trigger_level(10)
        self.assertTrue(
            self.test.New_Settings['GeneralSettings']["Trigger_Level"], 10)

        self.test.set_activate_trigger(True)
        self.assertTrue(
            self.test.New_Settings['GeneralSettings']["Activate_Trigger"], True)

        self.test.set_trigger_source("HOLD")
        self.assertTrue(
            self.test.New_Settings["GeneralSettings"]['Trigger_Source'], "HOLD")

        self.test.set_trigger_delay(0.001)
        self.assertTrue(
            self.test.New_Settings["GeneralSettings"]['Trigger_Delay'], 0.001)

        self.test.set_data_format("REAL")
        self.assertTrue(
            self.test.New_Settings['GeneralSettings']['Data_Format'], "REAL")

        self.test.set_start_frequency(1e6)
        self.assertEqual(
            self.test.New_Settings['GeneralSettings']["Start_Frequency"], 1e6)

        self.test.set_frequency_sweep(10)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Frequency_Sweep"], 10)

        self.test.set_stop_frequency(2e6)
        self.assertEqual(
            self.test.New_Settings['GeneralSettings']["Stop_Frequency"], 2e6)

    def test_saving_data_closing_device(self):
        """ Test if save data saves the correct values into a text file """
        self.test.set_power_type("AC")
        self.test.set_trigger_cycle(False)
        self.test.set_trigger_slope("POS")
        self.test.set_trigger_level(10)
        self.test.set_activate_trigger(True)
        self.test.set_trigger_source("HOLD")
        self.test.set_trigger_delay(0.001)
        self.test.set_data_format("REAL")
        self.test.set_start_frequency(1e6)
        self.test.set_frequency_sweep(10)
        self.test.set_stop_frequency(2e6)
        # Send all the settings to the device, skipping settings not changed
        self.test.send_all_settings()
        # Save data
        self.test.save_data('C:..\\Downloads', "Testing PM Devices")
        # Use this command to close out from using the device
        # Plan to only open and close the connection once
        self.test.close()

    def test_ac_case(self):
        """Unit test for AC"""
        self.test.set_power_type("AC")
        self.test.set_trigger_cycle(False)
        self.test.set_trigger_slope("POS")
        self.test.set_trigger_level(10)
        self.test.set_activate_trigger(True)
        self.test.set_trigger_source("HOLD")
        self.test.set_trigger_delay(0.001)
        self.test.set_data_format("REAL")
        self.test.set_start_frequency(1e6)
        self.test.set_frequency_sweep(10)
        self.test.set_stop_frequency(2e6)
        self.test.send_all_settings()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Power_Type"], "AC")

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Trigger_Cycle"], False)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Trigger_Slope"], "POS")

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Trigger_Level"], 10)

        self.assertEqual(
            self.test.Settings['GeneralSettings']["Activate_Trigger"], True)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Trigger_Source"], "HOLD")

        self.assertEqual(
            self.test.Settings["GeneralSettings"]['Trigger_Delay'], 0.001)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Data_Format"], "REAL")

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Start_Frequency"], 1e6)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Frequency_Sweep"], 10)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Stop_Frequency"], 2e6)
