#!/usr/bin/env python

import os
import time
import sys
import types
import optparse
import operator

try:
    import serial
except ImportError:
    print >>sys.stderr, "Please install pyserial."
    exit(0)

PAGE_SIZE = 1 << 9
SIO_BAUD = 115200 # Baud rate to use for all interprop comms
BYTE_DELAY = 1 / 6000
# End of page marker
MARKER = 0xFFFFFE

EEPROM_SIZE = 32768
RAM_SIZE = 262144

# Platform defaults
default_serial_ports = {
    "posix": "/dev/ttyUSB0",
    "nt": "COM1",
}

class Long:
    @classmethod
    def ror(cls, x, n):
        return ((x >> n) & 0xFFFFFFFF) | ((x << (32 - n) & 0xFFFFFFFF))

    @classmethod
    def reverse_bytes(cls, x):
        return ((x & 0xFF) << 24) | ((x << 8) & 0xFF0000) | ((x >> 8) & 0xFF00) \
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
    def split_bytes(cls, x):
        return ((x >> 24) & 0xFF, (x >> 16) & 0xFF, (x >> 8) & 0xFF, x & 0xFF)

def long_by_bytes(*args):
    bytes = None
    if len(args) == 1:
        bytes = args
    elif len(args) == 4:
        bytes = (args)
    else:
        raise Exception()
    return bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24)

class Uploader(object):

    def __init__(self, cpu_no=1, port=None):
        self.__cpu_no = None
        self.set_cpu_no(cpu_no)
        self.__serial = serial.Serial(baudrate=SIO_BAUD, timeout=None)
        self.__serial.port = port

    def get_cpu_no(self):
        return self.__cpu_no

    def set_cpu_no(self, no):
        self.__cpu_no = no

    def connect(self):
        self.__serial.open()
        self.reset()
        time.sleep(3)

    def reset(self):
        self.__serial.flushOutput()
        self.__serial.setDTR(1)
        time.sleep(0.025)
        self.__serial.setDTR(0)
        time.sleep(0.090)
        self.__serial.flushInput()

    def __send_sync_signal(self):
        """Send two-bytes sync signal: 0xFF <CPU_NO>. These sequences can never
        be generated accidentally because during normal sending 0xFF is stuffed
        to 0xFF 0x00, so we can wait for this without the risk of accidentally
        being triggered by a program being sent to another CPU."""
        print "Sending sync signal"
        self.send_byte(chr(0xFF))
        self.send_byte(chr(self.get_cpu_no()))

    def send_byte(self, byte, timeout=None):
        if not type(byte) is types.StringType:
            byte = chr(byte)
        self.__serial.write(byte)
        if timeout:
            time.sleep(timeout)

    def stuff_and_send_byte(self, byte, timeout=None):
        if not type(byte) is types.StringType:
            byte = chr(byte)
        self.send_byte(byte, timeout)
        if byte == chr(0xFF):
            self.send_byte(0, timeout)

    def stuff_and_send_long(self, x):
        bytes = x
        if type(x) is types.IntType or type(x) is types.LongType:
            bytes = Long.split_bytes(x)
        for byte in bytes:
            self.stuff_and_send_byte(byte)

    def upload(self, bin_filename):
        bin_fh = open(bin_filename)
        data = ''.join(bin_fh.readlines())
        if len(data) % 4 != 0:
            raise Exception("Invalid code size: must be a multiple of 4")
        print "Uploading %s (%d bytes)" % (bin_filename, len(data))
        # Send sync signal to start binary transmitting
        self.__send_sync_signal()
        # Note, that only a max of PAGE_SIZE will actually get loaded, thus
        # we split data on chunks and send them in pages
        chunks = [PAGE_SIZE] * (len(data) / PAGE_SIZE)
        if len(data) % PAGE_SIZE:
            chunks.append(len(data) % PAGE_SIZE)
        i = 1
        addr = 0
        for size in chunks:
            page = data[addr:addr + size]
            self.__send_page(i, addr, page, size)
            i += 1
            addr += size
        self.__send_page(i, MARKER, "", 0)
        bin_fh.close()

    def __send_page(self, seq_no, addr, buf, size):
        """Send bytes that have to be stored to Hub RAM."""
        # Sending 4-bytes header: [CPU_NO |    ADDR   ]
        header = (addr & 0xFFFFFF) | (self.get_cpu_no() << 24)
        self.stuff_and_send_long(Long.reverse_bytes(header))
        # Sending page 4 bytes size
        self.stuff_and_send_long(Long.reverse_bytes(size))
        # IF
        if addr == MARKER:
            self.send_byte(chr(self.get_cpu_no()))
            sys.stdout.write("Sending packet #%d [CPU=%d, ADDR=0x%x, SIZE=%d]\n" \
                                 % (seq_no, self.get_cpu_no(), addr, size))
            return
        # LRC-checksum value (xor of each byte)
        lrc_checksum = 0x00
        # Start transmitting page bytes
        print "Sending packet #%d [CPU=%d, ADDR=0x%x, SIZE=%d]" \
            % (seq_no, self.get_cpu_no(), addr, size)
        i = 0
        while i < size:
            self.stuff_and_send_byte(buf[i])
            # Calculate the XOR value for each byte
            lrc_checksum = operator.xor(lrc_checksum, ord(buf[i]))
            i += 1
        # Waiting for sync
        print "Waiting for sync..."
        sync = self.__serial.read(2) # timeout=None <== wait
        assert len(sync) == 2 # two bytes
        assert ord(sync[1]) == self.get_cpu_no()
        sys.stdout.write("Waiting for LRC checksum value... ")
        result_lrc_checksum = ord(self.__serial.read(1))
        print result_lrc_checksum
        # Compare our LRC value and result LRC value from device
        print "LRC-checksum: %d=%d" % (lrc_checksum, result_lrc_checksum)

    def disconnect(self):
        self.__serial.close()

def main(argv):
    parser = optparse.OptionParser(
        prog=os.path.basename(argv[0]),
        usage="%prog [options] FILENAME",
        description=None,
        formatter=optparse.IndentedHelpFormatter(),
        add_help_option=False,
    )
    parser.add_option("-h", "--help", action="help",
                      help="Show this help message and exit.")
    parser.add_option("-s", "--serial_port", dest="serial_port", nargs=1,
                      type="string", metavar="DEVICE",
                      default=default_serial_ports.get(os.name, "none"),
                      help="Select the serial port device. The default is %default.")
    parser.add_option("-c", "--cpu_no", dest="cpu_no", nargs=1, type="long",
                      metavar="ID", default=1,
                      help="Select the cpu no. The default is %default.")
    parser.add_option("-o", "--ram-offset", dest="ram_offset", nargs=1,
                      type="long", metavar="OFFSET", default=0,
                      help="RAM offset from which data will be stored.")
    (options, args) = parser.parse_args(argv[1:])
    if len(args) != 1:
        sys.stderr.write("Invalid number of arguments\n")
        parser.print_help(sys.stderr)
        return 2
    filename = args[0]

    uploader = Uploader(cpu_no=options.cpu_no, port=options.serial_port)
    uploader.connect()
    uploader.upload(filename)
    uploader.disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
