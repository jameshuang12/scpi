from Connect import connect

# Replace 'TestVNA' with Test{devicetype} to test the code with that device type
# Replace 'TestVNA' with the IP Address of the Device to actually connect to it
device = connect("TestVNA")
device.initialize_device()

# To look through the functions that that device type has, you can import that class
# Remove/comment out these two lines when you actually want to run the code
# from VNAClass import VNAClass
# device.__class__ = VNAClass

# If you are using a device that hasn't been setup yet, or trying a function that hasn't been added
device.write("ResBW", 10000)  # Write a value to the device
device.read("ResBW")  # Device returns specified value

# Set up the settings that you want the device to use, these will be sent to the device later
device.set_points(501)
device.set_start_frequency(8000000000)  # 8 GHz
device.set_stop_frequency(10500000000)  # 10.5 GHz

# Send all settings to the device, skipping settings that have not changed
device.send_all_settings()

# Take measurement
device.get_data()

# Save Data
device.save_data('C:\\Data\\Test')

# Use this command to close out from using the device
# Plan to only open and close the connection once
device.close()
