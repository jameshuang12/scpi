from Connect import connect
import unittest


class VnaUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        """ Function in unittest.TestCase that is initialized
        everytime a test case function is executed.
        """
        self.test_device = connect("TestVna")
        self.test_device.initialize_device()

    def test_initialization(self):
        self.assertTrue(self.test_device.New_Settings ==
                        self.test_device.Settings)
        self.assertEqual(
            self.test_device.New_Settings["GeneralSettings"]["Data_Format"], "ASC,0")
        self.assertFalse(
            self.test_device.New_Settings["GeneralSettings"]["Sweep_Continuous"] == "true")

    def test_value_assignments(self):
        # If you are using a device that hasn't been setup yet, or trying a function that hasn't been added
        self.test_device.set_res_bw(10000)  # Write a value to the device
        self.assertEqual(
            self.test_device.New_Settings["GeneralSettings"]["ResBW"], 10000)
        # Set up the settings that you want the device to use, these will be sent to the device later
        self.test_device.set_points(501)
        self.assertEqual(
            self.test_device.New_Settings["GeneralSettings"]["Points"], 501)
        self.test_device.set_start_frequency(8000000000)  # 8 GHz
        self.assertEqual(
            self.test_device.New_Settings["GeneralSettings"]["Start_Frequency"], 8000000000)
        self.test_device.set_stop_frequency(10500000000)  # 10.5 GHz
        self.assertEqual(
            self.test_device.New_Settings["GeneralSettings"]["Stop_Frequency"], 10500000000)

    def test_saving_data_closing_device(self):
        self.test_device.set_res_bw(10001)  # Write a value to the device
        self.test_device.set_points(500)
        self.test_device.set_start_frequency(7000000000)  # 7 GHz
        self.test_device.set_stop_frequency(10000000000)  # 10 GHz
        # Send all settings to the device, skipping settings that have not changed
        self.test_device.send_all_settings()

        # Save Data
        self.test_device.save_data('C:\\Data\\Test', "Testing VNA Devices")

        # Use this command to close out from using the device
        # Plan to only open and close the connection once
        self.test_device.close()
