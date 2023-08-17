""" DMM SAMPLE USAGE

This module will provide a background on how to test this device exactly
through the terminal.

The module has been split into portions to help you understadn how to test.

Remember, this modeul is a guide used for software testing.
"""

# Locate your terminal to the correct file location
# C:\Users\"Name"\> cd "To where the file is located"
# >py

# Then, you to import connect and set connect to a variable
from Connect import connect
# TO TEST WITH THE HARDWARE DIRECTLY
# Replace 'TestSG' with Test{devicetype} to test the code with that device type
# Replace 'TestSG' with the IP Address to test with the device directly
test = connect("TestDmm")

""" Setting Commands Testing """

# Write a value to the test and returns the specified value
test.write(test.Setting_Commands["Data_Format"], "REAL,64")
# Ouput: 'FORM REAL,64\n'

# This will rturn the value of the command by calling the read function
# Sets the data format, sends the new settings, and then reads the value
test.set_data_format("REAL,64")
test.send_all_settings()
test.read(test.Setting_Commands["Data_Format"], "REAL,64")
# Output: FORM?
#       'REAL,64'

""" Description on Test Cases """

# Setup the general settings that you want the device to use,
# All these commands below will be sent to the hardware later
test.set_measurement_function("CAP")
test.set_auto_measurement_level("ON")
test.set_trigger_level(100)
test.set_measurement_range(2e-9)
test.set_continuous_read(True)
test.set_data_format("REAL,64")

# Send all settings to the hardware. From here, the New_Settings should
# match to Settings as all of the values are copied over.
test.send_all_settings()

# Sends an ONCE command that performs an immediate autorange and then
# turns off autoranging.
# test.send_single_read()

# Selects the secondary measurement function for the current measurement
# It then collects and returns the saved data
# test.get_data()

# Save Data if interested
test.save_data('C:\\Data\\Test')

# Prints out the settings in the terminal
test.print_settings()

# Use this command to close out from using the device
# Plan to only open and close the connection once
test.close()
