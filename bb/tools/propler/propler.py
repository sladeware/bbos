#!/usr/bin/env python

import os
import time
import sys
import types
import optparse
import operator
import logging

from formats import SpinHeader, ElfHeader, ElfContext
from propeller_chip import PropellerP8X32

from ctypes import *
from bitwise_op import *

try:
    import serial
except ImportError:
    print >>sys.stderr, "Please install pyserial."
    exit(0)

# Initialize logger
#logger = logging.getLogger()

# Common hardware constants
EEPROM_24LC256_SIZE = 32768 # bytes

PAGE_SIZE = 1 << 9
DEFAULT_BAUDRATE = 115200 # Baud rate to use for all interprop comms
BYTE_DELAY = float(1) / float(6000)
# End of page marker
MARKER = 0xFFFFFE

READ_TIMEOUT = 5 # seconds

# Default serial ports by platforms
DEFAULT_SERIAL_PORTS = {
    "posix": "/dev/ttyUSB0",
    "nt": "COM1",
}

# Processor constants
LFSR_REQUEST_LEN = 250
LFSR_REPLY_LEN = 250
LFSR_SEED = ord("P")

#_______________________________________________________________________________

class UploadingError(Exception):
    pass

#_______________________________________________________________________________

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

#_______________________________________________________________________________

class Config(object):

    class Action(object):
        """Describes information about a command line action."""
        def __init__(self, function, usage, short_desc, long_desc='',
                     error_desc=None, options=lambda obj, parser: None,
                     uses_basepath=True):
            """Initializer for the class attributes."""
            self.function = function
            self.usage = usage
            self.short_desc = short_desc
            self.long_desc = long_desc
            self.error_desc = error_desc
            self.options = options
            self.uses_basepath = uses_basepath

        def __call__(self, cfg):
            """Invoke this Action on the specified Config.

            This calls the function of the appropriate name on Config, and
            respects polymophic overrides.

            Returns the result of the function call."""
            #method = getattr(cfg, self.function)
            #return method()
            return self.function(cfg)

    actions = dict()

    @classmethod
    def action(cls, name, **kargs):
        def action_catcher(function):
            cls.actions[name] = Config.Action(function, **kargs)
            return function
        return action_catcher

    def __init__(self, argv):
        """Initializer. Parses the command line and selects the action
        to use."""
        self.argv = argv
        self.parser = self.__get_option_parser()
        self.parser.disable_interspersed_args()
        # Copy supported actions
        self.actions = Config.actions

        #for action in self.actions.itervalues():
        #    action.options(self, self.parser)

        self.options, self.args = self.parser.parse_args(argv[1:])
        if len(self.args) < 1:
            self.print_help_and_exit()

        # Parse action
        action = self.args.pop(0)
        if action not in self.actions:
            self.parser.error("Unknown action: '%s'\n%s" %
                              (action, self.parser.get_description()))
        self.action = self.actions[action]

        if self.options.help:
            self.print_help_and_exit()

        self.parser, self.options = self.action_related_parser(self.action)

        if self.options.help:
            self.print_help_and_exit()

        if self.options.output_file:
            if os.path.exists(self.options.output_file):
                os.remove(self.options.output_file)
            hdlr = logging.FileHandler(self.options.output_file)
            logging.getLogger().addHandler(hdlr)
        else:
            logging.getLogger().addHandler(logging.NullHandler())
        # Setup logging level
        logging.getLogger().setLevel(logging.DEBUG)

        # Execute required action
        self.action(self)

    def action_related_parser(self, action):
        """Creates parser with documentation specific to 'action'."""
        parser = self.__get_option_parser()
        parser.set_usage(action.usage)
        parser.set_description('%s\n%s' % (action.short_desc, action.long_desc))
        action.options(self, parser)
        options, self.args = parser.parse_args(self.args) # XXX
        return parser, options

    def print_help_and_exit(self, exit_code=2):
        self.parser.print_help()
        sys.exit(exit_code)

    def get_action_descriptions(self):
        """Returns a formatted string containing the short_descs for all actions."""
        action_names = self.actions.keys()
        action_names.sort()
        desc = ''
        for action_name in action_names:
            desc += '  %s: %s\n' % (action_name, self.actions[action_name].short_desc)
        return desc

    def __get_option_parser(self):

        class Formatter(optparse.IndentedHelpFormatter):
            """Custom help formatter that does not reformat the description."""

            def format_description(self, description):
                """Very simple formatter."""
                return description + '\n'

        desc = self.get_action_descriptions()
        desc = ('Action must be one of:\n%s'
                'Use \'help <action>\' for a detailed description.') % desc

        parser = optparse.OptionParser(
            prog=os.path.basename(self.argv[0]),
            usage="%prog [options] <action>",
            description=desc,
            formatter=Formatter(),
            add_help_option=False,
            )
        parser.add_option("-h", "--help", action="store_true", dest='help',
                          help="Show this help message and exit.")
        parser.add_option("-o", "--output-file", action="store",
                          dest="output_file",
                          help="Log message to file.")
        return parser

class ActionOptions(object):
    @classmethod
    def upload_options(cls, cfg, parser):
        parser.add_option("-s", "--serial-port", dest="serial_port", nargs=1,
                          type="string", metavar="DEVICE",
                          default=DEFAULT_SERIAL_PORTS.get(os.name, "none"),
                          help="Select the serial port device. The default is %default.")

    @classmethod
    def multicog_spi_upload_options(cls, cfg, parser):
        cls.upload_options(cfg, parser)
        for cogid in range(1, PropellerP8X32.NR_COGS + 1):
            parser.add_option("-%d" % cogid, "--cog%d" % cogid,
                              dest="cog%d" % cogid, nargs=1, type="string",
                              metavar="filename", default=None,
                              help="Select filename to be loaded. The default is %default.")

#_______________________________________________________________________________

@Config.action('help', usage='%prog help <action>',
               short_desc='Print help for a specific action.',
               uses_basepath=False)
def help(cfg, action=None):
    """Prints help for a specific action.

    Expects cfg.args[0], or 'action', to contain the name of the action in
    question. Exits the program after printing the help message."""
    if not action:
        if len(cfg.args) != 1 or cfg.args[0] not in cfg.actions:
            cfg.parser.error('Expected a single action argument. ' +
                             'Must be one of:\n' +
                             cfg.get_action_descriptions())
        action = cfg.args[0]
    action = cfg.actions[action]
    cfg.parser, unused_options = cfg.action_related_parser(action)
    cfg.print_help_and_exit(exit_code=0)

#_______________________________________________________________________________

def is_valid_binary_file(filename):
    fh = open(filename)
    data = ''.join(fh.readlines())
    is_valid = is_valid_binary_image(data)
    fh.close()
    return is_valid

def is_valid_binary_image(data):
    bytes = bytearray(data)
    calc_checksum = reduce(lambda a, b: a + b, bytes)
    # The checksum includes the "extra" bytes.
    # The extra bytes at the end are $FF, $FF, $F9, $FF, $FF, $FF, $F9, $FF.
    # These are not included in the binary file, or in the EEPROM.
    # These bytes are added to the beginning of the stack at run time. The
    # extra bytes cause a Spin cog to jump to the ROM address $FFF9 when it
    # terminates. The code at $FFF9 contains a few Spin bytecode instructions
    # to get the cog ID and issue a cogstop.
    calc_checksum += 2 * (0xFF + 0xFF + 0xF9 + 0xFF)
    if not (calc_checksum & 0xFF):
        return True
    return False

@Config.action('dump_header',
               usage="",
               short_desc='Dump header information for binary file.',
               uses_basepath=False)
def dump_header(cfg, run_fn=None):
    # http://forums.parallax.com/showthread.php?117526-eeprom-file-format
    fname = cfg.args.pop(0)
    print "Binary file : %s" % fname
    fh = open(fname)
    data = ''.join(fh.readlines())
    print "Size        : %d (bytes)" % len(data)

    hdr = None

    if fname.endswith(".elf"):
        hdr = ElfHeader()
        memmove(addressof(hdr), data, sizeof(ElfHeader))
    else:
        hdr = SpinHeader()
        memmove(addressof(hdr), data, sizeof(SpinHeader))
    print str(hdr)

    fh.close()
    exit(0)

#_______________________________________________________________________________

@Config.action('edit_header',
               usage="",
               short_desc='Edit header information for binary file.',
               uses_basepath=False)
def edit_header(cfg, run_fn=None):
    pass

@Config.action('get_image_size',
               usage="",
               short_desc="Get image size.",
               uses_basepath=False)
def _get_image_size(cfg, run_fn=None):
    pass

def get_image_size(filename):
    ctx = ElfContext(filename)
    (start, image_size) = ctx.get_program_size()
    return image_size

@Config.action('extract_binary_image',
               usage="",
               short_desc='Extract binary image from ELF.',
               uses_basepath=False)
def extract_binary_image(cfg, run_fn=None):
    src_fname = cfg.args.pop(0)
    dst_fname = cfg.args.pop(0)

    print "Source file: %s (%d bytes)" % (src_fname, os.path.getsize(src_fname))

    ctx = ElfContext(src_fname)
    (start, image_size) = ctx.get_program_size()
    print "Image start: 0x%08x" % start
    print "Image size: %d byte(s)" % image_size

    image_buf = [chr(0)] * image_size

    # load each program section
    for i in range(ctx.hdr.phnum):
        program = ctx.load_program_table_entry(i)
        if not program:
            print "Can not load program table entry %d" % i
        print "Load program table entry", i
        print str(program)
        buf = ctx.load_program_segment(program)
        if not buf:
            print "Can not load program section %d" % i
        for j in range(program.filesz):
            image_buf[program.paddr - start + j] = buf[j]

    # fixup the header to point past the spin bytecodes and generated PASM code
    #hdr = SpinHeader()
    #memmove(addressof(hdr), ''.join(image_buf), sizeof(SpinHeader))
    #print  hdr.clk_speed
    #hdr.vbase = image_size #Word.split_by_bytes(image_size)
    #hdr.dbase = image_size + 2 * 4 #Word.split_by_bytes(image_size + 2 * 4) # stack markers
    #hdr.dcurr = hdr.dbase + 4 #Word.split_by_bytes(hdr.dbase + 4)
    #image_buf = list(hdr) + image_buf[sizeof(SpinHeader):]

    img = ''.join(image_buf)
    x = c_char_p(img)
    hdr_p = cast(x, POINTER(SpinHeader))
    hdr_p.contents.vbase = image_size
    print hdr_p.contents.clk_speed
    hdr_p.contents.dbase = image_size + 2 * 4
    hdr_p.contents.dcurr = hdr_p.contents.dbase + 4

    print "Writing image to the destination file:", dst_fname
    dst_fh = open(dst_fname, "w")
    dst_fh.write(img)#"".join(image_buf))
    dst_fh.close()

#_______________________________________________________________________________

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
        if not is_valid_binary_image(data):
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
        self.send(self.encode_long(value))

    def encode_long(self, value):
        """Encode a 32-bit long as short/long pulses."""
        result = []
        for i in range(10):
            result.append(chr(0x92 | (value & 0x01) | ((value & 2) << 2) | ((value & 4) << 4)))
            value >>= 3
        result.append(chr(0xf2 | (value & 0x01) | ((value & 2) << 2)))
        return "".join(result)

@Config.action('spi_upload',
               usage="",
               options=ActionOptions.upload_options,
               short_desc="Upload binary image.",
               uses_basepath=False)
def upload(cfg, run_fh=None):
    filenames = cfg.args
    assert len(filenames)
    # Select and read the file to be uploaded
    filename = filenames[0]
    fdata = None
    fh = open(filename, "rb")
    try:
        fdata = fh.read()
    finally:
        fh.close()
    # Instanciate uploader and connect to the target device
    uploader = StandardSPIUploader(port=cfg.options.serial_port)
    try:
        uploader.connect()
        uploader.upload(data=fdata)
    except (SystemExit, KeyboardInterrupt):
        print "Process has been interrupted"
        pass
    except Exception, e:
        print e
        exit(0)
    finally:
        uploader.disconnect()
    exit(0)

#_______________________________________________________________________________
#
# TODO: what do we need to do with binary images that have different
# clock speeds and modes?
#

class MulticogSPIUploader(SPIUploader):
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
                self.__total_upload_size += os.path.getsize(path)
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
        # hack the header. Thus assert(is_valid_binary_image(data)) is not
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

@Config.action('multicog_spi_upload',
               usage='%prog [options] multicog_spi_upload <filename>',
               options=ActionOptions.multicog_spi_upload_options,
               short_desc='Upload binary images, each for specific cog.',
               long_desc="""
The 'multicog_spi_upload' command uploads binary images to specific cogs.""",
               uses_basepath=False)
def multicog_spi_upload(cfg, run_fn=None):
    # Start process filenames and cogs.
    # Loading of equal binaries to different cogs is allowed.
    filenames = cfg.args
    free_cogs = range(1, PropellerP8X32.NR_COGS + 1)
    cogid_to_filename_mapping = dict()
    # Start process mappings from command line options
    for cogid in range(1, PropellerP8X32.NR_COGS + 1):
        filename = getattr(cfg.options, "cog%d" % cogid, None)
        if filename:
            cogid_to_filename_mapping[cogid] = filename
            free_cogs.remove(cogid)
    # Process filenames without specified cog id's
    if len(filenames) > len(free_cogs):
        print "Too many filenames."
        exit(0)
    for i in range(len(filenames)):
        if not os.path.exists(filenames[i]):
            raise Exception("File %s doesn't exist." % filenames[i])
        cogid_to_filename_mapping[free_cogs[i]] = filenames[i]
    # Instanciate uploader and connect to the target device
    try:
        uploader = MulticogSPIUploader(port=cfg.options.serial_port)
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

#_______________________________________________________________________________

def main(argv):
    cfg = Config(argv)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
