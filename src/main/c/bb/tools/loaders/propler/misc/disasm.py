#!/usr/bin/env python

import struct
import sys

#  Operation Code Types
#
#  0: No Arguement
#  1: Has a 'effect' code
#  2: Has a signed offset
#  3: Has a Packed literal
#  4: Has an unsigned offset
#  5: Has an unsigned offset and 'effect' code
#  6: Byte literal
#  7: Word literal
#  8: Near-Long literal
#  9: Long literal
#  10: Object.Call pair
#  11: Memory Operation Code
#

simpleOps = {
    0x00: ("FRAME_CALL_RETURN", 0),
    0x01: ("FRAME_CALL_NORETURN", 0),
    0x02: ("FRAME_CALL_ABORT", 0),
    0x03: ("FRAME_CALL_TRASHABORT", 0),
    0x04: ("BRANCH", 2),
    0x05: ("CALL", 6),
    0x06: ("OBJCALL", 10),
    # 0x07
    0x08: ("LOOP_START",2),
    0x09: ("LOOP_CONTINUE", 2),
    0x0A: ("JUMP_IF_FALSE", 2),
    0x0B: ("JUMP_IF_TRUE", 2),
    0x0C: ("JUMP_FROM_STACK",0),
    0x0D: ("COMPARE_CASE",2),
    0x0E: ("COMPARE_CASE_RANGE",2),
    0x0F: ("LOOK_ABORT", 0),
    0x10: ("LOOKUP_COMPARE", 0),
    0x11: ("LOODOWN_COMPARE", 0),
    0x12: ("LOOKUPRANGE_COMPARE", 0),
    0x13: ("LOOKDOWNRANGE_COMPARE", 0),
    0x14: ("QUIT",0),
    0x15: ("MARK_INTERPRETED", 0),
    0x16: ("STRSIZE", 0),
    0x17: ("STRCOMP", 0),
    0x18: ("BYTEFILL", 0),
    0x19: ("WORDFILL", 0),
    0x1A: ("LONGFILL", 0),
    0x1b: ("WAITPEQ", 0),
    0x1C: ("BYTEMOVE", 0),
    0x1D: ("WORDMOVE", 0),
    0x1E: ("LONGMOVE", 0),
    0x1f: ("WAITPNE", 0),
    0x20: ("CLKSET", 0),
    0x21: ("COGSTOP", 0),
    0x22: ("LOCKRET", 0),
    0x23: ("WAITCNT", 0),
    0x24: ("READ_INDEXED_SPR", 0),
    0x25: ("WRITE_INDEXED_SPR", 0),
    0x26: ("EFFECT_INDEXED_SPR",1),
    0x27: ("WAITVID", 0),
    0x28: ("COGINIT_RETURNS", 0),
    0x29: ("LOCKNEW_RETURNS", 0),
    0x2A: ("LOCKSET_RETURNS", 0),
    0x2B: ("LOCKCLR_RETURNS", 0),
    0x2C: ("COGINIT", 0),
    0x2D: ("LOCKNEW", 0),
    0x2e: ("LOCKSET", 0),
    0x2f: ("LOCKCLR", 0),
    0x30: ("ABORT", 0),
    0x31: ("ABORT_WITH_RETURN", 0),
    0x32: ("RETURN", 0),
    0x33: ("POP_RETURN", 0),
    0x34: ("PUSH_NEG1", 0),
    0x35: ("PUSH_0", 0),
    0x36: ("PUSH_1", 0),
    0x37: ("PUSH_PACKED_LIT", 3),
    0x38: ("PUSH_BYTE_LIT", 6),
    0x39: ("PUSH_WORD_LIT", 7),
    0x3A: ("PUSH_MID_LIT", 8),
    0x3B: ("PUSH_LONG_LIT", 9),
    # 0x3C
    0x3D: ("INDEXED_MEM_OP", 11),
    0x3E: ("INDEXED_RANGE_MEM_OP", 11),
    0x3F: ("MEMORY_OP", 11),
    # ...
    # 0x40 - 0x7F are variable blocks
    # ...
    0x80: ("PUSH_MAINMEM_BYTE", 0),
    0x81: ("POP_MAINMEM_BYTE", 0),
    0x82: ("EFFECT_MAINMEM_BYTE",1),
    0x83: ("REFERENCE_MAINMEM_BYTE", 0),
    0x84: ("PUSH_OBJECTMEM_BYTE" ,4),
    0x85: ("POP_OBJECTMEM_BYTE" ,4),
    0x86: ("EFFECT_OBJECTMEM_BYTE" ,5),
    0x87: ("REFERENCE_OBJECTMEM_BYTE" ,4),
    0x88: ("PUSH_VARIABLEMEM_BYTE" ,4),
    0x89: ("POP_VARIABLEMEM_BYTE" ,4),
    0x8A: ("EFFECT_VARIABLEMEM_BYTE" ,5),
    0x8B: ("REFERENCE_VARIABLEMEM_BYTE" ,4),
    0x8C: ("PUSH_INDEXED_LOCALMEM_BYTE" ,4),
    0x8D: ("POP_INDEXED_LOCALMEM_BYTE" ,4),
    0x8E: ("EFFECT_INDEXED_LOCALMEM_BYTE" ,5),
    0x8F: ("REFERENCE_INDEXED_LOCALMEM_BYTE" ,4),
    0x90: ("PUSH_INDEXED_MAINMEM_BYTE", 0),
    0x91: ("POP_INDEXED_MAINMEM_BYTE", 0),
    0x92: ("EFFECT_INDEXED_MAINMEM_BYTE",1),
    0x93: ("REFERENCE_INDEXED_MAINMEM_BYTE", 0),
    0x94: ("PUSH_INDEXED_OBJECTMEM_BYTE" ,4),
    0x95: ("POP_INDEXED_OBJECTMEM_BYTE" ,4),
    0x96: ("EFFECT_INDEXED_OBJECTMEM_BYTE" ,5),
    0x97: ("REFERENCE_INDEXED_OBJECTMEM_BYTE" ,4),
    0x98: ("PUSH_INDEXED_VARIABLEMEM_BYTE" ,4),
    0x99: ("POP_INDEXED_VARIABLEMEM_BYTE" ,4),
    0x9A: ("EFFECT_INDEXED_VARIABLEMEM_BYTE" ,5),
    0x9B: ("REFERENCE_INDEXED_VARIABLEMEM_BYTE" ,4),
    0x9C: ("PUSH_INDEXED_LOCALMEM_BYTE" ,4),
    0x9D: ("POP_INDEXED_LOCALMEM_BYTE" ,4),
    0x9E: ("EFFECT_INDEXED_LOCALMEM_BYTE" ,5),
    0x9F: ("REFERENCE_INDEXED_LOCALMEM_BYTE" ,4),
    0xA0: ("PUSH_MAINMEM_WORD", 0),           
    0xA1: ("POP_MAINMEM_WORD", 0),           
    0xA2: ("EFFECT_MAINMEM_WORD",1),
    0xA3: ("REFERENCE_MAINMEM_WORD", 0),
    0xA4: ("PUSH_OBJECTMEM_WORD" ,4),
    0xA5: ("POP_OBJECTMEM_WORD" ,4),
    0xA6: ("EFFECT_OBJECTMEM_WORD" ,5),
    0xA7: ("REFERENCE_OBJECTMEM_WORD" ,4),
    0xA8: ("PUSH_VARIABLEMEM_WORD" ,4),
    0xA9: ("POP_VARIABLEMEM_WORD" ,4),
    0xAA: ("EFFECT_VARIABLEMEM_WORD" ,5),
    0xAB: ("REFERENCE_VARIABLEMEM_WORD" ,4),
    0xAC: ("PUSH_LOCALMEM_WORD" ,4),
    0xAD: ("POP_LOCALMEM_WORD" ,4),
    0xAE: ("EFFECT_LOCALMEM_WORD" ,5),
    0xAF: ("REFERENCE_LOCALMEM_WORD" ,4),
    0xB0: ("PUSH_INDEXED_MAINMEM_WORD", 0),           
    0xB1: ("POP_INDEXED_MAINMEM_WORD", 0),           
    0xB2: ("EFFECT_INDEXED_MAINMEM_WORD",1),
    0xB3: ("REFERENCE_INDEXED_MAINMEM_WORD", 0),           
    0xB4: ("PUSH_INDEXED_OBJECTMEM_WORD" ,4),
    0xB5: ("POP_INDEXED_OBJECTMEM_WORD" ,4),
    0xB6: ("EFFECT_INDEXED_OBJECTMEM_WORD" ,5),
    0xB7: ("REFERENCE_INDEXED_OBJECTMEM_WORD" ,4),
    0xB8: ("PUSH_INDEXED_VARIABLEMEM_WORD" ,4),
    0xB9: ("POP_INDEXED_VARIABLEMEM_WORD" ,4),
    0xBA: ("EFFECT_INDEXED_VARIABLEMEM_WORD" ,5),
    0xBB: ("REFERENCE_INDEXED_VARIABLEMEM_WORD" ,4),
    0xBC: ("PUSH_INDEXED_LOCALMEM_WORD" ,4),
    0xBD: ("POP_INDEXED_LOCALMEM_WORD" ,4),
    0xBE: ("EFFECT_INDEXED_LOCALMEM_WORD" ,5),
    0xBF: ("REFERENCE_INDEXED_LOCALMEM_WORD" ,4),
    0xC0: ("PUSH_MAINMEM_LONG", 0),
    0xC1: ("POP_MAINMEM_LONG", 0),
    0xC2: ("EFFECT_MAINMEM_LONG",1),
    0xC3: ("REFERENCE_MAINMEM_LONG", 0),
    0xC4: ("PUSH_OBJECTMEM_LONG" ,4),
    0xC5: ("POP_OBJECTMEM_LONG" ,4),
    0xC6: ("EFFECT_OBJECTMEM_LONG" ,5),
    0xC7: ("REFERENCE_OBJECTMEM_LONG" ,4),
    0xC8: ("PUSH_VARIABLEMEM_LONG" ,4),
    0xC9: ("POP_VARIABLEMEM_LONG" ,4),
    0xCA: ("EFFECT_VARIABLEMEM_LONG" ,5),
    0xCB: ("REFERENCE_VARIABLEMEM_LONG" ,4),
    0xCC: ("PUSH_LOCALMEM_LONG" ,4),
    0xCD: ("POP_LOCALMEM_LONG" ,4),
    0xCE: ("EFFECT_LOCALMEM_LONG" ,5),
    0xCF: ("REFERENCE_LOCALMEM_LONG" ,4),
    0xD0: ("PUSH_INDEXED_MAINMEM_LONG", 0),
    0xD1: ("POP_INDEXED_MAINMEM_LONG", 0),
    0xD2: ("EFFECT_INDEXED_MAINMEM_LONG",1),
    0xD3: ("REFERENCE_INDEXED_MAINMEM_LONG", 0),
    0xD4: ("PUSH_INDEXED_OBJECTMEM_LONG" ,4),
    0xD5: ("POP_INDEXED_OBJECTMEM_LONG" ,4),
    0xD6: ("EFFECT_INDEXED_OBJECTMEM_LONG" ,5),
    0xD7: ("REFERENCE_INDEXED_OBJECTMEM_LONG" ,4),
    0xD8: ("PUSH_INDEXED_VARIABLEMEM_LONG" ,4),
    0xD9: ("POP_INDEXED_VARIABLEMEM_LONG" ,4),
    0xDA: ("EFFECT_INDEXED_VARIABLEMEM_LONG" ,5),
    0xDB: ("REFERENCE_INDEXED_VARIABLEMEM_LONG" ,4),
    0xDC: ("PUSH_INDEXED_LOCALMEM_LONG" ,4),
    0xDD: ("POP_INDEXED_LOCALMEM_LONG" ,4),
    0xDE: ("EFFECT_INDEXED_LOCALMEM_LONG" ,5),
    0xDF: ("REFERENCE_INDEXED_LOCALMEM_LONG" ,4),
    
    0xe0: ("ROTATE_RIGHT", 0),
    0xe1: ("ROTATE_LEFT", 0),
    0xe2: ("SHIFT_RIGHT", 0),
    0xe3: ("SHIFT_LEFT", 0),
    0xe4: ("LIMIT_MIN", 0),
    0xe5: ("LIMIT_MAX", 0),
    0xe6: ("NEGATE", 0),
    0xe7: ("COMPLEMENT", 0),
    0xe8: ("BIT_AND", 0),
    0xE9: ("ABSOLUTE_VALUE", 0),
    0xea: ("BIT_OR", 0),
    0xeb: ("BIT_XOR", 0),
    0xEC: ("ADD", 0),
    0xED: ("SUBTRACT", 0),
    0xee: ("ARITH_SHIFT_RIGHT", 0),
    0xef: ("BIT_REVERSE", 0),
    0xf0: ("LOGICAL_AND", 0),
    0xF1: ("ENCODE", 0),
    0xf2: ("LOGICAL_OR", 0),
    0xF3: ("DECODE", 0),
    0xf4: ("MULTIPLY", 0),
    0xf5: ("MULTIPLY_HI", 0),
    0xf6: ("DIVIDE", 0),
    0xf7: ("MODULO", 0),
    0xf8: ("SQUARE_ROOT", 0),
    0xf9: ("LESS", 0),
    0xfa: ("GREATER", 0),
    0xfb: ("NOT_EQUAL", 0),
    0xfc: ("EQUAL", 0),
    0xfd: ("LESS_EQUAL", 0),
    0xfe: ("GREATER_EQUAL", 0),
    0xFF: ("LOGICAL_NOT", 0),
    }

lops = {
    0x00: "COPY",
    0x08: "PRE_RANDOM",
    0x0C: "POST_RANDOM",
    
    0x10: "PRE_EXTEND_8",
    0x14: "PRE_EXTEND_16",
    0x18: "POST_EXTEND_8",
    0x1C: "POST_EXTEND_16",

    0x20: "PRE_INCREMENT_COGMEM",
    0x22: "PRE_INCREMENT_BYTE",
    0x24: "PRE_INCREMENT_WORD",
    0x26: "PRE_INCREMENT_LONG",
    0x28: "POST_INCREMENT_COGMEM",
    0x2A: "POST_INCREMENT_BYTE",
    0x2C: "POST_INCREMENT_WORD",
    0x2E: "POST_INCREMENT_LONG",

    0x30: "PRE_DECREMENT_COGMEM",
    0x32: "PRE_DECREMENT_BYTE",
    0x34: "PRE_DECREMENT_WORD",
    0x36: "PRE_DECREMENT_LONG",
    0x38: "POST_DECREMENT_COGMEM",
    0x3A: "POST_DECREMENT_BYTE",
    0x3C: "POST_DECREMENT_WORD",
    0x3E: "POST_DECREMENT_LONG",

    0x40: "ROTATE_RIGHT",
    0x41: "ROTATE_LEFT",
    0x42: "SHIFT_RIGHT",
    0x43: "SHIFT_LEFT",
    0x44: "MINIMUM",
    0x45: "MAXIMUM",
    0x46: "NEGATE",
    0x47: "COMPLEMENT",
    0x48: "BIT_AND",
    0x49: "ABSOLUTE_VALUE",
    0x4a: "BIT_OR",
    0x4b: "BIT_XOR",
    0x4c: "ADD",
    0x4d: "SUBTRACT",
    0x4e: "ARITH_SHIFT_RIGHT",
    0x4f: "BIT_REVERSE",
    
    0x50: "LOGICAL_AND",
    0x51: "ENCODE",
    0x52: "LOGICAL_OR",
    0x53: "DECODE",
    0x54: "MULTIPLY",
    0x55: "MULTIPLY_HI",
    0x56: "DIVIDE",
    0x57: "MODULO",
    0x58: "SQUARE_ROOT",
    0x59: "LESS",
    0x5a: "GREATER",
    0x5b: "NOT_EQUAL",
    0x5c: "EQUAL",
    0x5d: "LESS_EQUAL",
    0x5e: "GREATER_EQUAL",
    0x5F: "NOT",
    }

CogReg = {
    0x00 : "MEM_0",
    0x01 : "MEM_1",
    0x02 : "MEM_2",
    0x03 : "MEM_3",
    0x04 : "MEM_4",
    0x05 : "MEM_5",
    0x06 : "MEM_6",
    0x07 : "MEM_7",
    0x08 : "MEM_8",
    0x09 : "MEM_9",
    0x0A : "MEM_A",
    0x0B : "MEM_B",
    0x0C : "MEM_C",
    0x0D : "MEM_D",
    0x0E : "MEM_E",
    0x0F : "MEM_F",
    0x10 : "PAR",
    0x11 : "CNT",
    0x12 : "INA",
    0x13 : "INB",
    0x14 : "OUTA",
    0x15 : "OUTB",
    0x16 : "DIRA",
    0x17 : "DIRB",
    0x18 : "CTRA",
    0x19 : "CTRB",
    0x1A : "FRQA",
    0x1B : "FRQB",
    0x1C : "PHSA",
    0x1D : "PHSB",
    0x1E : "VCFG",
    0x1F : "VSCL"
    }

# --- Block insert these, make my life easier ---
for i in range( 8 ):
    simpleOps[i*4+0x40] = ("PUSH_VARMEM_LONG_%x"%(i),0)
    simpleOps[i*4+0x41] = ("POP_VARMEM_LONG_%x"%(i),0)
    simpleOps[i*4+0x42] = ("EFFECT_VARMEM_LONG_%x"%(i),1)
    simpleOps[i*4+0x43] = ("REFERENCE_VARMEM_LONG_%x"%(i),0)
    simpleOps[i*4+0x60] = ("PUSH_LOCALMEM_LONG_%x"%(i),0)
    simpleOps[i*4+0x61] = ("POP_LOCALMEM_LONG_%x"%(i),0)
    simpleOps[i*4+0x62] = ("EFFECT_LOCALMEM_LONG_%x"%(i),1)
    simpleOps[i*4+0x63] = ("REFERENCE_LOCALMEM_LONG_%x"%(i),0)

v1 = 0x100 - (len(simpleOps))
v2 = 0x80 - len(lops)

print v1, "voids remaining in main instruction set"
print v2, "voids remaining in the arithmatic set"
print "%2.2f%% Completed" % (100.0 * (0x180-v1-v2) / 0x180)

def PackedRelative( fo, addresses ):
    code = ord(fo.read(1))

    if code & 0x80 != 0:
        code = ord(fo.read(1)) | (code<<8)

        if code & 0x4000:    
            code -= 0x10000
        else:
            code &= 0x3FFF
    else:
        if code & 0x40:
            code -= 0x80        

    if code >= 0:
        addresses += [fo.tell()+code]

    return code

def PrintLOP( fo, addresses ):
    op = ord(fo.read(1))

    if (op & 0x80) == 0:
        print "POP",

    op &= 0x7F

    if op == 0x02:
        print "REPEAT_COMPARE", PackedRelative(fo, addresses)
    elif op == 0x06:
        print "REPEAT_COMPARE_STEP", PackedRelative(fo, addresses)
    elif op in lops:
        print lops[op]
    else:
        raise "UNKNOWN", hex(op)


def DoFunction( fo, base, end ):
    fo.seek(base)

    addresses = []
    while True:
        # Clear bypassed operations
        naddr = []
        for a in addresses:
            if a > fo.tell():
                naddr += [a]
            if a >= end:
                raise "BRANCH OUT OF RANGE"
        addresses = naddr

        x = ord(fo.read(1))        
        
        print "\t%x:\t%x\t" % (fo.tell()-1,x),
        
        if x in simpleOps:
            head, uop = simpleOps[x]

            print head,

            if uop == 1:
                PrintLOP(fo,addresses)
                
            elif uop == 2:
                print PackedRelative(fo,addresses)
                
            elif uop == 3:
                data = ord(fo.read(1))

                if data < 0x20:
                    print "%x -> %x" % (data, (2 << (data & 0x1F)))
                elif data < 0x40:
                    print "%x -> %x" % (data, (2 << (data & 0x1F))-1)
                elif data < 0x60:
                    print "%x -> %x" % (data, ~((2 << (data & 0x1F))))
                elif data < 0x80:
                    print "%x -> %x" % (data, ~((2 << (data & 0x1F))-1))
                else:
                    raise "Unknown packed literal", hex(data)
                    
            elif uop == 4 or uop == 5:
                data = ord(fo.read(1))

                if data & 0x80:
                    data = ord(fo.read(1)) | (data << 8) & 0x7FFF

                print "[%x]" % data,

                if uop == 5:
                    PrintLOP(fo,addresses)
                else:
                    print

            elif uop == 6:
                print "%i" % struct.unpack("B",fo.read(1))
            elif uop == 7:
                print "%i" % struct.unpack(">H",fo.read(2))
            elif uop == 8:
                print "%i" % struct.unpack(">I","\x00"+fo.read(3))
            elif uop == 9:
                print "%i" % struct.unpack(">I",fo.read(4))
            elif uop == 10:
                print "%i.%i" % struct.unpack("BB",fo.read(2))
            elif uop == 11:
                op = ord(fo.read(1))
                style = op & 0xE0
                    
                print CogReg[op & 0x1F],
                
                if style == 0x80:
                    print "PUSH"
                elif style == 0xA0:
                    print "POP"
                elif style == 0xC0:
                    print "EFFECTED",
                    PrintLOP(fo,addresses)
                else:
                    raise "UNKNOWN REG STYLE", hex(op)
            else:
                print

        else:
            raise "Unknown Op Code", hex(x)

        if len(addresses) == 0 and x == 0x32:
            break

    DoDataChunk( fo, fo.tell(), end )

def DoDataChunk( fo, base, end ):
    if base >= end:
        return
    
    fo.seek(base)
    print "Data chunk %x" % base

    print "\tbyte ",
    i = 16

    for c in fo.read(end - base):
        a = ord(c)

        if a <= 0x7E and a >= 0x20:
            print "'%s'," % c,
        elif a < 0x10:
            print "$0%x," % a,
        else:
            print "$%x," % a,

        i = i - 1
        if i == 0:
            i = 16
            print
            print "\tbyte ",
    print

def DoChunk( fo, base = 0, stack = 0 ):
    print "Object: %x %x" % (base, stack)

    fo.seek(base)
    size, longs, objects = struct.unpack("HBB",fo.read(4))

    funct_off = []
    object_off = []

    for i in range( 1, longs ):
        funct_off += [struct.unpack("HH",fo.read(4))]

    for i in range( objects ):
        object_off += [struct.unpack("HH",fo.read(4))]

    DoDataChunk(fo, fo.tell(), funct_off[0][0] + base )

    for i in range(len(funct_off)):
        offset, stackSize = funct_off[i]
        print "Function: %x ( %i bytes of stack )" % (offset+base,stackSize)

        if i+1 == len(funct_off):
            end = base+size
        else:
            end = funct_off[i+1][0]+base

        DoFunction( fo, offset+base, end )

    print
    
    for offset, unknown in object_off:
        DoChunk( fo, offset+base, unknown )

OSCM = { 0x00: "XINPUT", 0x08: "XTAL1", 0x10: "XTAL2", 0x18: "XTAL3" }
CLKSEL = {
        0: "RCFAST",
        1: "RCSLOW",
        2: "XINPUT",
        3: "PLL1X",
        4: "PLL2X",
        5: "PLL4X",
        6: "PLL8X",
        7: "PLL16X"
        }

def DumpClockMode(clk):
    print "Clock Mode:",
    if clk & 0x80:
        print "RESET",
    if clk & 0x40:
        print "PLL",
    if clk & 0x20:
        print OSCM[ clk & 0x18 ],

    print CLKSEL[ clk & 0x7 ]


def DumpChecksum(f,checksum_target,checksum):
    size = checksum_target - 20
    print "Total Data Checksumed: ", size
    print "Checksum: %x" % (checksum),

    f.seek(0)
    d = f.read(size)
    cs = 20
    
    for c in d:
        cs = (cs - ord(c)) & 0xFF
    if (cs & 0xFF) == 0:
        print "- Valid"
    else:
        print "- Invalid", cs & 0xFF

def DumpHeader(f):
    mhz,clk,checksum,first_object,var,free,entry_function,checksum_target = struct.unpack("IBBHHHHH",f.read(16))

    print "System Clock Rate: %imhz" %(mhz)
    DumpClockMode(clk)
    print
    print "Start of Variable Space: %x" % var
    print "End of EEPROM: %x" % free
    print "Checksum Target: %x" % checksum_target
    print "Entry Function: %x" % entry_function
    print "First Object: %x" % first_object

    DumpChecksum(f,free,checksum)

    print
    DoChunk( f, 0x10 )
    

def Disassemble(fn):
    print "--- STARTING OBJECT DUMP FOR %s ---" % fn

    f = file(fn,"rb")
    try:
        DumpHeader(f)
    finally:
        f.close()

#Disassemble( "Stack Length Demo.binary" )
Disassemble(sys.argv[1])
