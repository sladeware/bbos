#!/usr/bin/env python

"""Propler."""

import os
import os.path
import time
import sys
import types
import optparse
import operator
import logging
from ctypes import *

from bb.tools.propler.formats import SpinHeader, ElfHeader, ElfContext
from bb.tools.propler.propeller_chip import PropellerP8X32
from bb.tools.propler.bitwise_op import *

try:
    import serial
except ImportError:
    print >>sys.stderr, "Please install pyserial."
    exit(0)

# Common hardware constants
EEPROM_24LC256_SIZE = 32768 # bytes

PAGE_SIZE = 1 << 9
DEFAULT_BAUDRATE = 115200 # Baud rate to use for all interprop comms
BYTE_DELAY = float(1) / float(6000)
# End of page marker
MARKER = 0xFFFFFE

READ_TIMEOUT = 5 # seconds

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

# Processor constants
LFSR_REQUEST_LEN = 250
LFSR_REPLY_LEN = 250
LFSR_SEED = ord("P")

from bb.builder.loaders import BSTLLoader

HOME_DIR = os.path.dirname(os.path.realpath(__file__))
MULTICOG_BOOTLOADER_BINARY_FILENAME = os.path.join(HOME_DIR, "multicog_spi_bootloader.binary")

class UploadingError(Exception):
    """Base uploading error."""
    pass

def upload_bootloader():
    """Upload bootloader `MULTICOG_BOOTLOADER_BINARY_FILENAME`."""
    loader = BSTLLoader(verbose=True,
                        mode=BSTLLoader.Modes.EEPROM_AND_RUN,
                        device_filename="/dev/ttyUSB0")
    loader.load(MULTICOG_BOOTLOADER_BINARY_FILENAME)

class SPIUploader(object):
    """Base class for uploaders."""

    def __init__(self, port=None):
        self.__cpu_no = None
        self.__serial = serial.Serial(baudrate=DEFAULT_BAUDRATE,
                                      timeout=READ_TIMEOUT)
        self.__serial.port = port
        self.__serial.open()

    @property
    def serial(self):
        """Return instance of :class:`serial.Serial` that controls
        serial port."""
        return self.__serial

    def __calibrate(self):
        self.send_byte(0xF9)

    def receive_bit(self, echo, timeout):
        start = time.time()
        while time.time() - start < timeout:
            if echo:
                self.send_byte(0xF9)
                time.sleep(0.025)
            c = self.__serial.read(1)
            if c:
                if c in (chr(0xFE), chr(0xFF)):
                    return ord(c) & 0x01
                else:
                    raise Exception("Bad reply")
        raise Exception("Timeout error")

    def connect(self):
        self.reset()
        self.__calibrate()
        seq = []
        for (i, value) in zip(range(LFSR_REQUEST_LEN + LFSR_REPLY_LEN),
                              lfsr(LFSR_SEED)):
            seq.append(value)
        self.__serial.write("".join(chr(each | 0xFE) for each in seq[0:LFSR_REQUEST_LEN]))
        self.__serial.write(chr(0xF9) * (LFSR_REPLY_LEN + 8))
        for i in range(LFSR_REQUEST_LEN, LFSR_REQUEST_LEN + LFSR_REPLY_LEN):
            if self.receive_bit(False, 0.100) != seq[i]:
                raise Exception("No hardware found")
        version = 0
        for i in range(8):
            version = ((version >> 1) & 0x7F) | ((self.receive_bit(False, 0.050) << 7))
        print "Connected to Propeller v%d on %s" % (version, self.__serial.port)

    def reset(self):
        self.__serial.flushOutput()
        self.__serial.setDTR(1)
        time.sleep(0.025)
        self.__serial.setDTR(0)
        time.sleep(0.090)
        self.__serial.flushInput()

    def send(self, data, timeout=None):
        self.__serial.write(data)

    def send_byte(self, byte, timeout=None):
        if not type(byte) is types.StringType:
            byte = chr(byte)
        self.__serial.write(byte)
        if timeout:
            time.sleep(timeout)

    def receive(self, nbytes=1):
        return self.__serial.read(nbytes)

    def disconnect(self):
        self.__serial.close()

def extract_image_from_file(filename):
    """Extract image from file `filename`. Developed for extracting
    image from ELF binary."""
    ctx = ElfContext(filename)
    (start, image_size) = ctx.get_program_size()
    image_buf = [chr(0)] * image_size
    # load each program section
    for i in range(ctx.hdr.phnum):
        program = ctx.load_program_table_entry(i)
        if not program:
            print "Can not load program table entry %d" % i
        buf = ctx.load_program_segment(program)
        if not buf:
            print "Can not load program section %d" % i
        for j in range(program.filesz):
            image_buf[program.paddr - start + j] = buf[j]
    img = ''.join(image_buf)
    x = c_char_p(img)
    hdr_p = cast(x, POINTER(SpinHeader))
    hdr_p.contents.vbase = image_size
    hdr_p.contents.dbase = image_size + 2 * 4
    hdr_p.contents.dcurr = hdr_p.contents.dbase + 4
    return img

class MulticogSPIUploader(SPIUploader):
    """See :func:`multicog_spi_upload`.

    TODO: what do we need to do with binary images that have different
    clock speeds and modes?"""
    def __init__(self, *args, **kargs):
        SPIUploader.__init__(self, *args, **kargs)
        self.__offset = 0
        self.__total_upload_size = 0

    def upload(self, cogid_to_filename_mapping):
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
                self.__total_upload_size += get_image_file_size(path) #os.path.getsize(path)
            print "Total upload size: %d (bytes)" % self.__total_upload_size
        # Send synch signal in order to describe target
        # number of images to be sent
        self.__send_sync_signal(len(cogid_to_filename_mapping))
        # Start uploading images on cogs one by one
        i = 0
        for cogid in target_cogids:
            filename = cogid_to_filename_mapping.get(cogid)
            if not self.__upload_to_cog(i, cogid, filename):
                print "Uploading has been broken."
                break
            i += 1

    def __send_sync_signal(self, byte):
        """Send two-bytes sync signal: [0xFF|BYTE]. These sequences can never
        be generated accidentally because during normal sending 0xFF is stuffed
        to 0xFF 0x00, so we can wait for this without the risk of accidentally
        being triggered by a program being sent to another cog."""
        assert(byte < 256)
        logging.info("Sending sync signal: 0x%4x" % ((0xFF << 8) + byte))
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
        bin_fh = open(filename)
        data = ''.join(bin_fh.readlines()) # NEW!

        ctx = ElfContext(filename)
        if ctx.hdr.is_valid():
            data = extract_image_from_file(filename)
        sz = len(data)
        #if sz % 4 != 0:
        #    raise Exception("Invalid code size: must be a multiple of 4")
        logging.info("Uploading %s (%d bytes) on Cog %d" \
                         % (filename, sz, cogid))
        print "Uploading %s (%d bytes) on COG#%d" \
            % (filename, sz, cogid)
        # The following blocks aims to edit binary image
        offset = self.__total_upload_size + i * 16

        # Read and fix header
        # XXX: do we need to recalculate checksum value once the
        #      header has been updated?
        data_p = c_char_p(data)
        hdr_p = cast(data_p, POINTER(SpinHeader))
        hdr_p.contents.pbase = self.__offset + hdr_p.contents.pbase
        hdr_p.contents.vbase = offset + 0
        hdr_p.contents.dbase = offset + 8
        hdr_p.contents.pcurr = self.__offset + hdr_p.contents.pcurr
        hdr_p.contents.dcurr = offset + 16

        logging.info(str(hdr_p.contents))
        data = list(data)

        # The data may be changed till this point. Thus we have to
        # double check it
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
        try:
            for size in chunks:
                page = data[addr:addr + size]
                done = float(i) / float(len(chunks))
                sys.stdout.write("[{0:50s}] {1:.1f}%".format('#' * int(done * 50), done * 100))
                sys.stdout.write("\r")
                sys.stdout.flush()
                # Do not forget about total offset
                self.__send_page(cogid, i, self.__offset + addr, page, size)
                i += 1
                addr += size
            print
            self.__send_page(cogid, i, MARKER, "", 0)
        except UploadingError:
            return False
        finally:
            self.__offset += sz
            bin_fh.close()
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
            # Calculate the XOR value for each byte
            lrc_checksum = operator.xor(lrc_checksum, ord(buf[i]))
            i += 1
        # Waiting for sync
        logging.info("Waiting for sync...")
        # Receive and verify first sync byte. Should be 0xFF.
        ff = self.receive(1)
        if not ff:
            logging.error("Timeout while expecting for '0xFF' value.")
            raise UploadingError()
        elif not ord(ff) == 0xFF:
            logging.error("Expecting '0xFF' value as the first byte of sync signal, "
                         "but received '%d'", ord(ff))
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

def multicog_spi_upload(cogid_to_filename_mapping, serial_port):
    """Start multicog upload, instanciate uploader
    :class:`MulticogSPIUploader` and connect to the
    target device. `cogid_to_filename_mapping` represents
    mapping of cog to filename that has to be uploaded on this cog.

    Note, the multicog bootloader has to be uploaded first before you
    will start transmitting images. See :func:`upload_bootloader`."""
    try:
        uploader = MulticogSPIUploader(port=serial_port)
        try:
            # Use standard connection in order to define whether we have
            # propeller device to work with
            uploader.connect()
            # If so, we no longer need this information and mode. Reset
            # propeller and wait for bootloader initialization.
            uploader.reset()
            time.sleep(2)
        except Exception, e:
            print e
            exit(0)
        uploader.upload(cogid_to_filename_mapping)
    except KeyboardInterrupt:
        print "Process has been interrupted"
        pass
    uploader.disconnect()

class Commands:
    SHUTDOWN            = 0
    LOAD_RAM_AND_RUN    = 1
    LOAD_EEPROM         = 2
    LOAD_EEPROM_AND_RUN = 3

class StandardSPIUploader(SPIUploader):
    """Standard one cog uploader."""

    def upload(self, data, run=True, eeprom=True):
        print "Under constraction!"
        exit(0)

        sz = len(data)
        #if sz % 4 != 0:
        #    raise Exception("Invalid code size: must be a multiple of 4")
        if not is_valid_image(data):
            raise Exception("Not valid binary image")
        print "Sending %d bytes" % sz
        if eeprom and len(data) < EEPROM_24LC256_SIZE:
            data = self.bin_to_eeprom(data, EEPROM_24LC256_SIZE)

        command = [Commands.SHUTDOWN, Commands.LOAD_RAM_AND_RUN,
                   Commands.LOAD_EEPROM, Commands.LOAD_EEPROM_AND_RUN][eeprom * 2 + run]
        self.send_long(command)
        if not eeprom and not run:
            return
        self.send_long(sz // 4)
        i = 0
        while i < len(data):
            self.send_long(ord(data[i]) | (ord(data[i + 1]) << 8) \
                               | (ord(data[i + 2]) << 16) | (ord(data[i + 3]) << 24))
            i += 4
            sys.stdout.write("Sending... %d bytes\r" % i)
        print
        if self.receive_bit(True, 8) == 1:
            raise Exception("RAM checksum error")

    def send_long(self, value):
        """Send long."""
        self.send(self.encode_long(value))

    def encode_long(self, value):
        """Encode a 32-bit long as short/long pulses."""
        result = []
        for i in range(10):
            result.append(chr(0x92 | (value & 0x01) | ((value & 2) << 2) | ((value & 4) << 4)))
            value >>= 3
        result.append(chr(0xf2 | (value & 0x01) | ((value & 2) << 2)))
        return "".join(result)

def is_valid_image_file(filename):
    """Takes file name and returns ``True`` if it is valid binary file.
    See also :func:`is_valid_image`"""
    fh = open(filename)
    data = ''.join(fh.readlines())
    is_valid = is_valid_image(data)
    fh.close()
    return is_valid

def is_valid_image(data):
    """Return ``True`` if binary image is valid. The checksum includes
    the "extra" bytes.  The extra bytes at the end are ``FF``, ``FF``,
    ``F9``, ``FF``, ``FF``, ``FF``, ``F9``, ``FF``.  These are not
    included in the binary file, or in the EEPROM.  These bytes are
    added to the beginning of the stack at run time. The extra bytes
    cause a Spin cog to jump to the ROM address ``FFF9`` when it
    terminates. The code at ``FFF9`` contains a few Spin bytecode
    instructions to get the cog ID and issue a cogstop."""
    bytes = bytearray(data)
    calc_checksum = reduce(lambda a, b: a + b, bytes)
    calc_checksum += 2 * (0xFF + 0xFF + 0xF9 + 0xFF)
    if not (calc_checksum & 0xFF):
        return True
    return False

def get_image_file_size(filename):
    """Return image size contained in file `filename`. Supports SPIN and
    ELF images."""
    ctx = ElfContext(filename)
    (start, image_size) = ctx.get_program_size()
    return image_size
