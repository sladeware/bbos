#!/usr/bin/env python

class PropellerP8X32(object):
    NR_COGS = 8
    RAM_SIZE = 262144

class ClockModes:
    """Valid Clock Modes."""
    RCFASE        = 0x00
    RCSLOW        = 0x01
    XINPUT        = 0x22
    XTAL1         = 0x2A
    XTAL2         = 0x32
    XTAL3         = 0x3A
    XINPUT_PLL1X  = 0x63
    XINPUT_PLL2X  = 0x64
    XINPUT_PLL4X  = 0x65
    XINPUT_PLL8X  = 0x66
    XINPUT_PLL16X = 0x67
    XTAL1_PLL1X   = 0x6B
    XTAL1_PLL2X   = 0x6C
    XTAL1_PLL4X   = 0x6D
    XTAL1_PLL8X   = 0x6E
    XTAL1_PLL16X  = 0x6F
    XTAL2_PLL1X   = 0x73
    XTAL2_PLL2X   = 0x74
    XTAL2_PLL4X   = 0x75
    XTAL2_PLL8X   = 0x76
    XTAL2_PLL16X  = 0x77
    XTAL3_PLL1X   = 0x7B
    XTAL3_PLL2X   = 0x7C
    XTAL3_PLL4X   = 0x7D
    XTAL3_PLL8X   = 0x7E
    XTAL3_PLL16X  = 0x7F

    to_string = {
        XTAL1         : "XTAL1",
        XTAL2         : "XTAL1",
        XTAL3         : "XTAL1",
        XINPUT_PLL1X  : "XINPUT_PLL1X",
        XINPUT_PLL2X  : "XINPUT_PLL2X",
        XINPUT_PLL4X  : "XINPUT_PLL4X",
        XINPUT_PLL8X  : "XINPUT_PLL8X",
        XINPUT_PLL16X : "XINPUT_PLL16X",
        XTAL1_PLL1X   : "XTAL1_PLL1X",
        XTAL1_PLL2X   : "XTAL1_PLL2X",
        XTAL1_PLL4X   : "XTAL1_PLL4X",
        XTAL1_PLL8X   : "XTAL1_PLL8X",
        XTAL1_PLL16X  : "XTAL1_PLL16X",
        XTAL2_PLL1X   : "XTAL2_PLL1X",
        XTAL2_PLL2X   : "XTAL2_PLL2X",
        XTAL2_PLL4X   : "XTAL2_PLL4X",
        XTAL2_PLL8X   : "XTAL2_PLL8X",
        XTAL2_PLL16X  : "XTAL2_PLL16X",
        XTAL3_PLL1X   : "XTAL3_PLL1X",
        XTAL3_PLL2X   : "XTAL3_PLL2X",
        XTAL3_PLL4X   : "XTAL3_PLL4X",
        XTAL3_PLL8X   : "XTAL3_PLL8X",
        XTAL3_PLL16X  : "XTAL3_PLL16X"
        }
