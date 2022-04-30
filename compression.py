#!/usr/bin/env python3

'''
Python3 codec algorithms for APRS 434 LoRa:

- Source Address Callsign compression CCCC
- Source Address SSID & Digipeater Address compression D

'''

### FUNCTIONS ###


def encodeCCCC(string):

    integer = int(string, 36)                      # Decode the given Base36 string to an integer.

    return integer.to_bytes(4, byteorder='big')    # Encode the integer as a 4 byte Base256 bytestring.


def decodeCCCC(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given Base256 bytestring to an integer.

    encode36 = lambda integer, numerals='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ': \
                      numerals[0] if integer == 0 \
                      else \
                      encode36(integer // 36, numerals).lstrip(numerals[0]) + numerals[integer % 36]    # Recursive!

    return encode36(integer)    # Encode the integer as a Base36 string.


def encodeD(ssid, path):

    integer = ssid * 16 + path

    return integer.to_bytes(1, byteorder='big')    # Encode the integer as a single Base256 byte.


def decodeD(bytestring):

    integer = int.from_bytes(bytestring, byteorder='big')    # Decode the given Base256 byte to an integer.

    ssid = integer // 16 
    path = integer  % 16 

    return (ssid, path)


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
print(encodeD(6, 3))
print(decodeD(encodeD(6, 3)))
print()
print(encodeD(15, 7))
print(decodeD(encodeD(15, 7)))
print()
print(encodeD(1, 0))
print(decodeD(encodeD(1, 0)))
print()
print(encodeD(0, 1))
print(decodeD(encodeD(0, 1)))
print()
print(encodeD(0, 0))
print(decodeD(encodeD(0, 0)))
