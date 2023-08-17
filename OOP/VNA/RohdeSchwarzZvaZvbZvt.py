import sys

from .VNAClass import VNAClass


# See ZVA_AVB_ZVT_OperatingManueal_en_33.pdf

class RohdeSchwarzZvaZvbZvt(VNAClass):
    def __init__(self, address: str, is_usb_connection=False):
        super().__init__(address, is_usb_connection)
        self.BinaryEndsWithTermination = True
        self.Endian = "<"

    "Commands that MAY need to be overwritten"
    # Update Initialize commands if needed

    #    def Additional_Initialization(self):
    #        self.Initialize_Values()
    #        self.send_SweepContinuous(False)

    "Commands that DO need to be overwritten"

    def send_preset(self):
        """Presets the Device
        """
        current_timeout = self.Device.gettimeout()
        self.Device.settimeout(10)
        self.write("SYST:PRES")
        self.send_wait_to_continue()
        self.Device.settimeout(current_timeout)
        self.get_all_settings()

    def send_abort(self):
        """Aborts a running measurement and resets the trigger system.
        """
        self.write("ABOR")

    def get_channels(self):
        """Returns the numbers and names of all channels in the current setup.
        """
        channels = self.read("CONF:CHAN:CAT").replace("'", "").split(",")
        # Gets the channel number by index and channel name by index + 1
        for index in range(0, len(channels), 2):
            if index % 2 == 0:
                channel_name = channels[index + 1]
                self.Settings[channel_name] = self.Channel_Settings.copy()
                self.Settings[channel_name]["channel"] = int(channels[index])
                self.get_traces(channel_name)
                self.get_s_catalog(channel_name)
                self.channel_data[channel_name] = {}
        self.get_all_settings()

    def get_traces(self, channel_name: str):
        """Returns the numbers and names of all traces in the current setup.
        """
        traces = self.read(f"CALC{self.Settings[channel_name]['channel']}:PAR:CAT"
                           ).replace("'", "").split(",")
        self.Settings[channel_name]["traces"] = []
        for trace in range(int(len(traces)/2)):
            self.Settings[channel_name]["traces"].append(traces[trace * 2 + 1])

    def send_initiate(self):
        """Initiates a sweep when the device is not in continuous sweep
        """
        self.write("INIT:IMM")

    def get_s_catalog(self, channel_name: str):
        """Returns all S-Parameters which are available for
        CALCulate<Ch>:DATA:CALL? in channel no. <Ch>.
        """
        s_parms = self.read(f"CALC{self.Settings[channel_name]['channel']}:DATA:"
                            "CALL:CAT").replace("'", "").split(",")
        self.Settings[channel_name]["SParameters"] = s_parms

    def send_configure_channel(self, name: str, on: bool = True):
        """Creates or deletes channel no. <Ch> and selects it as the active
        channel.
        """
        channels = []
        for key in self.Settings:
            if key != "GeneralSettings":
                channels.append(int(self.Settings[key]["channel"]))
        i = 1
        while i in channels:
            i += 1
        channel = 1
        self.Settings[name] = self.Channel_Settings.copy()
        self.Settings[name]["channel"] = channel
        self.write(f"CONF:CHAN{self.Settings[name]['channel']}", on)
        self.send_channel_rename(name, channel)

    def send_channel_rename(self, channel_name: str, new_name: str,):
        """Assigns a name to channel number <Ch>. The channel must be created
        before (CONFigure:CHANnel<Ch>[:STATe] ON). Moreover it is not possible
        to assign the same name to two different channels.
        """
        self.write(f"CONF:CHAN{self.Settings[channel_name]['channel']}:NAME",
                   f" '{new_name}'")
        self.Settings[new_name] = self.Settings[channel_name].copy()
        del self.Settings[channel_name]

    def get_data(self, channel_name: str = ""):
        """Reads the current response values of all S-parameter data traces in
        channel no. <Ch>. If a full n-port system error correction (TOSM, TOM,
        TRL ...) is active in this channel, the command reads the full nxn
        Smatrix of the calibrated ports (there is no need to create or display
        the S-parameter traces). Use CALCulate<Ch>:DATA:CALL:CATalog? to query
        the available traces.
        """
        # TODO add default function for channel = ""
        current_timeout = self.Device.gettimeout()
        if not self.Settings["GeneralSettings"]["Sweep_Continuous"]:
            self.Device.settimeout(self.Settings["GeneralSettings"]
                                   ["SweepTime"] + 2)
            self.send_wait_to_continue()
        datatype = f" {datatype}"
        self.save_channel(channel_name, self.read(
            f"CALC{self.Settings[channel_name]['channel']}:DATA:CALL", " SDAT"))
        self.Device.settimeout(current_timeout)

    def get_group_s_data(self, channel_name: str, datatype: str = "SDAT"):
        """Reads the current response values of all S-parameters associated to
        a group of logical ports (S-parameter group). The S-parameter group
        must be created before using CALCulate<Ch>:PARameter:DEFine:SGRoup.
        """
        data_types = {"FDAT", "SDAT", "MDAT"}
        if datatype.upper() not in data_types:
            sys.exit(f"Format must be on of these:\n{data_types}")
        else:
            datatype = f" {datatype}"
            return self.read(f"CALC{self.Settings[channel_name]['channel']}:"
                             "DATA:SGR", f" {datatype}")
            # TODO Fix above line, it does not work
            # probably because CALC:PAR:DEF:SGR was not defined

    def get_stimulus(self, channel_name: str):
        """Reads the stimulus values of the active data or memory trace.
        """
        self.Settings[channel_name]["stimulus"] = self.read(
            f"CALC{self.Settings[channel_name]['channel']}:DATA:STIM")

    def send_display_format(self, channel_name: str, display_format: str = "MLOG"):
        """Defines how the measured result at any sweep point is
        post-processed and presented in the graphical display.
        """
        valid_format = {"MLIN", "MLOG", "PHAS", "UPH", "POL", "SMIT", "ISM",
                        "GDEL", "REAL", "IMAG", "SWR", "COMP", "MAGN"}
        if display_format.upper() not in valid_format:
            sys.exit(f"Format must be on of these:\n{valid_format}")
        else:
            self.write(f"CALC{self.Settings[channel_name]['channel']}:"
                       f"FORM {display_format}")

    def send_define_trace(self, channel_name: str, trace_name: str,
                          measured_quantity: str):
        """Creates a trace and assigns a channel number, a name and a measured
        quantity to it. The trace becomes the active trace in the channel but
        is not displayed.
        """
        if trace_name == "" or measured_quantity == "":
            sys.exit("TraceName and MeasuredQuantity must not be blank")
        # TODO Ensure TraceName is good
        # TODO Ensure MeasuredQuantity is good
        self.write(f"CALC{self.Settings[channel_name]['channel']}:PAR:SDEF "
                   f"'{trace_name}', '{measured_quantity}'")

    def get_all_usb_cal_units(self):
        """Queries the names (USB addresses) of all connected calibration
        units.
        """
        return self.read("SYST:COMM:RDEV:AKAL:ADDR:ALL")

    def send_delete_trace(self, channel_name: str, trace_name: str):
        """Deletes a trace with a specified trace name and channel."""
        if trace_name == "":
            sys.exit("TraceName must not be blank")
        self.write(f"CALC{self.Settings[channel_name]['channel']}:PAR:DEL "
                   f"'{trace_name}'")

    def send_open_window(self, window: int, on: bool = True):
        """Creates or deletes a diagram area, identified by its area number
        <Wnd>.
        """
        self.write(f"DISP:WIND{window}:STAT {int(on)}")

    def send_assign_trace(self, window: int, trace_name: str):
        """Assigns an existing trace (CALCulate<Ch>:PARameter:SDEFine
        <Trace_Name>) to a diagram area <Wnd>, and displays the trace. Use
        DISPlay[:WINDow<Wnd>]:TRACe<WndTr>:FEED to assign the trace to a
        diagram area using a numeric suffix (e.g. in order to use the
        DISPlay[:WINDow<Wnd>]:TRACe<WndTr>:Y:OFFSet command).
        """
        self.write(f"DISP:WIND{window}:TRAC:EFE '{trace_name}'")

    def send_trace_power_division(self, power_per_division: float,
                                  trace_name: str):
        """Sets the value between two grid lines (value “per division”) for
        the diagram area <Wnd>. When a new PDIVision value is entered, the
        current RLEVel is kept the same, while the top and bottom scaling is
        adjusted for the new PDIVision value.
        """
        self.write(f"DISP:TRAC1:Y:PDIV {power_per_division}, '{trace_name}'")

    def send_trace_reference_level(self, reference_level: float,
                                   trace_name: str):
        """Sets the reference level (or reference value) for a particular
        displayed trace. Setting a new reference level does not affect the
        value of PDIVision. The trace can be referenced either by its number
        <WndTr> or by its name <trace_name>. #TODO does not seem to do anything
        """
        self.write(f"DISP:TRAC1:Y:PREF {reference_level}, '{trace_name}'")

    def send_trace_reference_position(self, reference_position: float,
                                      trace_name: str):
        """Sets the point on the y-axis to be used as the reference position
        as a percentage of the length of the y-axis. The reference position is
        the point on the y-axis which should equal the RLEVel.
        """
        # TODO fix this
        self.write(f"DISP:TRAC1:Y:RPOS {reference_position}, '{trace_name}'")

    def send_annotate_frequencies(self, on: bool = True):
        """Shows or hides all frequency stimulus values in the diagrams. Does
        not seem to be needed for Automation, but defaults to on anyway
        """
        self.write(f"DISP:ANN:FREQ {int(on)}")

    def send_annotate_channels(self, on: bool = True):
        """Shows or hides the channel list below the diagrams. Does not seem
        to be needed for Automation, but defaults to on anyway
        """
        self.write(f"DISP:ANN:CHAN {int(on)}")

    def send_calbrate_vna(self, channel: str, cal_kit_file: str = "",
                          ports: str = "1,2"):
        """Initiates a one-port, two-port, three-port or four-port automatic
        calibration at arbitrary analyzer and cal unit ports.
        """
        # TODO add device timeout increase
        self.write(f"SENS{self.Settings[channel]['channel']}:CORR:COLL:AUTO "
                   f"'{cal_kit_file}',{ports}")
        self.send_wait_to_continue()

    def send_calibrate_vna_settings(self, cal_type: str = "FNP",
                                    cal_kit_file: str = ""):
        """Selects a calibration type and a cal unit characterization
        (cal kit file) for an automatic calibration with multiple port
        assignments.
        """
        cal_types = {"FNP", "FOP", "OPTP"}
        if cal_type.upper() not in cal_types:
            self.log_error(f'Cal type must be on of these:\n{cal_types}')
        else:
            self.write(f"CORR:COLL:AUTO:CONF {cal_type}, '{cal_kit_file}'")

    def send_change_directory(self, directory_name: str = ""):
        """Changes the current directory for mass memory storage.
        """
        if directory_name == "":
            directory_name = "DEF"
        else:
            directory_name = f"'{directory_name}'"
        self.write(f"MMEM:CDIR {directory_name}")

    def get_directory(self):
        """Returns the current directory for the mass memory storage.
        """
        return self.read("MMEM:CDIR")

    def send_create_directory(self, directory_name: str):
        """Creates a new subdirectory for mass memory storage in an existing
        directory.
        """
        if directory_name:
            self.write(f"MMEM:MDIR '{directory_name}'")
            self.write(f"MMEM:MDIR '{directory_name}'")

    def send_create_directory_path(self, directory_name: str):
        """Follows and creates directories as needed to create full path
        """
        path = directory_name.split('\\')
        current_path = f"{path[0]}"
        self.send_change_directory(f"{path[0]}\\")
        for x in path[1:]:
            current_path = f'{current_path}\\{x}'
            self.send_change_directory(x)
            if f"'{current_path}'\n" != self.get_directory():
                self.send_create_directory(x)
                self.send_change_directory(x)
                if self.get_directory() != current_path:
                    sys.exit("Directory Path could not be created.\nCurrent "
                             f"Directory= {self.get_directory()}\nDirectory "
                             f"attempt= '{current_path}'")

    def send_store_configuration_data(self, file_name: str):
        """Stores the configuration data of the current setup to a specified
        setup file.
        """
        self.write(f"MMEM:STOR:STAT 1, '{file_name}'")
