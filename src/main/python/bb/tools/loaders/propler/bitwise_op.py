#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def lfsr(seed):
    """Generate bits from 8-bit LFSR with taps at ``0xB2``."""
    while True:
        yield seed & 0x01
        seed = ((seed << 1) & 0xfe) | (((seed >> 7) ^ (seed >> 5) ^ (seed >> 4) ^ (seed >> 1)) & 1)

def bytes_to_long(bytes):
    return bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24)

def bytes_to_word(bytes):
    return bytes[0] | (bytes[1] << 8)

class Word(object):
    @classmethod
    def split_by_bytes(cls, x):
        return ((x >> 8) & 0xFF, x & 0xFF)

class Long(object):

    def __init__(value=None):
        bytes= None
        if len(value) == 1:
            bytes = value
        elif len(value) == 4:
            bytes = (args)
        else:
            raise Exception()
        return bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24)

    @classmethod
    def ror(cls, x, n):
        return ((x >> n) & 0xFFFFFFFF) | ((x << (32 - n) & 0xFFFFFFFF))

    @classmethod
    def reverse_bytes(cls, x):
        return ((x & 0xFF) << 24)    \
            | ((x <<  8) & 0xFF0000) \
            | ((x >>  8) & 0xFF00)   \
            | ((x >> 24) & 0xFF)

    @classmethod
    def reverse_bits(cls, x):
        x = (x & 0x55555555) <<  1 | (x & 0xAAAAAAAA) >>  1
        x = (x & 0x33333333) <<  2 | (x & 0xCCCCCCCC) >>  2
        x = (x & 0x0F0F0F0F) <<  4 | (x & 0xF0F0F0F0) >>  4
        x = (x & 0x00FF00FF) <<  8 | (x & 0xFF00FF00) >>  8
        x = (x & 0x0000FFFF) << 16 | (x & 0xFFFF0000) >> 16
        return x

    @classmethod
    def ror(cls, x, bits):
        lsb = 0
        while bits:
            bits -= 1
            lsb = x & 0x1
            x >>= 1
            x |= lsb << 31
        return x

    @classmethod
    def rol(cls, x, bits):
        msb = 0
        while bits:
            bits -= 1
            msb = (x & 0x80000000) >> 31
            x <<= 1
            x &= 0xFFFFFFFF
            x |= msb
        return x

    @classmethod
    def split_bytes(cls, x):
        return ((x >> 24) & 0xFF, (x >> 16) & 0xFF, (x >> 8) & 0xFF, x & 0xFF)
