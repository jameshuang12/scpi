""" SG SAMPLE USAGE

This module will provide background on how to test this device exactly through
the terminal.

The module has been split into portions to help you understand how to test.

Remember, this module is a guide used for software testing.
"""

# Locate your terminal to the correct file location
# C:\Users\"Name"\> cd "To where the file is located"
# >py

# Then, you to import connect and set connect to a variable
from Connect import connect
# TO TEST WITH THE HARDWARE DIRECTLY
# Replace 'TestSG' with Test{devicetype} to test the code with that device type
# Replace 'TestSG' with the IP Address to test with the device directly
test = connect("TestSg")

""" Setting Commands Testing """

# Writes a value to the test and returns the specified value
test.write(test.Setting_Commands["Frequency"], 2e6)
# Output:'FREQ 2e6\n'


# This will return the value of the command by calling the read function
# Sets the frequency period, sends the new settings, and then reads the value
test.set_frequency(2e6)
test.send_all_settings()
test.read(test.Setting_Commands["Frequency"])
# Output: FREQ?
#         '2e6'

""" Description on Test Cases """

# Setup the general settings that you want the device to use,
# All these commands below will be sent to the hardware later
test.set_waveform_shape("SQU")
test.set_output_amplitude(10)
test.set_frequency(2e6)
test.set_power_control(2)
test.set_stop_frequency(600e6)
test.set_start_frequency(400e6)
test.set_center_frequency(500e6)
test.set_frequency_span(200e6)
test.set_frequency_sweep("STEP")
test.set_sweep_space("LOG")
test.set_space_step_width(44e5)
test.set_amplitude_modulation(True)
test.set_rf_frequency_sweep_cycle("SING")
test.set_screen_saver_mode(False)

# Send all settings to the hardware. From here, the New_Settings should
# match to Settings as all of the values are copied over.
test.send_all_settings()

# Send a rf output by turning on the rf and then wait 3 seconds to turn it off
test.send_rf_output()
time.sleep(3)
test.send_rf_output()

# Gets the file name and imports that file into the signal generator
# test.send_data_file("SG_File")

# Selects the separator between the frequency and level column.
# test.send_separator_file("SG_File")

# Sends a calibration to the current waveform
# test.send_calibration()

# Save Data if interested
test.save_data('C:\\Data\\Test')

# Prints out the settings in the terminal
test.print_settings()

# Use this command to close out from using the device
# Plan to only open and close the connection once
test.close()
