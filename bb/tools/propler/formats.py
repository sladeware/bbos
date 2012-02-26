#!/usr/bin/env python

import types
from ctypes import *

import bb.tools.propler.propeller_chip

class SpinHeader(Structure):
    """
    =========  ============
    Name       Description
    =========  ============
    clk_speed  Clock speed.
    clk_mode   --
    checksum   --
    pbase      Start address of an object.
    vbase      Start address of the VAR section of an object.
    dbase      Start address of a method's stack variables.
    pcurr      Current program counter. Starting address of the first
               instraction to be executed.
    dcurr      Address of the next variable to be stored on the stack.
    =========  ============"""
    _fields_ = [("clk_speed", c_int),
                ("clk_mode", c_byte),
                ("checksum", c_byte),
                ("pbase", c_short),
                ("vbase", c_short),
                ("dbase", c_short),
                ("pcurr", c_short),
                ("dcurr", c_short)
                ]

    def __str__(self):
        return "Spin header:\n" \
            " clock speed : %d\n" \
            " clock mode  : 0x%02x (s)\n" \
            " checksum    : %d\n" \
            " pbase       : 0x%04x\n" \
            " vbase       : 0x%04x\n" \
            " dbase       : 0x%04x\n" \
            " pcurr       : 0x%04x\n" \
            " dcurr       : 0x%04x"\
            % (self.clk_speed,
               self.clk_mode, #propeller_chip.ClockModes.to_string[self.clk_mode],
               self.checksum,
               self.pbase, self.vbase, self.dbase, self.pcurr, self.dcurr)

class ElfContext(object):
    def __init__(self, filename):
        self.fname = filename
        self.fh = open(filename)
        self.data = ''.join(self.fh.readlines())
        # Read header
        self.hdr = ElfHeader()
        memmove(addressof(self.hdr), self.data, sizeof(ElfHeader))

    def get_program_size(self):
        start = 0xFFFFFFFF
        end = 0
        for i in range(self.hdr.phnum):
            program = self.load_program_table_entry(i)
            if program.paddr < start:
                start = program.paddr
            if (program.paddr + program.filesz) > end:
                end = program.paddr + program.filesz
        return (start, end - start)

    def load_program_segment(self, program):
        return self.data[program.offset:program.offset + program.filesz]

    def load_program_table_entry(self, i):
        o = self.hdr.phoff + (i * self.hdr.phentsize)
        hdr = ElfProgramHeader()
        memmove(addressof(hdr), self.data[o:o + sizeof(ElfProgramHeader)], sizeof(ElfProgramHeader))
        return hdr

class ElfProgramHeader(Structure):
    """Program header."""
    FLAGS = [[0x1, "R"], [0x2, "W"], [0x4, "E"]]

    _fields_ = [("type", c_long),
                ("offset", c_long),
                ("vaddr", c_long),
                ("paddr", c_long),
                ("filesz", c_long),
                ("memsz", c_long),
                ("flags", c_long),
                ("align", c_long)]

    def __str__(self):
        flags_string = ""
        for flag in self.FLAGS:
            if self.flags & flag[0]: flags_string += flag[1]
            else: flags_string += " "
        return "Program header:\n" \
            " Type     : %d\n" \
            " Offset   : 0x%08x\n" \
            " VirtAddr : 0x%08x\n" \
            " PhysAddr : 0x%08x\n" \
            " FileSize : %d\n" \
            " MemSize  : %d\n" \
            " Flags    : %s (0x%02x)\n" \
            " Align    : 0x%08x\n" \
            % (self.type, self.offset, self.vaddr, self.paddr,
               self.filesz, self.memsz, flags_string, self.flags, self.align)

IDENT_SIGNIFICANT_BYTES = 9
ident = [
    0x7f, ord('E'), ord('L'), ord('F'),         # magic number
    0x01,                                       # class
    0x01,                                       # data
    0x01,                                       # version
    0x00,                                       # os / abi identification
    0x00,                                       # abi version
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00    # padding
]

class ElfHeader(Structure):
    """ELF header.

    ============== ===========
    Name           Description
    ============== ===========
    `e_ident`      The initial bytes mark the file as an object file and provide machine-independent data with which to decode and interpret the file's contents.
    `e_type`       This member identifies the object file type.
    `e_machine`    This member's value specifies the required architecture
                   for an individual file.
    `e_version`    This member identifies the object file version.
    `e_entry`      This member gives the virtual address to which the system
                   first transfers control, thus starting the process. If the
                   file has no associated entry point, this member holds zero.
    `e_phoff`      This member holds the program header table's file offset in
                   bytes. If the file has no program header table, this
                   member holds zero.
    `e_shoff`      This member holds the section header table's file offset in
                   bytes. If the file has no section header table,
                   this member holds zero.
    `e_flags`      This member holds processor-specific flags associated with
                   the file.
    `e_ehsize`     This member holds the ELF header's size in bytes.
    `e_phentsize`  This member holds the size in bytes of one entry in the
                   file's program header table; all entries are the same size.
    `e_phnum`      This member holds the number of entries in the program header
                   table. Thus the product of `e_phentsize` and
                   `e_phnum` gives
                   the table's size in bytes. If a file has no program header
                   table, `e_phnum` holds the value zero.
    `e_shentsize`  This member holds a section header's size in bytes. A section
                   header is one entry in the section header table; all entries
                   are the same size.
    `e_shnum`      This member holds the number of entries in the section
                   header table. Thus the product of `e_shentsize` and `e_shnum`
                   gives the section header table's size in bytes. If a file has
                   no section header table, `e_shnum` holds the value zero.
    `e_shstrndx`   This member holds the section header table index of the entry
                   associated with the section name string table.
    ============== ===========
    """
    MACHINE_MAP = {
        0x5072: "Parallax Propeller",
        }

    _fields_ = [("ident", (c_char * 16)), # Magic number and other info
                ("type", c_ushort), # Object file type
                ("machine", c_ushort),
                ("version", c_uint),
                ("entry", c_uint),
                ("phoff", c_uint),
                ("shoff", c_uint),
                ("flags", c_uint),
                ("ehsize", c_ushort),
                ("phentsize", c_ushort),
                ("phnum", c_ushort),
                ("shentsize", c_ushort),
                ("shnum", c_ushort),
                ("shstrndx", c_ushort),
                ]

    def is_valid(self):
        for i in range(len(self.ident)):
            if ord(self.ident[i]) != ident[i]:
                return False
        return True

    def __str__(self):
        return "ELF Header:\n" \
            " ident                     : %s\n" \
            " type                      : 0x%04x\n" \
            " machine                   : 0x%04x (%s)\n" \
            " version                   : 0x%08x\n" \
            " entry point address       : 0x%08x\n" \
            " start of program headers  : %d (bytes into file)\n" \
            " size of program headers   : %d (bytes)\n" \
            " number of program headers : %d\n" \
            " size of section headers   : %d (bytes)\n" \
            " number of section headers : %d" \
            % ("".join([" %02x" % ord(c) for c in self.ident]),
               self.type,
               self.machine, self.MACHINE_MAP[self.machine],
               self.version,
               self.entry,
               self.phoff,
               self.phentsize,
               self.phnum,
               self.shentsize,
               self.shnum)
