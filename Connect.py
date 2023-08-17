import os
import sys
import time

from OOP.BaseDevice import BaseDevice
from OOP.Utils.Utils import process_device, process_usb_device

active_usb_connections = []


def usb_connect(address: str):
    """ Takes the address of the device and connects to it.
    Should be able to connect to TCP/IP v4, USB, and GPIB
    """
    base_device = BaseDevice(address, True)
    device = process_usb_device(base_device)
    generic_make_model = f"{base_device.Make}{base_device.Model}" \
        .replace("&", "")

    if device is None:
        base_device.log_error(f"Module '{generic_make_model}' not found." +
                              " Defaulting to generic SCPI functionality.")
        active_usb_connections.append(base_device)
        return base_device
    make_model = f"{device.Make}{device.Model}".replace("&", "")

    device.log_info(f'Generic Module: "{generic_make_model}"')
    device.log_info(f'Module: "{make_model}"')
    active_usb_connections.append(device)
    return device


def connect(address: str):
    """ Takes the adrress of the device and connects to it.
    Should be able to connect to TCP/IP v4, USB, and GPIB
    """
    base_device = BaseDevice(address)
    device = process_device(base_device)
    generic_make_model = f"{base_device.Make}{base_device.Model}" \
        .replace("&", "")

    if device is None:
        base_device.log_error(f"Module '{generic_make_model}' not found." +
                              " Defaulting to generic SCPI functionality.")
        return base_device
    make_model = f"{device.Make}{device.Model}".replace("&", "")

    device.log_info(f'Generic Module: "{generic_make_model}"')
    device.log_info(f'Module: "{make_model}"')
    return device


if __name__ == "__main__":
    """ Allows for testing when run straight from this file, or allows
    arguments to be passed to confirm control from other applications
    """
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--IPAddress', help='Enter the IP Address of the \
                        device, or use TEST[Devicetype] "\nExample: "py \
                        Connect.py --IPAddress TESTVNA"', required=True)
    inputs = parser.parse_args()
    IPAddress = inputs.IPAddress
    TestDevice = connect(IPAddress)
    TestDevice.log_info(TestDevice)
    # TestDevice.Save_Data("C:\\Users\\SavageT\\test.txt")
    TestDevice.close()
