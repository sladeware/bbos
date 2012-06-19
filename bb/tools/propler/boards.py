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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__all__ = ["CustomBoardConfig", "QuickStartBoardConfig", "DemoBoardConfig"]

class BoardConfig(object):
    """Base board config."""

    def __init__(self):
        self.__eeprom_size = getattr(self, "EEPROM_SIZE", None)
        self.__baudrate = getattr(self, "BAUDRATE", None)
        self.__chip_version = None

    def set_chip_version(self, version):
        self.__chip_version = version

    def get_chip_version(self):
        return self.__chip_version

    def get_eeprom_size(self):
        """Return EEPROM size."""
        return self.__eeprom_size

    def get_baudrate(self):
        """Return baudrate."""
        return self.__baudrate

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
