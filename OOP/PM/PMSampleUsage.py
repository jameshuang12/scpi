""" PM SAMPLE USAGE

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
# Replace 'TestPM' with Test{devicetype} to test the code with that device type
# Replace 'TestPM' with the IP Address of the Device to actually connect to it
# IP Address :
test = connect("TestPM")

""" Setting Commands Testing """


# Writes a value to the device and returns the specified value
test.write(test.Setting_Commands["Frequency"], 1e5)
# Output:'FREQ 1e5\n'

# This will return the value of the command by calling the read function
# Sets the frequency period, sends the new settings, and then reads the value
test.set_frequency(1e5)
test.send_all_settings()
test.read(test.Setting_Commands["Frequency"])
# Output: FREQ?
#         '2e6'

""" Description on Test Cases """

# Setup the general settings that you want the device to use,
# All these commands below will be sent to the hardware later
test.set_power_type("AC")
test.set_trigger_cycle(False)
test.set_trigger_type("POS")
test.set_trigger_level("ON")
test.set_trigger_source("HOLD")
test.set_trigger_delay(0.001)
test.set_data_format("REAL")
test.set_start_frequency(1e6)
test.set_frequency_sweep(10)
test.set_stop_frequency(2e6)

# Send all settings to the hardware. From here, the New_Settings should
# match to Settings as all of the values are copied over.
test.send_all_settings()

# Send a rf output by turning on the rf and then wait 3 seconds to turn it off
test.send_rf_output()
time.sleep(3)
test.send_rf_output()

# Send a amplitude modulation by turning on the channel
# and then wait 3 seconds to turn it off
test.send_modulation_output()
time.sleep(3)
test.send_modulation_output()


# Gets the file name and imports that file into the power meter
# test.send_data_file("PM_File")

# Selects the separator between the frequency and level column.
# test.send_separator_file("PM_File")

# Sends a calibration
# test.send_calibration()

# Save Data if interested
test.Save_Data('C:\\Data\\Test')

# Prints out the settings in the terminal
test.print_settings()

# Use this command to close out from using the device
# Plan to only open and close the connection once
test.close()

###############################################################################
####         TEST CASES able to be ran in Connect.py or terminal        #######
###############################################################################

# Ex. CODE TO WRITE IN TERMINAL TO TEST
# C:\Users\"Name"\> cd "To where the file is located"
# >py

# from Connect import Connect
# test = Connect("INSERT the IP Address for the device")
# test.Settings (to see the current settings)
