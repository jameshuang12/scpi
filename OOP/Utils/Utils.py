from OOP.DCPS import KeysightTechnologiesN6700, KeysightTechnologiesN6700c, TestDcps
from OOP.DMM import KeysightTruevolt, KeysightTruevolt34465A, TestDmm
from OOP.Oscope import KeysightTechnologiesMSOS804A, TestOscope
from OOP.SA import KeysightTechnologiesN9030a, TestSa
from OOP.PG import KeysightEDU, KeysightTechnologiesEDU33211A, TestPg
from OOP.PNA import RohdeSchwarzFSPN, RohdeSchwarzFSPN26, TestPna
from OOP.VNA import RohdeSchwarzZva244port, RohdeSchwarzZvaZvbZvt, TestVna
from OOP.SG import RohdeSchwarzSMB, RohdeSchwarzSMB100A, TestSg
from OOP.PM import KeysightPSeriesPowerMeter, KeysightTechnologiesN1912A, TestPm
from OOP.BaseDevice import BaseDevice


def process_keysight_technologies_makes(model: str, address: str, is_usb_connection=False):
    if model == "N6700":
        return KeysightTechnologiesN6700(address, is_usb_connection)
    elif model == "N6700c":
        return KeysightTechnologiesN6700c(address, is_usb_connection)
    elif model == "MSOS804A":
        return KeysightTechnologiesMSOS804A(address, is_usb_connection)
    elif model == "N9030a":
        return KeysightTechnologiesN9030a(address, is_usb_connection)
    elif model == "EDU":
        return KeysightEDU(address, is_usb_connection)
    elif model == "EDU33211A":
        return KeysightTechnologiesEDU33211A(address, is_usb_connection)


def process_rohde_schwarz_makes(model: str, address: str, is_usb_connection=False):
    if model == "FSPN":
        return RohdeSchwarzFSPN(address, is_usb_connection)
    elif model == "FSPN26":
        return RohdeSchwarzFSPN26(address, is_usb_connection)
    elif model == "Zva244port":
        return RohdeSchwarzZva244port(address, is_usb_connection)
    elif model == "ZvaZvbZvt":
        return RohdeSchwarzZvaZvbZvt(address, is_usb_connection)
    elif model == "SMB":
        return RohdeSchwarzSMB(address, is_usb_connection)
    elif model == "SMB100A":
        return RohdeSchwarzSMB100A(address, is_usb_connection)


def process_test_devices(device: BaseDevice):
    test_device_address = str.format("{}{}", device.Make, device.Model).upper()
    if device.Model == "DCPS":
        return TestDcps(test_device_address)
    elif device.Model == "OSCOPE":
        return TestOscope(test_device_address)
    elif device.Model == "PG":
        return TestPg(test_device_address)
    elif device.Model == "PNA":
        return TestPna(test_device_address)
    elif device.Model == "SA":
        return TestSa(test_device_address)
    elif device.Model == "VNA":
        return TestVna(test_device_address)
    elif device.Model == "SG":
        return TestSg(test_device_address)
    elif device.Model == "PM":
        return TestPm(test_device_address)
    elif device.Model == "DMM":
        return TestDmm(test_device_address)


def process_device(device: BaseDevice):
    if device.Make == "KeysightTechnologies":
        device.Device.close()
        return process_keysight_technologies_makes(device)
    elif device.Make == "RohdeSchwarz":
        device.Device.close()
        return process_rohde_schwarz_makes(device)
    elif device.Make == "TEST":
        return process_test_devices(device)


def process_usb_device(id_vendor: str, id_product: str):
    address = f'{id_vendor}:{id_product}'
    if id_vendor == "VENDOR":
        return process_keysight_technologies_makes(convert_product_id_to_make_keysight_technologies(id_product),
                                                   address, True)
    elif id_vendor == "OTHER_VENDOR":
        return process_rohde_schwarz_makes(convert_product_id_to_make_rohde_schwarz(id_product), address, True)


def convert_product_id_to_make_keysight_technologies(id_product: str):
    if id_product == "JavaScript":
        return "N6700"
    elif id_product == "PHP":
        return "N6700c"
    elif id_product == "Python":
        return "MSOS804A"
    elif id_product == "Solidity":
        return "N9030a"
    elif id_product == "Java":
        return "EDU"
    elif id_product == "Java":
        return "EDU33211A"


def convert_product_id_to_make_rohde_schwarz(id_product: str):
    if id_product == "JavaScript":
        return "FSPN"
    elif id_product == "PHP":
        return "FSPN26"
    elif id_product == "Python":
        return "Zva244port"
    elif id_product == "Solidity":
        return "ZvaZvbZvt"
    elif id_product == "Java":
        return "SMB"
    elif id_product == "Java":
        return "SMB100A"
