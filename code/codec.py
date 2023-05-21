#!/usr/bin/env python3

'''
Python3 codec algorithms for APRS 434 LoRa:

    - Callsign Compression CCCC
    - SSID, pathCode & Data Type Compression D

    - Callsign Compression EEEE
    - SSID & MessageNo Compression F

    - Text Compression tttt


CAVEAT ON ESP32

    Avoid deep recursive function calls.
    Individual recursive function calls do not always add a lot of stack usage each time they are called,
    but if each function includes large stack-based variables then the overhead can get quite high.

    https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/performance/ram-usage.html

'''

### IMPORTS ###

import math


### GLOBALS ###

digits = ' 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-./?@'


### FUNCTIONS ###

def encodeInteger(base, integer):
    # https://stackoverflow.com/a/23926613/2192488
    # https://github.com/numpy/numpy/blob/v1.14.2/numpy/core/numeric.py#L2067-L2120

    if base > len(digits):
        raise ValueError("The base is too large for the number of digits available.")
    elif base < 2:
        raise ValueError("The base should be at least 2.")

    integer = abs(integer)
    array   = []
    while integer:
        array.append(digits[integer % base])
        integer //= base

    return ''.join(reversed(array or ''))


def decodeInteger(base, string):

    if base > len(digits):
        raise ValueError("The base is too large for the number of digits available.")
    elif base < 2:
        raise ValueError("The base should be at least 2.")

    array   = reversed(list(string.upper()))
    integer = 0
    for e, c in enumerate(array):
        integer += digits.index(c) * base**e

    return integer


def encodeCCCC(string):

    integer = decodeInteger(37, string[-6:].ljust(6)) # Decode the 6 character Base37 string to an integer.
                                                   # The given string cannot be longer than 6 characters and
                                                   # will be right-padded with spaces if shorter.
    return integer.to_bytes(4, byteorder='big')    # Encode the integer as a 4 byte Base256 bytestring.


def decodeCCCC(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given 4 byte Base256 bytestring to an integer.

    return encodeInteger(37, integer)                           # Encode the integer as a 6 character Base37 string.


def encodeD(ssid, pathCode, dataTypeCode):

    ssid         = min(abs(ssid), 15)
    pathCode     = min(abs(pathCode), 3)
    dataTypeCode = min(abs(dataTypeCode), 3)

    integer = ssid * 16 + pathCode * 4 + dataTypeCode

    return integer.to_bytes(1, byteorder='big')    # Encode the integer as a single Base256 byte.


def decodeD(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given Base256 byte to an integer.

    ssid          = integer  // 16    # integer division
    remainder     = integer   % 16    # modulo operation
    pathCode      = remainder // 4
    dataTypeCode  = remainder  % 4

    return (ssid, pathCode, dataTypeCode)


def encodeEEEE(string):

    return encodeCCCC(string)


def decodeEEEE(bytestring):

    return decodeCCCC(bytestring)


def encodeF(ssid, messageNo):

    ssid      = min(abs(ssid), 15)
    messageNo = min(abs(messageNo), 15)

    integer = ssid * 16 + messageNo

    return integer.to_bytes(1, byteorder='big')    # Encode the integer as a single Base256 byte.


def decodeF(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given Base256 byte to an integer.

    ssid      = integer // 16
    messageNo = integer  % 16

    return (ssid, messageNo)


def encodetttt(string):

    integer = decodeInteger(42, string[:51])            # Decode the first 51 characters of the given Base42 string to an integer.

    n = math.ceil(math.log(42**len(string), 256))    # number of required Base256 bytes

    return integer.to_bytes(n, byteorder='big')      # Encode the integer as an n byte Base256 bytestring.


def decodetttt(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given Base256 bytestring to an integer.

    return encodeInteger(42, integer)                           # Encode the integer as a Base42 string.


### TESTS ###

print(encodeCCCC('ON4AA'))
print(decodeCCCC(encodeCCCC('ON4AA')))
print()
print(encodeCCCC('PA0FOT'))
print(decodeCCCC(encodeCCCC('PA0FOT')))
print()
print(encodeCCCC('cd2rxu'))
print(encodeCCCC('CD2RXU'))
print(decodeCCCC(encodeCCCC('cd2rxu')))
print()
print(encodeCCCC('W3A'))
print(decodeCCCC(encodeCCCC('W3A')))
print()
print(encodeCCCC('W3A   '))
print(decodeCCCC(encodeCCCC('W3A   ')))
print()
print(encodeCCCC('ZZZZZZ'))
print(decodeCCCC(encodeCCCC('ZZZZZZ')))
print()
print(encodeCCCC('0HN0'))
print(decodeCCCC(encodeCCCC('0HN0')))
print()
print(encodeD(6, 3, 2))
print(decodeD(encodeD(6, 3, 2)))
print()
print(encodeD(15, 3, 3))
print(decodeD(encodeD(15, 3, 3)))
print()
print(encodeD(1, 0, 0))
print(decodeD(encodeD(1, 0, 0)))
print()
print(encodeD(0, 0, 1))
print(decodeD(encodeD(0, 0, 1)))
print()
print(encodeD(0, 0, 0))
print(decodeD(encodeD(0, 0, 0)))
print()
print(encodeF(7, 13))
print(decodeF(encodeF(7, 13)))
print()
uncompressed = '0 This is ON4AA-6. QSL? @ Yes/No'
compressed = encodetttt(uncompressed)
print('%s = %d bytes' % (compressed, len(compressed)))
print('%s = %d bytes' % (decodetttt(compressed), len(uncompressed)))
print()
uncompressed = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
compressed = encodetttt(uncompressed)
print('%s = %d bytes' % (compressed, len(compressed)))
print('%s = %d bytes' % (decodetttt(compressed), len(uncompressed)))
print()
uncompressed = '@@@'
compressed = encodetttt(uncompressed)
print('%s = %d bytes' % (compressed, len(compressed)))
print('%s = %d bytes' % (decodetttt(compressed), len(uncompressed)))
print()
uncompressed = '@@@ '
compressed = encodetttt(uncompressed)
print('%s = %d bytes' % (compressed, len(compressed)))
print('%s = %d bytes' % (decodetttt(compressed), len(uncompressed)))
