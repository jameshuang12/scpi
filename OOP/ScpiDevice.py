import os
import sys
import re
import socket
from datetime import datetime

import numpy as np
import logging


class ScpiDevice:
    """ This is the abstract class that will be inherited by the baseDevice
    class.
    """
    Device_Type = ""
    # Common Error Message
    ND = "This device has not been programmed for the method: \"{}\"."
    # Sets endian value to native, '>' for big endian, '<' for little endian
    Endian = '='
    # Header format is "#NB"
    # where N = number of Bytes of B and B = number of bytes of the Data
    DataHeader = "#0"

    Data = ""
    BinaryEndsWithTermination = True
    Data_Format = {}
    TrueFalseString = ["1", "0"]

    def connect(self):
        """ Checks if the connect file and module exist and will run properly.
        """
        self.log_info("Device is connecting")
        if self.Is_Usb_Connection:
            self.log_info("Device is connecting via usb")
            # self.Device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.Device.settimeout(2)
            # self.Device.connect((self.Address, 5025))
        elif self.Address[0:4] != "TEST" and self.Address is not None:
            self.log_info("Device is connecting via socket")
            self.Device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Device.settimeout(2)
            self.Device.connect((self.Address, 5025))
        else:
            self.log_info("Device is None or Test Device")
            self.Device = None

    def close(self):
        """Properly closes the connection with the device. This should also
        do the following before closing the connection:
        turn off any outputs, max any attenuators, turn off any amplifiers,
        basically anything that will make the device safe.
        If this cannot be done, a Warning message should be displayed."""
        """ Closes out the program
        """
        self.log_info("Device is closing")
        if self.Device:
            self.Device.close()

    def __init__(self, address: str, is_usb_connection = False):
        """Initializes a SCPI Device with the given address:
        IP Adress
        TEST<DeviceTypeShortHand>
        USB/PortNumber Address (TODO)
        GPIB (TODO)"""
        self.logger = logging.getLogger("Base")
        self.Device = None
        self.TChar = "\n"  # Termination Character
        self.Make = ""
        self.Model = ""
        self.Serial_Number = ""
        self.Firmware_Version = ""
        self.Settings = {}
        self.New_Settings = {}
        self.Setting_Commands = {}
        self.mode_to_command = {}
        self.Extra_Setting = {}
        self.Settings_Format = {}
        self.Common_SCPI = {
            "ClearStatus": "*CLS",
            "EventStatusEnable": "*ESE",
            "EventStatusRead": "*ESR",
            "IdentificationQuery": "*IDN",
            "IndividualStatusQuery": "*IST",
            "OperationComplete": "*OPC",
            "OptionIdentificationQuery": "*OPT",
            "PassControlBack": "*PCB",
            "ParallelPollRegisterEnable": "*PRE",
            "PowerOnStatusClear": "*PSC",
            "Reset": "*RST",
            "ServiceRequestEnable": "*SRE",
            "StatusByteQuery": "*STB",
            "Trigger": "*TRG",
            "SelfTestQuery": "*TST",
            "WaitToContinue": "*WAI"
        }

        self.Address = address.upper()
        self.Is_Usb_Connection = is_usb_connection
        self.connect()
        id_query = self.get_identification_query()

        self.Make = id_query[0]
        self.Model = id_query[1]
        self.Serial_Number = id_query[2]
        self.Firmware_Version = id_query[3]

        self.Options = self.get_option_identification_query()

    def __str__(self):
        """Sets the string of the class to the identification of the device"""
        if self.Make != "":
            firmware = self.Firmware_Version
            serial_number = self.Serial_Number
            return f"{self.Make}, {self.Model}, {serial_number}, {firmware}"
        else:
            self.log_error("This device is not connected!")
            self.close()

    "Common Methods"

    def data_format_conversion(self, value):
        """ Converts binary data into the specified data format
        """
        # TODO REAL => Floating point numbers; INT => 32 bit integer;
        #  also, all binary oscope formats are signed integers, not floats
        data_format = self.Data_Format[
            self.Settings["GeneralSettings"]["Data_Format"]]
        if data_format != 0:
            if data_format == 8:
                dt = np.dtype(np.byte)
            elif data_format == 16:
                dt = np.dtype(np.half)
            elif data_format == 32:
                dt = np.dtype(np.single)
            elif data_format == 64:
                dt = np.dtype(np.double)
            else:
                return f"Data type bit value '{data_format}' wasn't programmed"
            np.set_printoptions(precision=50, floatmode='maxprec')
            dt = dt.newbyteorder(self.Endian)
            return np.frombuffer(value, dtype=dt)
        return value

    def write(self, command: str, value=None, channel: int = -1):
        """ Write the command directly to the hardware to execute
        TODO possibility of channel and mode at same time
        """
        if value is not None:
            if isinstance(value, bool):
                if value:
                    value = self.TrueFalseString[0]
                elif not value:
                    value = self.TrueFalseString[1]
            if channel == -1:
                self.Device.send(str.encode(
                    f"{command} {value}{self.TChar}"))
            else:
                self.Device.send(str.encode(
                    f"{command} {value}{self.TChar}".format(channel)))
        else:
            self.Device.send(str.encode(f"{command}{self.TChar}"))

    def read(self, command: str, extra: str = '', channel: int = -1):
        """ Writes queries to the device and recieves the response
        TODO possibility of channel and mode at same time
        """
        # Below commented code is good for debugging, but annoyin in actual use
        # print(str.encode(f"{command}? {extra}{self.TChar}"))
        self.log_info(str.encode(f"{command}?{extra}{self.TChar}"))
        if channel == -1:
            self.Device.send(str.encode(f"{command}? {extra}{self.TChar}"))
        else:
            self.Device.send(str.encode(
                f"{command}? {extra}{self.TChar}".format(channel)))
        start_of_message = self.Device.recv(1).decode()
        if start_of_message == '#':
            number_length = int(self.Device.recv(1).decode())
            data_length = int(self.Device.recv(number_length).decode())
            self.DataHeader = f"{start_of_message}{number_length}{data_length}"
            data = self.Device.recv(data_length)
            # data_to_write = data
            while len(data) < data_length:
                more_data = self.Device.recv(data_length - len(data))
                data = data + more_data
            if self.BinaryEndsWithTermination:
                self.Device.recv(1)
            data_to_write = data
        else:
            data_to_write = f"{start_of_message}" \
                            + f"{self.Device.recv(1024).decode()}"
            while data_to_write[len(data_to_write) - 1] != "\n":
                data_to_write = f"{data_to_write}" \
                                + f"{self.Device.recv(1).decode()}"
                # print(data_to_write)
            data_to_write = data_to_write[:len(data_to_write) - 1]
        return data_to_write

    def get_all_settings(self):
        """Queries all values in self.Settings from the device and applies
        these values to self.Settings
        """
        channel = -1
        for key in self.New_Settings:
            if key != "GeneralSettings":
                if "channel" in self.New_Settings[key]:
                    channel = self.New_Settings[key]['channel']

            for setting in self.New_Settings[key]:
                try:
                    if channel > -1:
                        value = self.read(self.Setting_Commands[setting],
                                          self.Extra_Setting[setting], channel)
                    else:
                        value = self.read(self.Setting_Commands[setting],
                                          self.Extra_Setting[setting])
                except KeyError:
                    sys.exit(
                        f'KeyError was thrown. The setting, "{key}: {setting}"'
                        ' does not exist in get_all_settings.')
                if self.Settings_Format[setting] == bool:
                    if isinstance(value, bool):
                        value = bool(value)
                    elif isinstance(value, str):
                        if value[0] == "1" or value.upper() == "ON":
                            value = True
                        elif value[0] == "0" or value.upper() == "OFF":
                            value = False
                        else:
                            self.log_info(f'{key}:{setting} is a Value Error.')
                    else:
                        self.log_info(f'{key}:{setting} is a Type Error.')
                self.Settings[key][setting] \
                    = self.Settings_Format[setting](value)

    def check_settings(self):
        """Compares self.Settings and self.New_Settings
        returns a list of values that are different
        """
        self.get_all_settings()
        failed_settings = []
        for key in self.Settings:
            for setting in self.Settings[key]:
                if self.Settings[key][setting] \
                        != self.New_Settings[key][setting]:
                    failed_settings.append(f"{key}: {setting}")
        return failed_settings

    def send_all_settings(self):
        """Send all values in self.New_Settings that are different than the
        values in self.Settings, then confirms that the new settings have been
        applied to the device
        """
        start_stop_diff = []
        center_span_diff = []
        channel = -1
        for key in self.New_Settings:
            # Checks if there is a channel in the device that will be used
            # and set in setting commands
            if key != "GeneralSettings":
                if "channel" in self.New_Settings[key]:
                    channel = self.New_Settings[key]['channel']

            for setting in self.New_Settings[key]:
                same = self.New_Settings[key][setting] \
                    == self.Settings[key][setting]
                if setting == "Start_Frequency" and not same:
                    start_stop_diff.append(setting)
                elif setting == "Stop_Frequency" and not same:
                    start_stop_diff.append(setting)
                elif setting == "Center_Frequency" and not same:
                    center_span_diff.append(setting)
                elif setting == "Frequency_Span":
                    if not same:
                        center_span_diff.append(setting)
                    if len(start_stop_diff) > len(center_span_diff):
                        for diff in start_stop_diff:
                            self.write(self.Setting_Commands[diff],
                                       self.New_Settings[key][diff])
                    elif len(start_stop_diff) < len(center_span_diff):
                        for diff in center_span_diff:
                            self.write(self.Setting_Commands[diff],
                                       self.New_Settings[key][diff])
                    elif len(start_stop_diff) == len(center_span_diff) and \
                            len(start_stop_diff) > 0:
                        for diff in center_span_diff:
                            self.write(self.Setting_Commands[diff],
                                       self.New_Settings[key][diff])
                elif not same:
                    if channel > -1:
                        self.write(self.Setting_Commands[setting],
                                   self.New_Settings[key][setting], channel)
                    else:
                        self.write(self.Setting_Commands[setting],
                                   self.New_Settings[key][setting])
        failed_settings = self.check_settings()
        if len(failed_settings) > 0:
            self.log_info(
                f"These settings didn't setup properly: {failed_settings}\n")

    def vna_option_line(self):
        """ Sets the option line of the save file for a s*p formatted file.
        Needs to be updated per Device Type, may only be needed
        for VNAs? optionline_format = f"# {"HZ"} {"S"} {"RI"} {"R"} {50.00}\n"
        Used for s*p files for VNAs
        """
        return ""

    def option_line(self):
        """ Sets the option line of the save file for a s*p formatted file.
        Needs to be updated per Device Type, may only be needed
        for VNAs? optionline_format = f"# {"HZ"} {"S"} {"RI"} {"R"} {50.00}\n"
        Used for s*p files for VNAs
        """
        option_line = "!Options: "
        for i in self.Options:
            option_line = f"{option_line} {i}"
        return option_line

    def measurement_info(self, channel: str):
        """ Needs to be updated per Device Type, may not be required for all
        Creates information specific to the measurement data
        Ex. S-parameters for VNAs
        """
        return ""

    def create_data_text(self, channel: str):
        """ Needs to be updated per Device Type, may not be required for all
        Creates Header and Data Table
        """
        return ""

    def create_extension(self, channel: str):
        """ Sets file extension of save file.
        Needs to be updated per Device Type, may only be needed for VNAs?
        """
        return "txt"

    def select_channel_to_save(self, channel: str):
        """ Sets specified channel's save data to save data.
        """
        return

    def save_data(self, filename: str, comments: str = "", channel: str = "",
                  append: bool = False):
        """ Creates a standardized save file that saves all of the device
        information as well as data and comments
        Filename should be without the extension
        Ex. "filename" not "filename.txt"
        """
        settings = ""
        version = "!Version:\t0.1\n"
        dataStartLine = ""
        header = ""
        measurement = ""
        data = ""
        self.select_channel_to_save(channel)
        # TODO Figure out the option line for s2p files for VNA
        timestamp = datetime.now().strftime("%Y-%m-%d\t%H:%M:%S")
        timestamp_2 = datetime.now().strftime("-%Y%m%d-%H%M%S%f")
        # write_type = header = settings = comments = measurement = data = ''
        filename = f"{filename}{timestamp_2}.{self.create_extension('-1')}"
        if os.path.isfile(filename) and append:
            write_type = 'a'
            # TODO add settings confirmation before appending to file
        elif not os.path.isfile(filename):
            write_type = 'w'
            identification = f"{self.Make}\t{self.Model}\t \
                        {self.Firmware_Version}\t{self.Serial_Number}"
            header = f'!Make\tModel\tFirmware\tSerial Number \
                        \n!{identification}\n!Date:\t{timestamp}\n \
                        !Options:\t{self.vna_option_line()}\n'
            settings = '!Settings:'
            self.log_info(self.Settings)
            for key in self.Settings:
                for setting in self.Settings[key]:
                    settings = f"{settings}!{key}\t{setting}" \
                               f"\t{self.Settings[key][setting]}\n"
            settings = f"!Settings:\n{settings}"
            comments = f"!Comments\t{comments}\n"
            measurement = self.measurement_info(channel)
        else:
            self.log_error("File already exists")
            write_type = 'w'
            # TODO Maybe make the file be a separate file?
            # CAG-"if there is a microsecond timestamp,
            # there will never be two of the same files"
        data = self.create_data_text(channel)
        if data == "":
            dataStartLine = ""
        else:
            dataStartLine = f"{self.vna_option_line()}{version}{header}" \
                            f"{settings}{comments}{measurement}"
            dataStartLine = "!DataStartLine: {}\n".format(
                dataStartLine.count("\n") + 3)  # TODO 3 seems to be a constant
        with open(filename, write_type, encoding="utf-8") as file:
            if write_type == 'w':
                file.write(self.vna_option_line())
                file.write(version)
                file.write(dataStartLine)
                file.write(header)
                file.write(settings)
                file.write(comments)
                if measurement:
                    file.write(measurement)
            file.write(data)
            self.log_info(f'data has been written to {filename} successfully')

    "Common SCPI Commands"

    def send_clear_status(self):
        """ Sets the status byte (STB), the standard event register (ESR) and
        the EVENt -part of the QUEStionable and the OPERation registers to
        zero.
        The command doesn't alter the mask and transition parts of the
        registers.
        It clears the output buffer and the tooltip for remote
        error messages.
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["ClearStatus"])

    def send_event_status_enable(self):
        """Sets the event status enable register to the value indicated.
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["EventStatusEnable"])

    def get_event_status_enable(self):
        """Returns the contents of the event status enable register in decimal
        form.
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["EventStatusEnable"])
        else:
            return 'Event Status Enable for Test'

    def get_event_status_read(self):
        """ Returns the contents of the event status register in decimal form
        (0 to 255) and subsequently sets the register to zero.
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["EventStatusRead"])
        else:
            return 'Event Status Read for Test'

    def get_identification_query(self):
        """ Returns the instrument identification. The response is of the form
        "Make, Model, Serial_Number, Firmware_Version"
        The ID string can be changed in the System Config dialog.
        """
        if self.Address[0:4] == "TEST":
            id_query = f"{self.Address[0:4]}, {self.Address[4:]}, \
                            Serial Number, Firmware\n"
            self.Address = self.Address[:4]
        else:
            id_query = self.read(self.Common_SCPI["IdentificationQuery"])
        id_query = id_query.split(',')
        for i in range(0, len(id_query)):
            id_query[i] = re.sub(r"\s", "", id_query[i])
            if '&' in id_query[i] and i < 2:
                id_query[i] = id_query[i].replace('&', '')
            if '-' in id_query[i] and i < 2:
                id_query[i] = id_query[i].replace('-', '')
        return id_query

    def get_individual_status_query(self):
        """ Returns the contents of the IST flag in decimal form (0 | 1).
        The IST-flag is the status bit which is sent during a parallel poll.
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["IndividualStatusQuery"])
        else:
            return 'Individual Status Query for Test'

    def send_operation_complete(self):
        """ Sets bit 0 in the event status register when all preceding commands
        have been executed. This bit can be used to initiate a service request.
        The query form writes a "1" into the output buffer as soon as all
        preceding commands have been executed.
        This is used for command synchronization.
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["OperationComplete"])

    def get_operation_complete(self):
        """Writes a "1" into the output buffer as soon as all preceding
        commands have been executed. This is used for command
        synchronization.
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["OperationComplete"])
        else:
            return 'Operation Complete for Test'

    def get_option_identification_query(self):
        """ Queries the options included in the instrument and returns a
        list of the options installed. The response consists of arbitrary
        ASCII response data according to IEEE 488.2. The options are returned
        at fixed positions in a comma-separated string. A zero is returned
        for options that are not installed.
        """
        if self.Address == "TEST":
            option_query = ['Options', 'for', 'test', 'device']
        else:
            option_query = self.read(
                self.Common_SCPI["OptionIdentificationQuery"])
            option_query = option_query.replace(' ', '')
            option_query = option_query.split(',')
            option_query = [i for i in option_query if i != '0' and i != '']
        return option_query

    def send_pass_control_back(self):
        """ Indicates the controller address to which GPIB bus control
        is returned after termination of the triggered action.
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["PassControlBack"])

    def send_parallel_poll_register_enable(self):
        """ Sets parallel poll enable register to the value indicated.
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["ParallelPollRegisterEnable"])

    def get_parallel_poll_register_enable(self):
        """ Returns the contents of the parallel poll enable register in
        decimal form.
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["ParallelPollRegisterEnable"])
        else:
            return 'Parallel Poll Register Enable for Test'

    def send_power_on_status_clear(self):
        """ Determines whether the contents of the ENABle registers is
        maintained or reset when the analyzer is switched on. *PSC = 0 causes
        the contents of the status registers to be maintained. Thus a service
        request can be triggered on switching on in the case of a corresponding
        configuration of status registers ESE and SRE.
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["PowerOnStatusClear"])

    def get_power_on_status_clear(self):
        """ *PSC  0 resets the registers.
        TODO find out what the symbol is and fix it
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["PowerOnStatusClear"])
        else:
            return 'Power on Status Clear for Test'

    def send_reset(self):
        """ Sets the instrument to a defined default status by closing all
        open setups and creating a single setup "Set1" with factory-defined
        or user-defined default settings (see PRESet:USER[:STATe]).
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["Reset"])

    def send_service_request_enable(self):
        """ Sets the service request enable register to the value indicated.
        Bit 6 (MSS mask bit) remains 0. This command determines under which
        conditions a service request is triggered.
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["ServiceRequestEnable"])

    def get_service_request_enable(self):
        """ Returns the contents of the service request enable register in
        decimal form. Bit 6 is always 0.
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["ServiceRequestEnable"])
        else:
            return 'Service Request Enable for Test'

    def get_status_byte_query(self):
        """ Reads the contents of the status byte in decimal form.
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["StatusByteQuery"])
        else:
            return 'Status Byte Query for Test'

    def send_trigger(self):
        """ Triggers all actions waiting for a trigger event.
        In particular *TRG generates a manual trigger signal (Manual Trigger).
        This common command complements the commands of the TRIGger subsystem.
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["Trigger"])

    def get_self_test_query(self):
        """ Triggers selftests of the instrument and
        returns an error code in decimal form.
        """
        if self.Address != "TEST":
            return self.read(self.Common_SCPI["SelfTestQuery"])
        else:
            return 'Self Test Query for Test'

    def send_wait_to_continue(self):
        """ Prevents servicing of the subsequent commands until all
        preceding commands have been executed and all signals have settled
        (see also command synchronization and *OPC).
        """
        if self.Address != "TEST":
            self.write(self.Common_SCPI["WaitToContinue"])

    def initialize_logger(self, path: str, name: str):
        if not os.path.exists(path):
            os.mkdir(path)
        log_path = path + "/" + name
        logging.basicConfig(filename=log_path,
                            filemode="w", level=logging.DEBUG)

        # console handler
        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)
        logging.getLogger("").addHandler(console)
        self.logger = logging.getLogger(name)
        self.logger.info(name)

    def log_error(self, message):
        print(message)
        self.logger.error(message)

    def log_info(self, message):
        print(message)
        self.logger.info(message)

    def log_debug(self, message):
        print(message)
        self.logger.debug(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_critical(self, message):
        print(message)
        self.logger.critical(message)
