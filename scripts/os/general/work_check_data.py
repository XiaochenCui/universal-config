#!/usr/bin/env python3
import time
import struct
from datetime import datetime

from munch import Munch


def bytes_to_int(byte, byte_order=">"):
    """
    :type byte: str
    :type byte_order: str
    """
    if len(byte) == 1:
        format_flag = "B"
    elif len(byte) == 2:
        format_flag = "H"
    elif len(byte) == 4:
        format_flag = "L"
    format_string = byte_order + format_flag
    return struct.unpack(format_string, byte)[0]


def unix_timestamp(time_field):
    """
    Deconstruct time field in package, return unix timestamp in int
    :type time_field: str
    :rtype: int
    """
    year = 2000 + bytes_to_int(time_field[0])
    month = bytes_to_int(time_field[1])
    day = bytes_to_int(time_field[2])
    hour = bytes_to_int(time_field[3])
    minute = bytes_to_int(time_field[4])
    second = bytes_to_int(time_field[5])

    dt = datetime(year, month, day, hour, minute, second)
    return int(time.mktime(dt.timetuple()))


def validate_package(package):
    """
    Validate a package
    :param data: package content
    :type data: string
    """
    from utils.checksum import bcc

    if bcc(package.raw_data[2:-1]) != package.checksum:
        raise ValidateError(
            "BCC verification failed: {}".format(package.raw_data.encode("hex"))
        )
    if package.length != len(package.payload):
        raise ValidateError(
            (
                "Package length not valid, declared length:"
                " {length}, actual length: {actual_length}".format(
                    length=package.length, actual_length=len(package.payload),
                )
            )
        )


class ValidateError(Exception):
    pass


def deconstruct_package(data):
    """
    Deconsturct a package, return d dict
    :param data: package conent
    :type data: str
    :rtype: dict
    """
    if len(data) < 31:
        raise ValidateError(
            "Package length not validate: {}".format(data.encode("hex"))
        )
    package = Munch()
    package.start = data[0:2]
    package.command_flag = bytes_to_int(data[2])
    package.answer_flag = bytes_to_int(data[3])
    package.unique_code = data[4:21]
    package.encrypto_method = bytes_to_int(data[21])
    package.length = bytes_to_int(data[22:24])
    package.payload = data[24:-1]
    package.checksum = bytes_to_int(data[-1])

    package.raw_data = data
    package.timestamp = data[24:30]
    return package


def validate(data):
    data = data.decode("hex")
    try:
        package = deconstruct_package(data)
    except Exception:
        print(("Package length not validata: {}".format(len(data))))
        return

    print(("Payload length: {}".format(package.length)))
    print(("Payload actual length: {}".format(len(package.payload))))
    print(("Vin: {}".format(package.unique_code)))
    dt = package.payload[:6]
    timestamp = unix_timestamp(dt)
    print(("Timestamp: {}".format(timestamp)))
    print(("Datetime: {}".format(datetime.fromtimestamp(int(timestamp)))))
    try:
        validate_package(package)
    except ValidateError as e:
        print(e)


if __name__ == "__main__":
    while True:
        data = input("data:\n")
        validate(data)
