#!/usr/bin/env python

"""The basic idea of code uploader for Parallax Propeller chip was
taken from
`uploader <http://forums.parallax.com/showthread.php?90707-Propeller-development-for-non-Windows-users>`_
proposed by Remy Blank."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

#_____________________________________________________________________

import os
import os.path
import time
import sys
import types
import optparse
import operator
import logging
import threading
from ctypes import *
try:
    import serial
except ImportError:
    print >>sys.stderr, "Please install pyserial."
    exit(0)

from bb.utils.spawn import spawn
from bb.tools.propler.image import *
from bb.tools.propler.chips import *
from bb.tools.propler.bitwise_op import *
from bb.tools.propler.boards import *

#_____________________________________________________________________

DEFAULT_SERIAL_PORTS = {
    "posix": "/dev/ttyUSB0",
    "nt": "COM1",
}
"""Default serial ports by platforms:

    ======== ================
    PLATFORM PORT
    ======== ================
    posix    **/dev/ttyUSB0**
    nt       **COM1**
    ======== ================
"""

class UploadingError(Exception):
    """Base uploading error."""
    pass

PAGE_SIZE = 1 << 9

BYTE_DELAY = float(1) / float(6000)
# End of page marker
MARKER = 0xFFFFFE

HOME_DIR = os.path.dirname(os.path.realpath(__file__))

class SPIUploaderInterface(object):
    """Base class for uploaders. Learn more about transmission protocol from
    discussion
    `"serial boot loader" <http://forums.parallax.com/showthread.php?96822-serial-boot-loader&p=670593#post670593>`_."""

    # Processor constants
    LFSR_REQUEST_LEN = 250
    LFSR_REPLY_LEN = 250
    LFSR_SEED = ord("P")

    def __init__(self, port=None, baudrate=None, timeout=0, config=None):
        if not config:
            config = CustomBoardConfig()
        self.__config = config
        # Set baudrate from board configurations if it wasn't provided
        # by user
        if not baudrate:
            baudrate = config.get_baudrate()
        # Setup serial
        if not port:
            sys.stdout.write("Please select port: ")
            port = raw_input()
        self.__serial = serial.Serial(baudrate=baudrate, timeout=timeout)
        self.__serial.port = port
        self.__serial.stopbits = 1

    def get_config(self):
        return self.__config

    def bin_to_eeprom(self, image):
        if len(image) > self.get_config().get_eeprom_size() - 8:
            raise UploadingError("Code too long for EEPROM (max %d bytes)"
                                 % (self.get_config().get_eeprom_size() - 8))
        dbase = ord(image[0x0A]) + (ord(image[0x0B]) << 8)
        if dbase > self.get_config().get_eeprom_size():
            raise UploadingError("Invalid binary format")
        image += "".join(chr(0x00) * (dbase - 8 - len(image)))
        image += "".join(chr(each) for each in [0xFF, 0xFF, 0xF9, 0xFF,
                                                0xFF, 0xFF, 0xF9, 0xFF])
        image += "".join(chr(0x00) * (self.get_config().get_eeprom_size() - len(image)))
        return image

    @property
    def serial(self):
        """Return instance of :class:`serial.Serial` that controls
        serial port."""
        return self.__serial

    def __calibrate(self):
        self.send_byte(0xF9)

    def receive_bit(self, echo, timeout):
        """Receive response from hardware via echoed byte."""
        start = time.time()
        while (time.time() - start) < timeout:
            if echo:
                self.send_byte(0xF9)
                time.sleep(0.025)
            c = self.serial.read(1)
            if c:
                if c in (chr(0xFE), chr(0xFF)):
                    return ord(c) & 0x01
                else:
                    raise Exception("Bad reply")
        raise Exception("Timeout error")

    def connect(self, config=None):
        """Find propeller on port using sync-up sequence. Return
        ``False`` on error."""
        if config:
            self.serial.baudrate = config.get_baudrate()
        self.serial.close()
        if not self.serial.isOpen():
            self.serial.open()
        self.reset()
        self.__calibrate()
        seq = []
        for (i, value) in zip(range(self.LFSR_REQUEST_LEN + self.LFSR_REPLY_LEN),
                              lfsr(self.LFSR_SEED)):
            seq.append(value)
        self.serial.write("".join(chr(each | 0xFE) for each in seq[0:self.LFSR_REQUEST_LEN]))
        # send gobs of 0xF9 for id sync-up - these clock out the LSFR
        # bits and the id
        self.serial.write(chr(0xF9) * (self.LFSR_REPLY_LEN + 8))
        # wait for response so we know we have a Propeller
        for i in range(self.LFSR_REQUEST_LEN,
                       self.LFSR_REQUEST_LEN + self.LFSR_REPLY_LEN):
            if self.receive_bit(False, 0.100) != seq[i]:
                raise Exception("No hardware found")
        version = 0
        for i in range(8):
            version = ((version >> 1) & 0x7F) | ((self.receive_bit(False, 0.050) << 7))
        print "Connected to propeller v%d on '%s'" % (version, self.__serial.port)
        if version:
            return True
        self.disconnect()
        return False

    def reset(self):
        """Reset propeller chip."""
        self.serial.flushOutput()
        self.serial.setDTR(1)
        time.sleep(0.025)
        self.serial.setDTR(0)
        time.sleep(0.090)
        self.serial.flushInput()

    def send(self, data, timeout=None):
        self.__serial.write(data)

    def send_byte(self, byte, timeout=None):
        if not type(byte) is types.StringType:
            byte = chr(byte)
        self.__serial.write(byte)
        if timeout:
            time.sleep(timeout)

    def receive(self, nbytes=1, timeout=-1):
        # Save previous value of read timeout
        old_timeout = self.__serial.timeout
        if timeout is None or timeout > 0:
            self.__serial.timeout = timeout
        nbytes = self.__serial.read(nbytes)
        self.__serial.timeout = old_timeout
        return nbytes

    def disconnect(self):
        self.serial.close()
        print "Disconnected"


class Commands:
    SHUTDOWN               = 0
    LOAD_TO_RAM_AND_RUN    = 1
    LOAD_TO_EEPROM         = 2
    LOAD_TO_EEPROM_AND_RUN = 3

class SPIUploader(SPIUploaderInterface):
    """Standard one cog uploader."""

    def __init__(self, *args, **kargs):
        SPIUploaderInterface.__init__(self, *args, **kargs)

    def upload_file(self, filename, run=True, eeprom=False):
        image = Image.extract_from_file(filename)
        self.upload_image(image, run, eeprom)

    @classmethod
    def verify_image(cls, image, eeprom=False):
        if len(image) % 4 != 0:
            raise Exception("Invalid image size: must be a multiple of 4")
        checksum = reduce(lambda a, b: a + b, (ord(each) for each in image))
        if not eeprom:
            checksum += 2 * (0xff + 0xff + 0xf9 + 0xff)
        checksum &= 0xff
        if checksum != 0:
            raise Exception("Code checksum error: 0x%.2x" % checksum)

    def upload_image(self, image, run=True, eeprom=False):
        self.verify_image(image)
        if eeprom:
            image = self.bin_to_eeprom(image)
        count_bytes = len(image)
        count_longs = count_bytes // 4
        print "Ready to transmit", count_bytes, "bytes"
        command = [Commands.SHUTDOWN, Commands.LOAD_TO_RAM_AND_RUN,
                   Commands.LOAD_TO_EEPROM, Commands.LOAD_TO_EEPROM_AND_RUN][eeprom * 2 + run]
        self.send_long(command)
        self.send_long(count_longs)
        #time.sleep(0.05)
        for i in range(0, count_bytes, 4):
            #chunk = map(ord, image[i:i+4])
            #chunk = chunk[0] | (chunk[1] << 8) | (chunk[2] << 16) | (chunk[3] << 24)
            #self.send_long(chunk)
            self.send_long(ord(image[i]) | (ord(image[i + 1]) << 8) | (ord(image[i + 2]) << 16) | (ord(image[i + 3]) << 24))
            done = float(i + 4) / float(count_bytes)
            sys.stdout.write("Downloading [{0:50s}] {1:.1f}%".format('#' * int(done * 50), done * 100))
            sys.stdout.write("\r")
            sys.stdout.flush()
        print # escape from progress bar

        # wait for checksum calculation on Propeller ... 95ms is minimum
        time.sleep(0.15)
        sys.stdout.write("Verifying... ")
        sys.stdout.flush()
        if self.receive_bit(True, 8):
            print "RAM checksum error"
            return
        print "OK"

    def send_long(self, value):
        """Transmit an encoded long word to propeller."""
        self.serial.write(self.encode_long(value))

    def encode_long(self, value):
        """Make an encoded long word to string. Encode a 32-bit long
        as short/long pulses."""
        result = []
        for i in range(10):
            result.append(chr(0x92 | (value & 0x01) | ((value & 2) << 2) | ((value & 4) << 4)))
            value >>= 3
        result.append(chr(0xf2 | (value & 0x01) | ((value & 2) << 2)))
        return "".join(result)

class MulticogSPIUploader(SPIUploaderInterface):
    """See :func:`multicog_spi_upload`.

    TODO: what do we need to do with binary images that have different
    clock speeds and modes?"""
    def __init__(self, *args, **kargs):
        SPIUploaderInterface.__init__(self, *args, **kargs)
        self.__offset = 0
        self.__total_upload_size = 0

    def upload(self, cogid_to_filename_mapping):
        # Very important to select right timeout. Non-blocking mode is
        # not allowed
        self.serial.timeout = 5
        self.__total_upload_size = 0
        # Extract and sort a list of target COG id's in increase order
        target_cogids = cogid_to_filename_mapping.keys()
        target_cogids.sort()
        # Put a little bit of useful information to the log
        # if it's required
        if True:
            logging.info("Task:")
            for cogid in target_cogids:
                path = cogid_to_filename_mapping[cogid]
                logging.info("\t%s => COG #%d", path, cogid)
                self.__total_upload_size += Image.get_file_size(path)
            print "Total upload size: %d (bytes)" % self.__total_upload_size
        # Send synch signal in order to describe target
        # number of images to be sent
        self.__send_sync_signal(len(cogid_to_filename_mapping))
        # Start uploading images on cogs one by one
        i = 0
        for cogid in target_cogids:
            filename = cogid_to_filename_mapping.get(cogid)
            if not self.__upload_to_cog(i, cogid, filename):
                raise UploadingError("Uploading has been broken.")
            i += 1

    def __send_sync_signal(self, byte):
        """Send two-bytes sync signal: [0xFF|BYTE]. These sequences can never
        be generated accidentally because during normal sending 0xFF is stuffed
        to 0xFF 0x00, so we can wait for this without the risk of accidentally
        being triggered by a program being sent to another cog."""
        assert(byte < 256)
        logging.info("Sending sync signal: 0x%4x" % ((0xFF << 8) + byte))
        #print "Sending sync signal: 0x%4x" % ((0xFF << 8) + byte)
        self.send_byte(chr(0xFF))
        self.send_byte(chr(byte))

    def stuff_and_send_byte(self, byte, timeout=None):
        if not type(byte) is types.StringType:
            byte = chr(byte)
        self.send_byte(byte, timeout)
        if byte == chr(0xFF):
            self.send_byte(chr(0), timeout)

    def stuff_and_send_long(self, x):
        bytes = x
        if type(x) is types.IntType or type(x) is types.LongType:
            bytes = Long.split_bytes(x)
        for byte in bytes:
            self.stuff_and_send_byte(byte)

    def __upload_to_cog(self, i, cogid, filename):
        # Extract image from the file
        data = Image.extract_from_file(filename)
        sz = len(data)
        if sz % 4 != 0:
            raise Exception("Invalid code size: must be a multiple of 4")
        logging.info("Uploading %s (%d bytes) on COG#%d" \
                         % (filename, sz, cogid))
        print "Uploading %s (%d bytes) on COG#%d to 0x%08x" \
            % (filename, sz, cogid, self.__offset)
        # The following blocks aims to edit binary image
        vars_size = 512 # 16
        stack_size = 1024 # 128
        # Compute an offset for working space for our program
        offset = self.__total_upload_size + i * (vars_size + stack_size)

        # Read and fix header
        # XXX: do we need to recalculate checksum value once the
        #      header has been updated?
        data_p = c_char_p(data)
        hdr_p = cast(data_p, POINTER(SpinHeader))
        hdr_p.contents.pbase = self.__offset + hdr_p.contents.pbase
        hdr_p.contents.vbase = offset + 0
        hdr_p.contents.dbase = offset + vars_size
        hdr_p.contents.pcurr = self.__offset + hdr_p.contents.pcurr
        hdr_p.contents.dcurr = offset + vars_size + 4 #offset + (vars_size + stack_size)
        #print str(hdr_p.contents)
        logging.info(str(hdr_p.contents))
        data = list(data)

        # The data may be changed till this point, thus we have to
        # double check its size
        assert(len(data) == sz)
        # Sorry, but checksum can be broken since we'are trying to
        # hack the header. Thus assert(is_valid_image(data)) is not
        # working anymore here.
        #
        # OK. Now we're starting to transmit the data...
        #
        # Send sync signal to start binary transmitting
        self.__send_sync_signal(cogid)
        # Note, that only a max of PAGE_SIZE will actually get loaded, thus
        # we split data on chunks and send them in pages
        chunks = [PAGE_SIZE] * (sz / PAGE_SIZE)
        if sz % PAGE_SIZE:
            chunks.append(sz % PAGE_SIZE)
        i = 1
        addr = 0
        page_sending_delay = 0.050
        try:
            for size in chunks:
                page = data[addr:addr + size]
                done = float(i) / float(len(chunks))
                sys.stdout.write("Downloading [{0:50s}] {1:.1f}%".format('#' * int(done * 50), done * 100))
                sys.stdout.write("\r")
                sys.stdout.flush()
                # Do not forget about total offset
                time.sleep(page_sending_delay)
                self.__send_page(cogid, i, self.__offset + addr, page, size)
                i += 1
                addr += size
            print
            self.__send_page(cogid, i, MARKER, "", 0)
        except UploadingError:
            return False
        finally:
            self.__offset += sz
        return True

    def __send_page(self, cogid, seq_no, addr, buf, size):
        """Send bytes that have to be stored to Hub RAM. Return True
        it the data from was successfully transmitted (data
        LRC-checksum should be equal to result LRC-checksum recevied
        from device)."""
        logging.info("Sending packet #%d [COG=%d, ADDR=0x%08x, SIZE=%d]" \
                        % (seq_no, cogid, addr, size))
        # 4-bytes address: [COG_ID |    ADDR   ]
        addr_hdr = (addr & 0xFFFFFF) | (cogid << 24)
        logging.info("Sending header: 0x%08x 0x%08x"
                    % (Long.reverse_bytes(addr_hdr), Long.reverse_bytes(size)))
        #print "Sending header: 0x%08x 0x%08x" \
            #% (Long.reverse_bytes(addr_hdr), Long.reverse_bytes(size))
        self.stuff_and_send_long(Long.reverse_bytes(addr_hdr))
        # Sending page 4 bytes size
        self.stuff_and_send_long(Long.reverse_bytes(size))
        # IF
        if addr == MARKER:
            self.send_byte(chr(cogid))
            return
        # LRC-checksum value (xor of each byte)
        lrc_checksum = 0x00
        # Start transmitting page bytes
        i = 0
        while i < size:
            self.stuff_and_send_byte(buf[i], timeout=BYTE_DELAY)
            # Calculate the XOR value for this byte
            lrc_checksum = operator.xor(lrc_checksum, ord(buf[i]))
            i += 1
        # Wait for calculation LRC value
        # Waiting for sync
        logging.info("Waiting for sync...")
        # Receive and verify first sync byte, should be 0xFF
        ff = self.receive(1, None)
        if not ff:
            logging.error("Timeout while expecting for '0xFF' value.")
            raise UploadingError()
        elif not ord(ff) == 0xFF:
            logging.error("PACKET#%d: expecting '0xFF' value as the first byte of sync signal, "
                         "but received '%d'", seq_no, ord(ff))
            raise UploadingError()
        # Receive and verify second sync byte. Should be our COG id.
        result_cog_id = self.receive(1) # timeout=None <== wait
        if ord(result_cog_id) != cogid:
            logging.error("Waiting for %d but received %d", cogid, ord(result_cog_id))
            raise UploadingError()
        # Receive and verify LRC value
        logging.info("Waiting for result LRC checksum value... ")
        result_lrc_checksum = ord(self.receive(1))
        logging.info("Result LRC checksum value: %d", result_lrc_checksum)
        # Compare our LRC value and result LRC value from device
        logging.info("Verifying LRC-checksum: %d and %d"
                    % (lrc_checksum, result_lrc_checksum))
        if not lrc_checksum == result_lrc_checksum:
            logging.error("LRC-checksum didn't match.")
            raise UploadingError()

def multicog_spi_upload(cogid_to_filename_mapping, serial_port,
                        force=False, bootloader_settle_delay=5):
    """Start multicog upload, instanciate uploader
    :class:`MulticogSPIUploader` and connect to the target
    device. `cogid_to_filename_mapping` represents mapping of cog to
    filename that has to be uploaded on this cog. Return uploading
    status.

    If ``force`` is defined, uploader will try to continue upload
    images until success.

    Note, the multicog bootloader has to be uploaded first before you
    will start transmitting images. See :func:`upload_bootloader`."""

    print "+--------+--------------------------------+---------+"
    print "| %6s | %30s | %7s |" % ("COG ID", "IMAGE", "SIZE")
    print "+--------+--------------------------------+---------+"
    total_size = 0
    for (cogid, filename) in cogid_to_filename_mapping.items():
        sz = Image.get_file_size(filename)
        print "| %6d | %30s | %7d |" % (cogid, filename, sz)
        total_size += sz
    print "+--------+--------------------------------+---------+"
    print "  %39s | %7d |" % (" ", total_size)
    print "                                          +---------+"

    try:
        while True:
            try:
                uploader = MulticogSPIUploader(port=serial_port)
                # Use standard connection in order to define whether
                # we have propeller device to work with
                uploader.connect()
                # If so, we no longer need this information and
                # mode. Reset propeller and wait for bootloader
                # initialization.
                uploader.reset()
                time.sleep(bootloader_settle_delay)
                uploader.upload(cogid_to_filename_mapping)
            except (KeyboardInterrupt, SystemExit):
                print # prevent overlapping with uploader's printing
                print "Process has been interrupted"
            except Exception, e:
                print
                print e
                if force:
                    continue
                else:
                    break
            break
    except (KeyboardInterrupt, SystemExit):
        print # prevent overlapping with uploader's printing
        print "Process has been interrupted"
    uploader.disconnect()

def upload_bootloader(port="/dev/ttyUSB0", config=None):
    """Upload bootloader `MULTICOG_BOOTLOADER_BINARY_FILENAME` by using
    :class:`SPIUploader`."""

    catalina_board_configs = {
        QuickStartBoardConfig : "CUSTOM",
        DemoBoardConfig : "DEMO"
        }
    if not config:
        raise Exception("Please provide config")
    catalina_config = catalina_board_configs.get(config.__class__, None)
    if not catalina_config:
        raise Exception("Cannot find catalina config for %s" %
                        config.__class__.__name__)
    bootloader_src = os.path.join(HOME_DIR, "multicog_spi_bootloader.spin")
    bootloader_binary = "multicog_spi_bootloader"
    spawn(["homespun", bootloader_src, "-b",
           "-L", "/usr/local/lib/catalina/target/",
           "-D", catalina_config,
           "-o", bootloader_binary], verbose=True)
    # Fix binary name, since '.binary' will be added automatically
    bootloader_binary += ".binary"
    uploader = SPIUploader(port=port)
    uploader.connect()
    uploader.upload_file(bootloader_binary, eeprom=True)
    uploader.disconnect()
    return uploader
