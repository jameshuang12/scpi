import unittest
from Connect import connect


class PgUnitTest(unittest.TestCase):
    """ This module is used to run unit testing on the PG class
    """

    def setUp(self) -> None:
        """ Function in unittest.TestCase that is initialized
        everytime a test case function is executed.
        """
        self.test = connect("TestPg")
        self.test.initialize_device()

    def test_initialization(self):
        """ Test if the initialization is set up properly
        """
        self.assertTrue(self.test.New_Settings == self.test.Settings)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Waveform_Type"], "")
        self.assertFalse(
            self.test.New_Settings["GeneralSettings"]["Continuous_Waveform"], True)

    def test_value_assignment(self):
        """ Test if the New_Settings set up the value correctly 
        """
        self.test.set_waveform_type("SIN")
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Waveform_Type"], "SIN")

        self.test.set_voltage_low(0)
        self.assertEqual(
            self.test.New_Settings["WaveformSettings"]["Voltage_Low"], 0)

        self.test.set_frequency(1e5)
        self.assertEqual(
            self.test.New_Settings["WaveformSettings"]["Frequency"], 1e5)

        self.test.set_voltage_high(2)
        self.assertEqual(
            self.test.New_Settings["WaveformSettings"]["Voltage_High"], 2)

        self.test.set_phase_parameter(90)
        self.assertEqual(
            self.test.New_Settings["WaveformSettings"]["Phase_Parameter"], 90)

        self.test.set_continuous_waveform(True)
        self.assertEqual(
            self.test.New_Settings["GeneralSettings"]["Continuous_Waveform"], True)

    def test_saving_data_closing_device(self):
        """ Test if the Save Data saves the correct values into a text file """
        self.test.set_waveform_type("SIN")
        self.test.set_voltage_low(0)
        self.test.set_frequency(1e5)
        self.test.set_voltage_high(2)
        self.test.set_phase_parameter(90)
        self.test.set_continuous_waveform(True)
        # Send all settings to the device, skipping settings not changed
        self.test.send_all_settings()
        # Save Data
        self.test.save_data('C:..\\Downloads', "Testing PG Devices")
        # Use this command to close out from using the device
        # Plan to only open and close the connection once
        self.test.close()

    def test_sin_case(self):
        """ Unit test for SIN"""
        self.test.set_waveform_type("SIN")
        self.test.set_voltage_low(0.0)
        self.test.set_frequency(1e5)
        self.test.set_voltage_high(2.0)
        self.test.set_phase_parameter(90.0)
        self.test.set_continuous_waveform(True)
        self.test.send_all_settings()
        self.test.send_pulse_output()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Waveform_Type"], "SIN")

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_Low"], 0)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Frequency"], 1e5)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_High"], 2)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Phase_Parameter"], 90)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Continuous_Waveform"], True)

        self.assertFalse(self.test.output, False)

    def test_squ_case(self):
        """ Unit test for SQU """
        self.test.set_waveform_type("SQU")
        self.test.set_voltage_low(0.0)
        self.test.set_frequency(10000.0)
        self.test.set_voltage_high(4.0)
        self.test.set_duty_cycle(20.0)
        self.test.set_continuous_waveform(True)
        self.test.send_all_settings()
        self.test.send_pulse_output()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Waveform_Type"], "SQU")

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_Low"], 0)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Frequency"], 1e4)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_High"], 4)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Duty_Cycle"], 20)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Continuous_Waveform"], True)

        self.assertFalse(self.test.output, False)

    def test_ramp_case(self):
        """ Unit test for RAMP """
        self.test.set_waveform_type("RAMP")
        self.test.set_voltage_low(0.0)
        self.test.set_frequency(10000.0)
        self.test.set_voltage_high(4.0)
        self.test.set_ramp_symmetry(100.0)
        self.test.set_continuous_waveform(True)
        self.test.send_all_settings()
        self.test.send_pulse_output()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Waveform_Type"], "RAMP")

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_Low"], 0)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Frequency"], 1e4)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_High"], 4)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Ramp_Symmetry"], 100)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Continuous_Waveform"], True)

        self.assertFalse(self.test.output, False)

    def test_puls_case(self):
        """ Unit test for PULS """
        self.test.set_waveform_type("PULS")
        # self.test.set_leading_edge_time(4e-8)
        # self.test.set_trailing_edge_time(1e-6)
        self.test.set_pulse_width(3e-6)
        self.test.set_frequency(2e5)
        self.test.set_voltage_high(3.0)
        self.test.set_voltage_low(0.0)
        self.test.set_continuous_waveform(True)
        self.test.send_all_settings()
        self.test.send_pulse_output()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Waveform_Type"], "PULS")

        # self.assertEqual(
        #     self.test.Settings["WaveformSettings"]["Leading_Edge_Time"], 4e-8)

        # self.assertEqual(
        #     self.test.Settings["WaveformSettings"]["Trailing_Edge_Time"], 1e-6)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]['Pulse_Width'], 3e-6)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_Low"], 0)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Frequency"], 2e5)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_High"], 3)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Continuous_Waveform"], True)

        self.assertFalse(self.test.output, False)

    def test_prbs_case(self):
        """ Unit test for PRBS """
        self.test.set_waveform_type("PRBS")
        self.test.set_edge_time(8.4e-9)
        self.test.set_frequency(2e5)
        self.test.set_voltage_high(3.0)
        self.test.set_voltage_low(0.0)
        self.test.set_continuous_waveform(True)
        self.test.send_all_settings()
        self.test.send_pulse_output()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Waveform_Type"], "PRBS")

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Edge_Time"], 8.4e-9)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_Low"], 0)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Frequency"], 2e5)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_High"], 3)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Continuous_Waveform"], True)

        self.assertFalse(self.test.output, False)

    def test_dc_case(self):
        """ Unit test for DC """
        self.test.set_waveform_type("DC")
        self.test.set_voltage_high(0.0)
        self.test.set_voltage_low(-5.0)
        self.test.set_continuous_waveform(True)
        self.test.send_all_settings()
        self.test.send_pulse_output()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Waveform_Type"], "DC")

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_Low"], -5)

        self.assertEqual(
            self.test.Settings["WaveformSettings"]["Voltage_High"], 0)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Continuous_Waveform"], True)

        self.assertFalse(self.test.output, False)

    def test_general_setting_case(self):
        """ Unit test for General Settings """
        self.test.set_trigger_source("IMM")
        self.test.set_trigger_delay(5.0)
        self.test.set_trigger_output(True)
        self.test.set_trigger_polarity("POS")
        self.test.set_burst_cycles(5.0)
        self.test.send_all_settings()

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Trigger_Source"], "IMM")

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Trigger_Delay"], 5)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Trigger_Output"], True)

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Trigger_Polarity"], "POS")

        self.assertEqual(
            self.test.Settings["GeneralSettings"]["Burst_Cycles"], 5)

        self.test.send_modulation_output()
        self.assertFalse(self.test.modulation, False)

        self.test.send_sweep_output()
        self.assertFalse(self.test.sweep, False)

        self.test.send_burst_output()
        self.assertFalse(self.test.burst, False)

        self.test.send_pulse_output()
        self.assertFalse(self.test.output, False)
