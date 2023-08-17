import unittest
from Connect import connect


class SgUnitTest(unittest.TestCase):
    """ This module is used to run unit testing on the SG Class
    """

    def setUp(self) -> None:
        """ Function in unittest.TestCase that is initialized 
        everytime a test case function is executed
        """
        self.test = connect('TestSg')
        self.test.initialize_device()

    def test_initialization(self):
        """ Test if the initialization is set up properly
        """
        self.assertTrue(self.test.New_Settings == self.test.Settings)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Waveform_Shape"], "")
        self.assertFalse(
            self.test.New_Settings["GeneralSettings"]["Pulse_Generator_State"], True)

    def test_value_assignment(self):
        """ Test if the New_Settings set up the value correctly
        """
        self.test.set_waveform_shape("SQU")
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Waveform_Shape"], "SQU")

        self.test.set_output_amplitude(10)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Output_Amplitude"], 10)

        self.test.set_power_control(2)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Power_Control"], 2)

        self.test.set_frequency(2e6)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Frequency"], 2e6)

        self.test.set_stop_frequency(6e6)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Stop_Frequency"], 6e6)

        self.test.set_start_frequency(4e6)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Start_Frequency"], 4e6)

        self.test.set_center_frequency(5e6)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Center_Frequency"], 5e6)

        self.test.set_frequency_span(2e6)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Frequency_Span"], 2e6)

        self.test.set_frequency_sweep("STEP")
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Frequency_Sweep"], "STEP")

        self.test.set_sweep_space("LOG")
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Sweep_Space"], "LOG")

        self.test.set_space_step_width(44e5)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Space_Step_Width"], 44e5)

        self.test.set_pulse_generator_state(True)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Pulse_Generator_State"], True)

        self.test.set_rf_frequency_sweep_cycle("SING")
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["RF_Frequency_Sweep_Cycle"], "SING")

        self.test.set_screen_saver_mode(False)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Screen_Saver_Mode"], False)

    def test_saving_data_closing_device(self):
        """ Test if the Save Data saves the correct values into a text file """
        self.test.set_waveform_shape("SQU")
        self.test.set_output_amplitude(10)
        self.test.set_frequency(2e6)
        self.test.set_power_control(2)
        self.test.set_stop_frequency(6e6)
        self.test.set_frequency_span(3e6)
        self.test.set_frequency_sweep("STEP")
        self.test.set_sweep_space("LOG")
        self.test.set_space_step_width(44e5)
        self.test.set_pulse_generator_state(True)
        self.test.set_rf_frequency_sweep_cycle("SING")
        self.test.set_screen_saver_mode(False)
        # Send all settings to the device, skipping settings not changed
        self.test.send_all_settings()
        # Save Data
        self.test.save_data('C:..\\Downloads', "Testing SG Devices")
        # Use this command to close out from using the device
        # Plan to only open and close the connection once
        self.test.close()

    def test_modgenerator_settings_case(self):
        """ Unit Test for ModGenerator Settings """
        self.test.set_lf_frequency_sweep(True)
        self.test.set_lf_generator_output("SWE")
        self.test.send_all_settings()

        self.assertEqual(
            self.test.Settings["ModGeneratorSettings"]["LF_Frequency_Sweep"], True)

        self.assertEqual(
            self.test.Settings["ModGeneratorSettings"]["LF_Generator_Output"], "SWE")

    def test_modulation_settings_case(self):
        """ Unit Test for Modulation Settings """
        self.test.set_amplitude_modulation(True)
        self.test.send_all_settings()
        self.assertEqual(
            self.test.Settings["ModulationSettings"]["Amplitude_Modulation"], True)

        self.test.set_frequency_modulation(True)
        self.test.send_all_settings()
        self.assertEqual(
            self.test.Settings['ModulationSettings']['Frequency_Modulation'], True)

        self.test.set_phase_modulation(True)
        self.test.send_all_settings()
        self.assertEqual(
            self.test.Settings["ModulationSettings"]["Phase_Modulation"], True)

    def test_rf_block_auto_sweep_case(self):
        """ Unit Test for Auto Sweep for the RF Block"""
        self.test.set_frequency_sweep("AUTO")
        self.test.set_rf_frequency_sweep_cycle("AUTO")
        self.test.send_all_settings()
        self.test.send_sweep()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Frequency_Sweep"], "AUTO")

        self.assertEqual(
            self.test.Settings['GeneralSettings']["RF_Frequency_Sweep_Cycle"], "AUTO")

    def test_rf_block_single_sweep_case(self):
        """ Unit Test for Single Sweep for the RF Block """
        self.test.set_frequency_sweep("AUTO")
        self.test.set_rf_frequency_sweep_cycle("SING")
        self.test.send_all_settings()
        self.test.send_sweep()
        self.test.send_trigger()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Frequency_Sweep"], "AUTO")

        self.assertEqual(
            self.test.Settings['GeneralSettings']["RF_Frequency_Sweep_Cycle"], "SING")

    def test_rf_block_step_sweep_case(self):
        """ Unit Test for Step Sweep for the RF Block """
        self.test.set_center_frequency(3e8)
        self.test.set_frequency(4e8)
        self.test.set_sweep_space("LIN")
        self.test.set_space_step_width(1e8)
        self.test.set_frequency_sweep("MAN")
        self.test.set_rf_frequency_sweep_cycle("SING")
        self.test.send_all_settings()
        self.test.send_sweep()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Center_Frequency"], 3e8)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Frequency"], 4e8)

        self.assertEqual(
            self.test.Settings['GeneralSettings']["Sweep_Space"], "LIN")

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Space_Step_Width"], 1e8)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Frequency_Sweep"], "MAN")

        self.assertEqual(
            self.test.Settings['GeneralSettings']["RF_Frequency_Sweep_Cycle"], "SING")

    def test_rf_frequency_sweep_case(self):
        """ Unit Test for RF Frequency Sweep """
        self.test.set_center_frequency(3e8)
        self.test.set_sweep_space("LIN")
        self.test.set_space_step_width(2e7)
        self.test.set_rf_frequency_sweep_cycle("SING")
        self.test.set_frequency_sweep("AUTO")
        self.test.send_all_settings()
        self.test.send_sweep()
        self.test.send_trigger()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Center_Frequency"], 3e8)

        self.assertEqual(
            self.test.Settings['GeneralSettings']["Sweep_Space"], "LIN")

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Space_Step_Width"], 2e7)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Frequency_Sweep"], "AUTO")

        self.assertEqual(
            self.test.Settings['GeneralSettings']["RF_Frequency_Sweep_Cycle"], "SING")
