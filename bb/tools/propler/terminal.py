#!/usr/bin/env python

"""This is a console application that provides a small terminal application."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__all__ = ["Terminal"]

import os
import sys
import threading

try:
    import serial
except ImportError:
    print >>sys.stderr, "Please install pyserial."
    exit(0)

if sys.version_info >= (3, 0):
    def character(b):
        return b.decode('latin1')
else:
    def character(b):
        return b

# First choose a platform dependant way to read single characters from
# the console
global console

if os.name == 'nt':
    import msvcrt
    class Console(object):
        def __init__(self):
            pass

        def setup(self):
            pass # Do nothing for 'nt'

        def cleanup(self):
            pass # Do nothing for 'nt'

        def getkey(self):
            while True:
                z = msvcrt.getch()
                if z == '\0' or z == '\xe0':    # functions keys, ignore
                    msvcrt.getch()
                else:
                    if z == '\r':
                        return '\n'
                    return z
    console = Console()
elif os.name == 'posix':
    import termios, sys, os
    class Console(object):
        def __init__(self):
            self.fd = sys.stdin.fileno()

        def setup(self):
            self.old = termios.tcgetattr(self.fd)
            new = termios.tcgetattr(self.fd)
            new[3] = new[3] & ~termios.ICANON & ~termios.ECHO & ~termios.ISIG
            new[6][termios.VMIN] = 1
            new[6][termios.VTIME] = 0
            termios.tcsetattr(self.fd, termios.TCSANOW, new)

        def getkey(self):
            c = os.read(self.fd, 1)
            return c

        def cleanup(self):
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old)

    console = Console()

    def cleanup_console():
        console.cleanup()

    console.setup()
    sys.exitfunc = cleanup_console      # terminal modes have to be restored on exit...
else:
    raise NotImplementedError("Sorry no implementation for your " \
                                  "platform (%s) available." % sys.platform)

EXIT_CHARACTER = chr(3)

class Terminal(object):
    """Propler terminal for serial communications."""

    def __init__(self, port):
        self.sio = serial.Serial(port=port, baudrate=115200, timeout=2)
        self.sio.open()
        self.is_alive = True
        self.receiver_thread = None
        self.transmitter_thread = None

    def start(self):
        # Start reader
        self.receiver_thread = threading.Thread(target=self.reader)
        self.receiver_thread.daemon = True
        self.receiver_thread.start()
        # Start writer
        self.transmitter_thread = threading.Thread(target=self.writer)
        self.transmitter_thread.daemon = True
        self.transmitter_thread.start()
        # While alive
        try:
            self.receiver_thread.join()
            self.transmitter_thread.join()
        except KeyboardInterrupt:
            print "Interrupted"

    def stop(self):
        self.is_alive = False

    def writer(self):
        try:
            while self.is_alive:
                try:
                    b = console.getkey()
                except KeyboardInterrupt:
                    b = serial.to_bytes([3])
                    raise
                c = character(b)
                self.sio.write(b)

                if c == EXIT_CHARACTER:
                    self.stop()
                    break
        except serial.SerialException, e:
            self.stop()
            raise
        except KeyboardInterrupt:
            self.stop()
            raise

    def reader(self):
        try:
            while self.is_alive:
                c = self.sio.read()
                sys.stdout.flush()
                sys.stdout.write(c)
        except serial.SerialException, e:
            self.stop()
            raise
        except KeyboardInterrupt:
            self.stop()
            raise
        print "EXIT"



