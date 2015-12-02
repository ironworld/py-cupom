This module was created to generate short alphanumeric ids for a discount coupon application. It can also be useful to generate shared session keys for games and any other application where you need an easy to share alphanumeric code.

It can be used as a short hash for integers, but in fact is uses a base 32 notation that has the following attributes:

  * Collision-free 1 to 1 mapping for positive integers
  * Somewhat compact: encodes 5 bit per digit
  * Generates a case insensitive code
  * Pads to a given number of digits
  * Does not use 'L'/'l', 'I'/'i' and 'O','o' to avoid mistakes with 'zero' and 'one'.
  * Optional Luhn mod N algorithm included for checksum digit generation

Maximum range can be calculated as 32 elevated to the number of digits used.

You can customize FW\_MAP and BW\_MAP to make codes harder to guess, but this algorithm was **not** designed to be crypto safe. In my map I made 0=A because I prefer AAAY1 over 000Y1 when padding. This has some side-effects:

  * AAAAA1 == AAA1 == 1 (000001 == 0001 == 1)
  * checksum calculation also ignores any A(s) on the left

Sorry, guys, only Python >= 2.6 for now. Backporting python 2.6+ bin() is left as an exercise to the reader.

Example:
```
>> import py_cupom
>> py_cupom.encode(999999)
'YGHZ'
>> # 4 digit code
>> py_cupom.encode(999999, 6)
'AAYGHZ'
>> # 4 digit plus check
>> py_cupom.encode(999999, 4, True)
'YGHZH'
>> # Max range with 4 digit: 32**4
>> py_cupom.decode('ZZZZ')
1048575
>> py_cupom.decode('AAAAAAAYGHZ')
999999
>> py_cupom.decode('YGHZ')
999999
>> py_cupom.digit('YGHZ')
'H'
>> py_cupom.check('YGHZ')
False
>> py_cupom.check('YGHZ' + 'H')
True
```