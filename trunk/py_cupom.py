#-------------------------------------------------------------------------------
# Name:        py_cupom
# Purpose:     generate shorter case insensitive alphanumeric ids from integers
#
# Author:      Paulo Scardine
#
# Created:     09/09/2010
# Copyright:   (c) Paulo Scardine 2010
# Licence:     GNU GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

"""
This module was created to generate short alphanumeric ids for a discount cupom
application. It uses a base32 encoding that has the following attributes:

    * Case insensitive
    * Pad to a given number of digits
    * Code translates to/from valid integers
    * Does not use 'L'/'l' and 'I'/'i' to avoid mistakes
    * 5 bit per digit
    * Luhn mod N algorithm included for checksum digit generation

You can customize FW_MAP and BW_MAP to make codes harder to guess, but this
algorithm was *not* designed to be crypto safe.

Sorry, guys, only Python >= 2.6 for now.
"""

FW_MAP = {
    '01010':	'0',
    '00001':	'1',
    '00010':	'2',
    '00011':	'3',
    '00100':	'4',
    '00101':	'5',
    '00110':	'6',
    '00111':	'7',
    '01000':	'8',
    '01001':	'9',
    '00000':	'A',
    '01011':	'B',
    '01100':	'C',
    '01101':	'D',
    '01110':	'E',
    '01111':	'F',
    '10000':	'G',
    '10001':	'H',
    '10010':	'J',
    '10011':	'K',
    '10100':	'M',
    '10101':	'N',
    '10110':	'P',
    '10111':	'Q',
    '11000':	'R',
    '11001':	'S',
    '11010':	'T',
    '11011':	'V',
    '11100':	'W',
    '11101':	'X',
    '11110':	'Y',
    '11111':	'Z',
}

BW_MAP = {
    '0': '01010', 'O': '01010', 'o': '01010',
    '1': '00001', 'i': '00001', 'I': '00001', 'l': '00001', 'L': '00001',
    '2': '00010',
    '3': '00011',
    '4': '00100',
    '5': '00101',
    '6': '00110',
    '7': '00111',
    '8': '01000',
    '9': '01001',
    'A': '00000', 'a': '00000',
    'B': '01011', 'b': '01011',
    'C': '01100', 'c': '01100',
    'D': '01101', 'd': '01101',
    'E': '01110', 'e': '01110',
    'F': '01111', 'f': '01111',
    'G': '10000', 'g': '10000',
    'H': '10001', 'h': '10001',
    'J': '10010', 'j': '10010',
    'K': '10011', 'k': '10011',
    'M': '10100', 'm': '10100',
    'N': '10101', 'n': '10101',
    'P': '10110', 'p': '10110',
    'Q': '10111', 'q': '10111',
    'R': '11000', 'r': '11000',
    'S': '11001', 's': '11001',
    'T': '11010', 't': '11010',
    'V': '11011', 'v': '11011',
    'W': '11100', 'w': '11100',
    'X': '11101', 'x': '11101',
    'Y': '11110', 'y': '11110',
    'Z': '11111', 'z': '11111',
}

def digit(code):
    """Generate Luhn mod N checksum digit"""
    factor = 2
    total = 0
    n = len(FW_MAP)
    for l in code[::-1]:
        code_point = int(BW_MAP[l], 2)
        addend = factor * code_point
        factor = 1 if factor == 2 else 2
        addend = (addend / n) + (addend % n)
        total += addend
    remainder = total % n
    check_code_point = n - remainder
    check_code_point = check_code_point % n
    return FW_MAP[bin(check_code_point)[2:].rjust(5, '0')]

def check(code):
    """Checks Luhn mod N code+digit for validity"""
    factor = 1
    total = 0
    n = len(FW_MAP)
    for l in code[::-1]:
        code_point = int(BW_MAP[l], 2)
        addend = factor * code_point
        factor = 1 if factor == 2 else 2
        addend = (addend / n) + (addend % n)
        total += addend
    remainder = total % n
    return remainder == 0

def encode(n, digits=5, check_digit=False):
    """Encode integer to base 32 shorter case insensitive alphanumeric code.

Parameters:
    digits: pads to 'digits' number of digits (default=5)
    check_digit: appends Luhn mod N check digit if True (default=False).
    """
    if int(n) > decode('Z' * digits):
        raise OverflowError
    padded_bin = bin(abs(n))[2:].rjust(5*digits,'0')
    code = ''.join([ FW_MAP[padded_bin[i*5:i*5+5]] for i in range(0, digits) ])
    return code + digit(code) if check_digit else code

def decode(s):
    """Decodes an alphanumeric code to integer"""
    return int(''.join([BW_MAP[l] for l in str(s)]), 2)

def main():
    pass

if __name__ == '__main__':
    main()
