#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

#_____________________________________________________________________

import types
from ctypes import *

from bb.tools.propler.chips import *

#_____________________________________________________________________

__all__ = ["Image", "SpinHeader", "ElfHeader", "ElfContext",
           "ElfSectionHeader"]

class Image(object):
    """This class represents binary image."""

    # Target checksum for a binary file.
    SPIN_TARGET_CHECKSUM = 0x14

    @classmethod
    def dump_binary_header(cls, data):
        """Dump binary header."""
        print "Size : %d (bytes)" % len(data)
        hdr = None
        if fname:
            ctx = ElfContext(fname)
            if ctx.hdr.is_valid():
                hdr = ElfHeader()
                memmove(addressof(hdr), data, sizeof(ElfHeader))
                image = cls.extract_from_file(fname)
                hdr = SpinHeader()
                memmove(addressof(hdr), image, sizeof(SpinHeader))
            else:
                hdr = SpinHeader()
                memmove(addressof(hdr), data, sizeof(SpinHeader))
                print str(hdr)

    @classmethod
    def dump_file_header(cls, fname):
        """Dump image file header.
        See also :func:`dump_binary_header`."""
        # http://forums.parallax.com/showthread.php?117526-eeprom-file-format
        print "Binary file : %s" % fname
        fh = open(fname)
        data = ''.join(fh.readlines())
        print "File : %s" % fname
        fh = open(fname)
        cls.dump_binary_header(data)
        data = ''.join(fh.readlines())
        fh.close()

    @classmethod
    def extract_from_file(cls, filename):
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
        start = 0 # TODO: fix this
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
            # print program
            if not program:
                print "Can not load program table entry %d" % i
            buf = ctx.load_program_segment(program)
            if not buf:
                print "Cannot load program section %d" % i
            # for j in range(program.filesz):
            #    image_buf[program.paddr - start + j] = buf[j]
        img = ''.join(image_buf)
        # Fixup the header to point past the spin bytecodes and generated
        # PASM code
        x = c_char_p(img)
        hdr_p = cast(x, POINTER(SpinHeader))
        # hdr_p.contents.clk_speed = 80000000
        # hdr_p.contents.clk_mode = 0x6F
        hdr_p.contents.vbase = image_size
        hdr_p.contents.dbase = image_size + 2 * 4 # stack markers
        hdr_p.contents.dcurr = hdr_p.contents.dbase + 4
        # update checksum
        img = cls.update_binary_checksum(img)
        return img

    @classmethod
    def update_binary_checksum(cls, image):
        """Update checksum in binary."""
        checksum = 0
        x = c_char_p(image)
        hdr_p = cast(x, POINTER(SpinHeader))
        # first zero out the checksum
        hdr_p.contents.checksum = 0
        # compute the checksum
        for char in list(image):
            checksum += ord(char)
        # store the checksum in the header
        hdr_p.contents.checksum = cls.SPIN_TARGET_CHECKSUM - checksum
        return image

    @classmethod
    def is_valid_file(cls, filename):
        """Takes file name and returns ``True`` if it is valid binary
        file. See also :func:`is_valid_binary`."""
        fh = open(filename)
        data = ''.join(fh.readlines())
        is_valid = cls.is_valid_binary(data)
        fh.close()
        return is_valid

    @classmethod
    def is_valid_binary(cls, data):
        """Return ``True`` if binary image is valid. The checksum
        includes the "extra" bytes.  The extra bytes at the end are
        ``FF``, ``FF``, ``F9``, ``FF``, ``FF``, ``FF``, ``F9``,
        ``FF``. These are not included in the binary file, or in the
        EEPROM. These bytes are added to the beginning of the stack at
        run time. The extra bytes cause a Spin cog to jump to the ROM
        address ``FFF9`` when it terminates. The code at ``FFF9``
        contains a few Spin bytecode instructions to get the cog ID
        and issue a cogstop."""
        bytes = bytearray(data)
        calc_checksum = reduce(lambda a, b: a + b, bytes)
        calc_checksum += 2 * (0xFF + 0xFF + 0xF9 + 0xFF)
        if not (calc_checksum & 0xFF):
            return True
        return False

    @classmethod
    def get_file_size(cls, filename):
        """Return image size contained in file `filename`. Supports
        SPIN and ELF images."""
        ctx = ElfContext(filename)
        (start, image_size) = ctx.get_program_size()
        return image_size

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

# Just to be sure
assert sizeof(SpinHeader) == 16, \
    "Size of spin header must be 16 bytes!"

class ElfContext(object):
    """This class represents ELF context."""

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
        ## The following implemetation reflects implementation from
        ## propeller-load tool.
        for i in range(self.hdr.phnum):
            program = self.load_program_table_entry(i)
            if program.paddr < start:
                start = program.paddr
            if (program.paddr + program.filesz) > end:
                end = program.paddr + program.filesz

        #for i in range(self.hdr.shnum):
        #    section = self.load_section_table_entry(i)
        #    if section.addr < start:
        #        start = section.addr
        #    if (section.addr + section.size) > end:
        #        end = section.addr + section.size
        
        return (start, end - start)

    def load_section_table_entry(self, i):
        offset = self.hdr.shoff + (i * self.hdr.shentsize)
        hdr = ElfSectionHeader()
        memmove(addressof(hdr), self.data[offset:offset + sizeof(ElfSectionHeader)], sizeof(ElfSectionHeader))
        return hdr

    def load_section_segment(self, section):
        return self.data[section.offset:section.offset + section.size]

    def load_program_table_entry(self, i):
        o = self.hdr.phoff + (i * self.hdr.phentsize)
        hdr = ElfProgramHeader()
        memmove(addressof(hdr), self.data[o:o + sizeof(ElfProgramHeader)], sizeof(ElfProgramHeader))
        return hdr

    def load_program_segment(self, program):
        return self.data[program.offset:program.offset + program.filesz]

class ElfSectionHeader(Structure):
    SHT_NULL =0
    SHT_PROGBITS =1
    SHT_SYMTAB =2
    SHT_STRTAB =3
    SHT_RELA =4
    SHT_HASH =5
    SHT_DYNAMIC =6
    SHT_NOTE =7
    SHT_NOBITS =8
    SHT_REL =9
    SHT_SHLIB =10
    SHT_DYNSYM =11
    SHT_LOPROC =0x70000000
    SHT_HIPROC =0x7fffffff
    SHT_LOUSER =0x80000000
    SHT_HIUSER =0xffffffff

    _fields_ = [("name"      , c_long),
                ("type"      , c_long),
                ("flags"     , c_long),
                ("addr"      , c_long),
                ("offset"    , c_long),
                ("size"      , c_long),
                ("link"      , c_long),
                ("info"      , c_long),
                ("addralign" , c_long),
                ("entsize"   , c_long)]

class ElfProgramHeader(Structure):
    """An executable or shared object file's program header table is
    an array of structures, each describing a segment or other
    information the system needs to prepare the program for
    execution. Program headers are meaningful only for executable and
    shared object files. A file specifies its own program header size
    with the ELF header's e_phentsize and e_phnum members."""
    FLAGS = [[0x1, "R"], [0x2, "W"], [0x4, "E"]]

    _fields_ = [("type"   , c_long),
                ("offset" , c_long),
                ("vaddr"  , c_long),
                ("paddr"  , c_long),
                ("filesz" , c_long),
                ("memsz"  , c_long),
                ("flags"  , c_long),
                ("align"  , c_long)]

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

    _fields_ = [("ident"    , (c_char * 16)), # Magic number and other info
                ("type"     , c_ushort), # Object file type
                ("machine"  , c_ushort),
                ("version"  , c_uint),
                ("entry"    , c_uint),
                ("phoff"    , c_uint),
                ("shoff"    , c_uint),
                ("flags"    , c_uint),
                ("ehsize"   , c_ushort),
                ("phentsize", c_ushort),
                ("phnum"    , c_ushort),
                ("shentsize", c_ushort),
                ("shnum"    , c_ushort),
                ("shstrndx" , c_ushort),
                ]

    def is_valid(self):
        if not len(self.ident):
            return False
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
            " start of section headers  : %d (bytes into file)\n" \
            " size of program headers   : %d (bytes)\n" \
            " number of program headers : %d\n" \
            " size of section headers   : %d (bytes)\n" \
            " number of section headers : %d\n" \
            " section header string table index : %d" \
            % ("".join([" %02x" % ord(c) for c in self.ident]),
               self.type,
               self.machine, self.MACHINE_MAP[self.machine],
               self.version,
               self.entry,
               self.phoff,
               self.shoff,
               self.phentsize,
               self.phnum,
               self.shentsize,
               self.shnum, self.shstrndx)
