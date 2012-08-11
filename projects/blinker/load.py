#!/usr/bin/env python

from bb.tools import propler

#uploader = propler.SPIUploader(port='/dev/ttyUSB0')
#if not uploader.connect():
#  exit(1)
#uploader.upload_file('Blinker_1', eeprom=False)
#uploader.disconnect()

import time
board_config = propler.QuickStartBoardConfig()
print "Uploading bootloader"
uploader = propler.upload_bootloader('/dev/ttyUSB0', board_config)
if not uploader:
  exit(0)
  # Very important! Let bootloader to settle!
time.sleep(7)
cogid_to_filename_mapping = {
    4: 'Blinker_0',
    6: 'Blinker_1',
}
if propler.multicog_spi_upload(cogid_to_filename_mapping,
                               "/dev/ttyUSB0", force=False): #uploader.serial.port
  propler.terminal_mode()
