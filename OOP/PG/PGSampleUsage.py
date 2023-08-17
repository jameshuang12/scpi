""" PG SAMPLE USAGE

This module will provide background on how to test this device exactly through
the terminal. 

The module has been split into portions to help you understand how to test. 

Remember, this module is a guide used for software testing.
"""

# Locate your terminal to the correct file location
# C:\Users\"Name"\> cd "To where the file is located"
# >py

# Then, you need to import connect and set connect to a variable
from Connect import connect
# TO TEST WITH THE HARDWARE DIRECTLY
# Replace 'TestPG' with Test{devicetype} to test the code with that device type
# Replace 'TestPG' with the IP Address to test with the device directly
test = connect("TestPG")

""" Setting Commands Terminal Testing """

# Writes a value to the test and returns the specified value
test.write(test.Setting_Commands["Frequency_Period"], 1e5)
# Output:'FREQ 1e5\n'


# This will return the value of the command by calling the read function
# Sets the frequency period, sends the new settings, and then reads the value
test.set_frequency(1e5)
test.send_all_settings()
test.read(test.Setting_Commands["Frequency_Period"])
# Output: FREQ?
#         '1e5'

""" Description on Using Automated Testing """

# Setup the general settings that you want the test to use,
# All these commands below will be send to the hardware later
test.set_waveform_type("SIN")

# To get the waveform settings so you can see what values you can change
test.print_settings()

# Setup the waveform settings that you want the test to use
# these will be sent to the test later
test.set_voltage_low(0.0)
test.set_frequency(1e5)
test.set_voltage_high(2.0)
test.set_phase_parameter(90.0)
test.set_continuous_waveform(True)

# Send all settings to the hardware. From here, the New_Settings should
# match to Settings as all of the values are copied over.
test.send_all_settings()

# Send a pulse by turning on the channel and then wait 3 seconds to turn it off
test.send_pulse_output()
time.sleep(3)
test.send_pulse_output()

# Save data if interested
test.save_data('C:\\Data\\Test')

# Prints out the settings in the terminal
test.print_settings()

# Use this command to close out from using the device
# Plan to only open and close the connection once
test.close()

# INTERESTED IN AMPLITUDE OR OFFSET?
# The mathematical operation is shown below

# AMPLITUDE:
# If voltage low is negative
# Amplitude = Voltage_High
# Else:
# Amplitude = Voltage_High - Voltage_Low

# OFFSET:
# Offset = Amplitude / 2
