#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__all__ = ["CustomBoardConfig", "QuickStartBoardConfig", "DemoBoardConfig"]

class BoardConfig(object):
    """Base board config."""

    def get_eeprom_size(self):
        """Return EEPROM size."""
        return self.EEPROM_SIZE

    def get_baudrate(self):
        """Return baudrate."""
        return self.BAUDRATE

class DemoBoardConfig(BoardConfig):
    """Propeller Demo Board configuration:

    .. image:: http://www.parallax.com/DesktopModules/CATALooKStore/MakeThumbImage.aspx?ID=%2fPortals%2f0%2fImages%2fProd%2f3%2f321%2f32100-M.jpg&PORTALID=0&W=120&H=120

    ===========  ======
    Property     Value
    ===========  ======
    BAUDRATE     115200
    EEPROM_SIZE  32768
    ===========  ======
    """
    BAUDRATE = 115200
    EEPROM_SIZE = 32768

class QuickStartBoardConfig(BoardConfig):
    """QuickStart board configuration:

    .. image:: http://www.parallax.com/DesktopModules/CATALooKStore/MakeThumbImage.aspx?ID=%2fPortals%2f0%2fImages%2fProd%2f4%2f400%2f40000-M.jpg&PORTALID=0&W=120&H=120

    ===========  ======
    Property     Value
    ===========  ======
    BAUDRATE     115200
    EEPROM_SIZE  32768
    ===========  ======
    """
    BAUDRATE = 115200
    EEPROM_SIZE = 32768

class CustomBoardConfig(BoardConfig):
    """Just a custom board."""
    EEPROM_SIZE = 32768
    # Baud rate to use for all interprop communications
    BAUDRATE = 115200
