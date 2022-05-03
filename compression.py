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


### FUNCTIONS ###


def encodeCCCC(string):

    integer = int(string, 36)                      # Decode the given 6 character Base36 string to an integer.
                                                   # Base36 is the maximum allowed base for int(string, base).

    return integer.to_bytes(4, byteorder='big')    # Encode the integer as a 4 byte Base256 bytestring.


def decodeCCCC(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given 4 byte Base256 bytestring to an integer.

    # https://stackoverflow.com/a/70416418/2192488
    encode36 = lambda integer, numerals='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ': \
                      '0' if integer == 0 \
                      else \
                      encode36(integer // 36, numerals).lstrip('0') + numerals[integer % 36]    # Recursive!

    return encode36(integer)    # Encode the integer as a 6 character Base36 string.


def encodeD(ssid, pathCode, dataTypeCode):

    integer = ssid * 16 + pathCode * 4 + dataTypeCode

    return integer.to_bytes(1, byteorder='big')    # Encode the integer as a single Base256 byte.


def decodeD(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given Base256 byte to an integer.

    ssid      = integer // 16    # integer division
    remainder = integer  % 16    # modulo operation
    pathCode      = remainder // 4
    dataTypeCode  = remainder  % 4

    return (ssid, pathCode, dataTypeCode)


def encodeEEEE(string):

    return encodeCCCC(string)


def decodeEEEE(bytestring):

    return decodeCCCC(bytestring)


def encodeF(ssid, messageNo):

    integer = ssid * 16 + messageNo

    return integer.to_bytes(1, byteorder='big')    # Encode the integer as a single Base256 byte.


def decodeF(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given Base256 byte to an integer.

    ssid      = integer // 16    # integer division
    messageNo = integer  % 16    # modulo operation

    return (ssid, messageNo)


def encodetttt(string):

    decode42 = lambda string, numerals='0123456789abcdefghijklmnopqrstuvwxyz .?-/_': \
                      0 if string == '' \
                      else \
                      decode42(string = string[:-1]) * 42 + numerals.index(string[-1].lower())    # Recursive!

    integer = decode42(string)                       # Decode the given Base42 string to an integer.

    n = math.ceil(math.log(42**len(string), 256))    # number of required Base256 bytes

    return integer.to_bytes(n, byteorder='big')      # Encode the integer as an n byte Base256 bytestring.


def decodetttt(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given Base256 bytestring to an integer.

    encode42 = lambda integer, numerals='0123456789abcdefghijklmnopqrstuvwxyz .?-/_': \
                      '0' if integer == 0 \
                      else \
                      encode42(integer // 42, numerals).lstrip('0') + numerals[integer % 42]    # Recursive!

    return encode42(integer)    # Encode the integer as a Base42 string.


### TESTS ###


print(encodeCCCC('PA0FOT'))
print(decodeCCCC(encodeCCCC('PA0FOT')))
print()
print(encodeCCCC('pa3fkm'))
print(decodeCCCC(encodeCCCC('pa3fkm')))
print()
print(encodeCCCC('ON4AA'))
print(decodeCCCC(encodeCCCC('ON4AA')))
print()
print(encodeCCCC('W3A'))
print(decodeCCCC(encodeCCCC('W3A')))
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
uncompressed = 'This is ON4AA-6. QSL? _ Yes/No'
compressed   = encodetttt(uncompressed)
print('%s = %d bytes' % (compressed, len(compressed)))
print('%s = %d bytes' % (decodetttt(compressed), len(uncompressed)))
