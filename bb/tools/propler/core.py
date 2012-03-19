#!/usr/bin/env python

"""The basic idea of code uploader for Parallax Propeller chip was
taken from
`uploader <http://forums.parallax.com/showthread.php?90707-Propeller-development-for-non-Windows-users>`_
proposed by Remy Blank."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

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

from bb.utils.spawn import spawn
from bb.tools.propler.formats import SpinHeader, ElfHeader, ElfContext, ElfSectionHeader
from bb.tools.propler.propeller_chip import PropellerP8X32
from bb.tools.propler.bitwise_op import *
from bb.tools.propler.config import CustomBoardConfig, QuickStartBoardConfig, DemoBoardConfig

def dump_header(fname, data=None):
    """Dump header."""
    # http://forums.parallax.com/showthread.php?117526-eeprom-file-format
<<<<<<< .mine
    if fname:
        print "Binary file : %s" % fname
        fh = open(fname)
        data = ''.join(fh.readlines())
=======
    print "File : %s" % fname
    fh = open(fname)
    data = ''.join(fh.readlines())
>>>>>>> .r631
    print "Size : %d (bytes)" % len(data)
    hdr = None
    if fname:
        ctx = ElfContext(fname)
        if ctx.hdr.is_valid():
            hdr = ElfHeader()
            memmove(addressof(hdr), data, sizeof(ElfHeader))
            image = extract_image_from_file(fname)
            hdr = SpinHeader()
            memmove(addressof(hdr), image, sizeof(SpinHeader))
    else:
        hdr = SpinHeader()
        memmove(addressof(hdr), data, sizeof(SpinHeader))
    print str(hdr)
    #fh.close()

def extract_image_from_file(filename):
    """Extract image from file `filename`. Developed for extracting
    image from ELF binary."""
    ctx = ElfContext(filename)
    # Verify ELF context
    if not ctx.hdr.is_valid():
        fh = open(filename, "rb")
        img = fh.read()
        fh.close()
        return img

    (start, image_size) = ctx.get_program_size()
<<<<<<< .mine
    start = 0 # TODO: fix this

=======
    
>>>>>>> .r631
    image_buf = [chr(0)] * image_size

    # Experemental!
    pos = 0
    for i in range(ctx.hdr.shnum):
        section = ctx.load_section_table_entry(i)
        if not section:
            print "Can not load section table entry %d" % i
        if section.type != ElfSectionHeader.SHT_PROGBITS:
            continue
        buf = ctx.load_section_segment(section)
        for j in range(section.size):
            image_buf[pos - start + j] = buf[j]
        pos += section.size

    # load each program section
    for i in range(ctx.hdr.phnum):
        program = ctx.load_program_table_entry(i)
        #print program
        if not program:
            print "Can not load program table entry %d" % i
        buf = ctx.load_program_segment(program)
        if not buf:
            print "Cannot load program section %d" % i
        #for j in range(program.filesz):
        #    image_buf[program.paddr - start + j] = buf[j]

    img = ''.join(image_buf)
    # Fixup the header to point past the spin bytecodes and generated
    # PASM code
    x = c_char_p(img)
    hdr_p = cast(x, POINTER(SpinHeader))
    #hdr_p.contents.clk_speed = 80000000
    #hdr_p.contents.clk_mode = 0x6F
    hdr_p.contents.vbase = image_size
    hdr_p.contents.dbase = image_size + 2 * 4 # stack markers
    hdr_p.contents.dcurr = hdr_p.contents.dbase + 4
    # update checksum
    img = update_image_checksum(img)
    return img

# Target checksum for a binary file
SPIN_TARGET_CHECKSUM = 0x14

def update_image_checksum(image):
    checksum = 0
    x = c_char_p(image)
    hdr_p = cast(x, POINTER(SpinHeader))
    # first zero out the checksum
    hdr_p.contents.checksum = 0
    # compute the checksum
    for char in list(image):
        checksum += ord(char)
    # store the checksum in the header
    hdr_p.contents.checksum = SPIN_TARGET_CHECKSUM - checksum
    return image


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
    ``F9``, ``FF``, ``FF``, ``FF``, ``F9``, ``FF``. These are not
    included in the binary file, or in the EEPROM. These bytes are
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
    """Return image size contained in file `filename`. Supports SPIN
    and ELF images."""
    ctx = ElfContext(filename)
    (start, image_size) = ctx.get_program_size()
    return image_size
