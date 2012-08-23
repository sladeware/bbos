#!/usr/bin/env python

#DESPIN.PY
# A Spin bytecode disassebler
# (c) Steve Waddicor 2007

import sys

(
OP_NONE,
OP_BYTE_ADDRESS,
OP_LOC_DO,
OP_DO,
OP_PACKED_LITERAL,
OP_BYTE_LITERAL,
OP_WORD_LITERAL,
OP_SEMILONG_LITERAL,
OP_LONG_LITERAL,
OP_BYTE_METHOD_NUMBER,
OP_UNSIGNED_OFFSET,
OP_OBJECT_OFFSET,
OP_BRANCH,
OP_COG_REGISTER_OPERATION,
OP_UNSIGNED_EFFECTED_OFFSET,
)=range(15)

(
ASM_OP_NONE,
ASM_OP_JMP,
ASM_OP_RD_WR_HUB,
ASM_OP_NOP,
)=range(4)

FOLLOW_ON = 0
SEPARATE_BLANK = 1
SEPARATE_COMMENT = 2

buffer=[]
p=0
cog_p=0
object_start = 0x10
_main=0
label_table = []
label_dict = {}
cog_label_table = []
cog_label_dict = {}
object_table = []
object_dict = {}
class_table = []
class_dict = {}
output=False

dict={
    0x00 : ("FRAME_CALL_RETURN",                  OP_NONE), # x := Method(y)
    0x01 : ("FRAME_CALL_NORETURN",                OP_NONE), # Method(y)
    0x02 : ("FRAME_CALL_ABORT",                   OP_NONE), # x := \Method(y)
    0x03 : ("FRAME_CALL_TRASHABORT",              OP_NONE), # \Method(y)
    0x04 : ("BRANCH",                             OP_BRANCH),
    0x05 : ("CALL",OP_BYTE_METHOD_NUMBER),              #followed by a byte that indexes the method number from 1
    0x08 : ("LOOP_START",                         OP_BRANCH),
    0x09 : ("LOOP_CONTINUE",                      OP_BRANCH),
    0x0a : ("BRANCH_IF_FALSE",                    OP_BRANCH),
    0x0b : ("BRANCH_IF_TRUE",                     OP_BRANCH),
    0x0c : ("JUMP_FROM_STACK",                    OP_NONE),
    0x0d : ("COMPARE_CASE",                       OP_BRANCH),
    0x0e : ("COMPARE_CASE_RANGE",                 OP_BRANCH),
    0x0f : ("LOOK_ABORT",                         OP_NONE),
    0x10 : ("LOOKUP_COMPARE",                     OP_NONE),
    0x11 : ("LOOKDOWN_COMPARE",                   OP_NONE),
    0x12 : ("LOOKUPRANGE_COMPARE",                OP_NONE),
    0x13 : ("LOOKDOWNRANGE_COMPARE",              OP_NONE),
    0x15 : ("MARK_INTERPRETED",                   OP_NONE),
    0x16 : ("STRSIZE",                            OP_NONE),
    0x21 : ("COGSTOP",                            OP_NONE),
    0x23 : ("WAITCNT",                            OP_NONE),
    0x28 : ("COGINIT_RETURNS",                    OP_NONE),
    0x2c : ("COGINIT",                            OP_NONE),
    0x30 : ("ABORT",OP_NONE),
    0x32 : ("RETURN",OP_NONE),
    0x33 : ("POP_RETURN",                         OP_NONE),
    0x34 : ("PUSH_NEG1",                          OP_NONE),
    0x35 : ("PUSH_0",                             OP_NONE),
    0x36 : ("PUSH_1",                             OP_NONE),
    0x37 : ("PUSH_PACKED_LIT",                    OP_PACKED_LITERAL),
    0x38 : ("PUSH_BYTE_LIT",                      OP_BYTE_LITERAL),
    0x39 : ("PUSH_WORD_LIT",                      OP_WORD_LITERAL),
    0x3a : ("PUSH_MID_LIT",                       OP_SEMILONG_LITERAL),
    0x3b : ("PUSH_LONG_LIT",                      OP_LONG_LITERAL),
    0x3d : ("BITFIELD_COG_REGISTER_OP",           OP_COG_REGISTER_OPERATION),
    0x3f : ("COG_REGISTER_OP",                    OP_COG_REGISTER_OPERATION),
    0x40 : ("PUSH_VARMEM_LONG_0",                 OP_NONE),
    0x41 : ("POP_VARMEM_LONG_0",                  OP_NONE),
    0x42 : ("EFFECT_VARMEM_LONG_0",               OP_DO),
    0x43 : ("REFERENCE_VARMEM_LONG_0",            OP_NONE),
    0x44 : ("PUSH_VARMEM_LONG_1",                 OP_NONE),
    0x45 : ("POP_VARMEM_LONG_1",                  OP_NONE),
    0x46 : ("EFFECT_VARMEM_LONG_1",               OP_DO),
    0x47 : ("REFERENCE_VARMEM_LONG_1",            OP_NONE),
    0x48 : ("PUSH_VARMEM_LONG_2",                 OP_NONE),
    0x49 : ("POP_VARMEM_LONG_2",                  OP_NONE),
    0x4a : ("EFFECT_VARMEM_LONG_2",               OP_DO),
    0x4b : ("REFERENCE_VARMEM_LONG_2",            OP_NONE),
    0x4c : ("PUSH_VARMEM_LONG_3",                 OP_NONE),
    0x4d : ("POP_VARMEM_LONG_3",                  OP_NONE),
    0x4e : ("EFFECT_VARMEM_LONG_3",               OP_DO),
    0x4f : ("REFERENCE_VARMEM_LONG_3",            OP_NONE),
    0x50 : ("PUSH_VARMEM_LONG_4",                 OP_NONE),
    0x51 : ("POP_VARMEM_LONG_4",                  OP_NONE),
    0x52 : ("EFFECT_VARMEM_LONG_4",               OP_DO),
    0x53 : ("REFERENCE_VARMEM_LONG_4",            OP_NONE),
    0x54 : ("PUSH_VARMEM_LONG_5",                 OP_NONE),
    0x55 : ("POP_VARMEM_LONG_5",                  OP_NONE),
    0x56 : ("EFFECT_VARMEM_LONG_5",               OP_DO),
    0x57 : ("REFERENCE_VARMEM_LONG_5",            OP_NONE),
    0x58 : ("PUSH_VARMEM_LONG_6",                 OP_NONE),
    0x59 : ("POP_VARMEM_LONG_6",                  OP_NONE),
    0x5a : ("EFFECT_VARMEM_LONG_6",               OP_DO),
    0x5b : ("REFERENCE_VARMEM_LONG_6",            OP_NONE),
    0x5c : ("PUSH_VARMEM_LONG_7",                 OP_NONE),
    0x5d : ("POP_VARMEM_LONG_7",                  OP_NONE),
    0x5e : ("EFFECT_VARMEM_LONG_7",               OP_DO),
    0x5f : ("REFERENCE_VARMEM_LONG_7",            OP_NONE),
    0x60 : ("PUSH_LOCALMEM_LONG_0",               OP_NONE),
    0x61 : ("POP_LOCALMEM_LONG_0",                OP_NONE),
    0x62 : ("EFFECT_LOCALMEM_LONG_0",             OP_DO),
    0x63 : ("REFERENCE_LOCALMEM_LONG_0",          OP_NONE),
    0x64 : ("PUSH_LOCALMEM_LONG_1",               OP_NONE),
    0x65 : ("POP_LOCALMEM_LONG_1",                OP_NONE),
    0x66 : ("EFFECT_LOCALMEM_LONG_1",             OP_DO),
    0x67 : ("REFERENCE_LOCALMEM_LONG_1",          OP_NONE),
    0x68 : ("PUSH_LOCALMEM_LONG_2",               OP_NONE),
    0x69 : ("POP_LOCALMEM_LONG_2",                OP_NONE),
    0x6a : ("EFFECT_LOCALMEM_LONG_2",             OP_DO),
    0x6b : ("REFERENCE_LOCALMEM_LONG_2",          OP_NONE),
    0x6c : ("PUSH_LOCALMEM_LONG_3",               OP_NONE),
    0x6d : ("POP_LOCALMEM_LONG_3",                OP_NONE),
    0x6e : ("EFFECT_LOCALMEM_LONG_3",             OP_DO),
    0x6f : ("REFERENCE_LOCALMEM_LONG_3",          OP_NONE),
    0x70 : ("PUSH_LOCALMEM_LONG_4",               OP_NONE),
    0x71 : ("POP_LOCALMEM_LONG_4",                OP_NONE),
    0x72 : ("EFFECT_LOCALMEM_LONG_4",             OP_DO),
    0x73 : ("REFERENCE_LOCALMEM_LONG_4",          OP_NONE),
    0x74 : ("PUSH_LOCALMEM_LONG_5",               OP_NONE),
    0x75 : ("POP_LOCALMEM_LONG_5",                OP_NONE),
    0x76 : ("EFFECT_LOCALMEM_LONG_5",             OP_DO),
    0x77 : ("REFERENCE_LOCALMEM_LONG_5",          OP_NONE),
    0x78 : ("PUSH_LOCALMEM_LONG_6",               OP_NONE),
    0x79 : ("POP_LOCALMEM_LONG_6",                OP_NONE),
    0x7a : ("EFFECT_LOCALMEM_LONG_6",             OP_DO),
    0x7b : ("REFERENCE_LOCALMEM_LONG_6",          OP_NONE),
    0x7c : ("PUSH_LOCALMEM_LONG_7",               OP_NONE),
    0x7d : ("POP_LOCALMEM_LONG_7",                OP_NONE),
    0x7e : ("EFFECT_LOCALMEM_LONG_7",             OP_DO),
    0x7f : ("REFERENCE_LOCALMEM_LONG_7",          OP_NONE),
#byte addressing 0x80 - 0x9f
    0x87 : ("REFERENCE_OBJECTMEM_BYTE",           OP_UNSIGNED_OFFSET), #Byte offset from beginning of object
#word addressing 0xa0 - 0xbf
    0x91 : ("POP_INDEXED_MAINMEM_BYTE",           OP_NONE),
    0x94 : ("PUSH_INDEXED_OBJECTMEM_BYTE",        OP_UNSIGNED_OFFSET),
    0x98 : ("PUSH_INDEXED_VARIABLEMEM_BYTE",      OP_UNSIGNED_OFFSET),
    0x99 : ("POP_INDEXED_VARIABLEMEM_BYTE",       OP_UNSIGNED_OFFSET),
    0xa8 : ("PUSH_VARIABLEMEM_WORD",              OP_UNSIGNED_OFFSET),
    0xa9 : ("POP_VARIABLEMEM_WORD",               OP_UNSIGNED_OFFSET),
    0xaa : ("do_word_var_@",OP_LOC_DO),
    0xab : ("push_word_var_adr",OP_UNSIGNED_OFFSET),
#long addressing 0xc0 - 0xdf
    0xb4 : ("PUSH_INDEXED_OBJECTMEM_WORD",        OP_UNSIGNED_OFFSET),
    0xb6 : ("EFFECT_INDEXED_OBJECTMEM_WORD",      OP_UNSIGNED_EFFECTED_OFFSET),
    0xc7 : ("REFERENCE_OBJECTMEM_LONG",           OP_OBJECT_OFFSET),
    0xc8 : ("PUSH_VARIABLEMEM_LONG",              OP_UNSIGNED_OFFSET),
    0xc9 : ("POP_VARIABLEMEM_LONG",               OP_UNSIGNED_OFFSET),
#operators
    0xd8 : ("PUSH_INDEXED_VARIABLEMEM_LONG",      OP_UNSIGNED_OFFSET),
    0xd9 : ("POP_INDEXED_VARIABLEMEM_LONG",       OP_UNSIGNED_OFFSET),
    0xdb : ("REFERENCE_INDEXED_VARIABLEMEM_LONG", OP_UNSIGNED_OFFSET),
    0xe0 : ("->",OP_NONE),
    0xe1 : ("<-",OP_NONE),
    0xe2 : (">>",OP_NONE),
    0xe3 : ("<<",OP_NONE),
    0xe4 : ("#>",OP_NONE),
    0xe5 : ("<#",OP_NONE),
    0xe6 : ("negate",OP_NONE),
    0xe7 : ("!",OP_NONE),
    0xe8 : ("&",OP_NONE),
    0xea : ("|",OP_NONE),
    0xeb : ("^",OP_NONE),
    0xec : ("+",OP_NONE),
    0xed : ("-",OP_NONE),
    0xee : ("~>",OP_NONE),
    0xef : ("><",OP_NONE),
    0xf0 : ("AND",OP_NONE),
    0xf2 : ("OR",OP_NONE),
    0xf4 : ("*",OP_NONE),
    0xf5 : ("**",OP_NONE),
    0xf6 : ("/",OP_NONE),
    0xf7 : ("//",OP_NONE),
    0xf9 : ("<",OP_NONE),
    0xfa : (">",OP_NONE),
    0xfb : ("<>",OP_NONE),
    0xfc : ("==",OP_NONE),
    0xfd : ("=<",OP_NONE),
    0xfe : ("=>",OP_NONE),
    }

do_dict = {
    0x00 : "COPY",
    0X02 : "REPEAT_COMPARE",
    0X08 : "PRE_RND",
    0X0C : "POST_RND",
    0X10 : "SIGN_EXTEND_BYTE",
    0X14 : "SIGN_EXTEND_WORD",
    0X18 : "POST_CLEAR",
    0X1C : "POST_SET_TRUE",
    0X24 : "PRE_INCREMENT",
    0X2C : "POST_INCREMENT",
    0x2E : "POST_INCREMENT_LONG",
    0X34 : "PRE_DECREMENT",
    0X3C : "POST_DECREMENT",
    0X47 : "BITWISE_NOT",
    0X49 : "ABS",
    0X4C : "+=",
    0X51 : "ENCODE",
    0X53 : "DECODE",
    0X58 : "SQR",
    0X5F : "LOGICAL_NOT",
    }

cog_register_dict = {
    0x00 : "R0",
    0x01 : "R1",
    0x02 : "R2",
    0x03 : "R3",
    0x04 : "R4",
    0x05 : "R5",
    0x06 : "R6",
    0x07 : "R7",
    0x08 : "R8",
    0x09 : "R9",
    0x0a : "R10",
    0x0b : "R11",
    0x0c : "R12",
    0x0d : "R13",
    0x0e : "R14",
    0x0f : "R15",
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
    0x1a : "FRQA",
    0x1b : "FRQB",
    0x1c : "PHSA",
    0x1d : "PHSB",
    0x1e : "VCFG",
    0x1f : "VSCL",
    }


asm_dict = {
    0x00 : ("byte",ASM_OP_RD_WR_HUB), #prepend "rd" or "wr" as appropriate late
    0x01 : ("word",ASM_OP_RD_WR_HUB),
    0x02 : ("long",ASM_OP_RD_WR_HUB),
    0x03 : ("hubop",ASM_OP_NONE),
    0x04 : ("mul",ASM_OP_NONE),
    0x05 : ("muls",ASM_OP_NONE),
    0x06 : ("enc",ASM_OP_NONE),
    0x07 : ("ones",ASM_OP_NONE),
    0x08 : ("ror",ASM_OP_NONE),
    0x09 : ("rol",ASM_OP_NONE),
    0x0a : ("shr",ASM_OP_NONE),
    0x0b : ("shl",ASM_OP_NONE),
    0x0c : ("rcr",ASM_OP_NONE),
    0x0d : ("rcl",ASM_OP_NONE),
    0x0e : ("sar",ASM_OP_NONE),
    0x0f : ("rev",ASM_OP_NONE),
    0x10 : ("mins",ASM_OP_NONE),
    0x11 : ("maxs",ASM_OP_NONE),
    0x12 : ("min",ASM_OP_NONE),
    0x13 : ("max",ASM_OP_NONE),
    0x14 : ("movs",ASM_OP_NONE),
    0x15 : ("movd",ASM_OP_NONE),
    0x16 : ("movi",ASM_OP_NONE),
    0x17 : ("jmp",ASM_OP_JMP),
    0x18 : ("and",ASM_OP_NONE),
    0x19 : ("andn",ASM_OP_NONE),
    0x1a : ("or",ASM_OP_NONE),
    0x1b : ("xor",ASM_OP_NONE),
    0x1c : ("muxc",ASM_OP_NONE),
    0x1d : ("muxnc",ASM_OP_NONE),
    0x1e : ("muxz",ASM_OP_NONE),
    0x1f : ("muxnz",ASM_OP_NONE),
    0x20 : ("add",ASM_OP_NONE),
    0x21 : ("sub",ASM_OP_NONE),
    0x22 : ("addabs",ASM_OP_NONE),
    0x23 : ("subabs",ASM_OP_NONE),
    0x24 : ("sumc",ASM_OP_NONE),
    0x25 : ("sumnc",ASM_OP_NONE),
    0x26 : ("sumz",ASM_OP_NONE),
    0x27 : ("sumnz",ASM_OP_NONE),
    0x28 : ("mov",ASM_OP_NONE),
    0x29 : ("neg",ASM_OP_NONE),
    0x2a : ("abs",ASM_OP_NONE),
    0x2b : ("absneg",ASM_OP_NONE),
    0x2c : ("negc",ASM_OP_NONE),
    0x2d : ("negnc",ASM_OP_NONE),
    0x2e : ("negz",ASM_OP_NONE),
    0x2f : ("negnz",ASM_OP_NONE),
    0x30 : ("cmps",ASM_OP_NONE),
    0x31 : ("cmpsx",ASM_OP_NONE),
    0x32 : ("addx",ASM_OP_NONE),
    0x33 : ("subx",ASM_OP_NONE),
    0x34 : ("adds",ASM_OP_NONE),
    0x35 : ("subs",ASM_OP_NONE),
    0x36 : ("addsx",ASM_OP_NONE),
    0x37 : ("subsx",ASM_OP_NONE),
    0x38 : ("cmpsub",ASM_OP_NONE),
    0x39 : ("djnz",ASM_OP_NONE),
    0x3a : ("tjnz",ASM_OP_NONE),
    0x3b : ("tjz",ASM_OP_NONE),
    0x3c : ("waitpeq",ASM_OP_NONE),
    0x3d : ("waitpne",ASM_OP_NONE),
    0x3e : ("waitcnt",ASM_OP_NONE),
    0x3f : ("waitvid",ASM_OP_NONE),
    }

condition_dict = {
    0x0 : "if_never",
    0x1 : "if_nz_and_nc",
    0x2 : "if_z_and_nc",
    0x3 : "if_nc",
    0x4 : "if_nz_and_c",
    0x5 : "if_nz",
    0x6 : "if_z_ne_c",
    0x7 : "if_nz_or_nc",
    0x8 : "if_z_and_c",
    0x9 : "if_z_eq_c",
    0xa : "if_z",
    0xb : "if_z_or_nc",
    0xc : "if_c",
    0xd : "if_nz_or_c",
    0xe : "if_z_or_c",
    0xf : "",
    }

register_dict = {
    0x1f0 : "par",
    0x1f1 : "cnt",
    0x1f2 : "ina",
    0x1f3 : "inb",
    0x1f4 : "outa",
    0x1f5 : "outb",
    0x1f6 : "dira",
    0x1f7 : "dirb",
    0x1f8 : "ctra",
    0x1f9 : "ctrb",
    0x1fa : "frqa",
    0x1fb : "frqb",
    0x1fc : "phsa",
    0x1fd : "phsb",
    0x1fe : "vcfg",
    0x1ff : "vscl",
}


def hexa(number,digits=2,prefix="$"):
    if number<0:
        return ("-"+prefix+"%0"+str(digits)+"X") % -number
    else:
        return (prefix+"%0"+str(digits)+"X") % number

def printo(*args):
    if output:
        for i in args:
            print i,
        print

def printo_(*args):
    if output:
        for i in args:
            print i,

def DeSpin(b):
    global _data
    global p
    global cog_p
    global dat_is_code
    global cog_index
    p=0
    cog_p = 0
    cog_index = 0
    dat_is_code = True
    DecodeProgramFrame()
    AddClassLabel("Class",p)
    while p<len(buffer):
        DecodeClassFrame()

def DecodeProgramFrame():
    global _main
    printo(hexa(p,4),"\t_long_freq\t\t\tLONG\t",GetLong())
    printo(hexa(p,4),"\t_clk\t\t\t\tBYTE\t",GetByte())
    printo(hexa(p,4),"\t_checksum\t\t\tBYTE\t",hexa(GetByte()))
    printo(hexa(p,4),"\t_program_base_address\t\tWORD\t",hexa(GetWord(),4),"\t(always $0010)?")
    printo(hexa(p,4),"\t_variable_space\t\t\tWORD\t",hexa(GetWord(),4))
    printo(hexa(p,4),"\t_stack_space\t\t\tWORD\t",hexa(GetWord(),4))
    printo_(hexa(p,4))
    _main = GetWord()
    printo("\t_main\t\t\t\tWORD\t",hexa(_main,4))
    printo(hexa(p,4),"\t_top_of_stack\t\t\tWORD\t",hexa(GetWord(),4))

def DecodeClassFrame():
    global p
    global class_frame_name
    global class_frame_data_start
    global class_frame_member_objects
    global class_frame_address

    class_frame_address = p
    class_frame_size = GetWord()
    AddClassLabel("Class",class_frame_address+class_frame_size)
    class_frame_name = class_table[class_dict[class_frame_address]]
    class_frame_data_start = GetByte()
    class_frame_member_objects = GetByte()

    PrintClassFrame(class_frame_address, class_frame_name, class_frame_size, class_frame_data_start, class_frame_member_objects)

    DecodeMethodTable()
    DecodeObjectTable()
    while Decode() and (not class_dict.has_key(p)):
        pass

def DecodeMethodTable():
    global _main
    global class_frame_data_start
    global class_frame_name
    global class_frame_address

    if class_frame_data_start>1:
        printo("' Method table                            Name,Start,Num_locals")
        printo("' ------------                            ---------------------------")
        m=1
        # _data gives number of words before data starts.  One word already taken, so _data-1 gives number of methods.
        for i in range(1,class_frame_data_start):
            address = p
            method = GetWord()
            locals = GetWord()
            methodName = AddMethodLabel(class_frame_name+"Method"+str(m), method+class_frame_address, locals)
            PrintMethodTableLine(address,methodName,method,locals)
            m+=1
        printo()

def DecodeObjectTable():
    global _main
    global class_frame_member_objects
    global class_frame_name
    if class_frame_member_objects>0:
        printo("' Object table                            Name,Start,Var_base")
        printo("' ------------                            -------------------")
        m=1
        for i in range(class_frame_member_objects):
            address=p
            start = GetWord()
            var_base = GetWord()
            objectName = AddObjectLabel(class_frame_name+"Object", start+0x10, var_base)
            try:
                objectType = class_table[class_dict[start+0x10]]
            except:
                objectType = "UnknownClass"
            PrintObjectTableLine(address,objectName,objectType,start,var_base)
            m+=1
        printo

def Decode():
    global p
    global _main
    global seperate
    if p<_main:
        separate=DecodeDat()
    else:
        separate=DecodeSpin()
    if separate == SEPARATE_BLANK:
        printo("\n")
    elif separate == SEPARATE_COMMENT:
        printo("                                                                    '")
    return p<len(buffer)

def Operand(instruction,operand_type,effects):
    if operand_type == ASM_OP_NOP:
        return ""
    source = instruction & 0x1FF
    if operand_type==ASM_OP_JMP:
        dest = ""
    else:
        dest = (instruction>>9) & 0x1FF
        if dest>=0x1F0:
            dest = register_dict.get(dest,hexa(dest,3))+","
        else:
            dest = AddCogLabel("CD",cog_index,dest)+","

    operand = dest
    if effects&0x1:
        operand+="#"
        if operand_type==ASM_OP_JMP:
            source = AddCogLabel("CC",cog_index,source)
        else:
            source = hexa(source,0)
    else:
        if source>=0x1F0:
            source = register_dict.get(source,hexa(source,3))
        else:
            source = AddCogLabel("CD",cog_index,source)

    operand+=source
    return operand

def DecodeDat():
    global p
    global cog_p
    global dat_is_code
    address = p
    if label_dict.has_key(p):
        printo(label_table[label_dict[p]][0])
    if cog_label_dict.has_key((cog_index,cog_p)):
        printo(cog_label_table[cog_label_dict[(cog_index,cog_p)]][0])
    instruction=GetLong()
    conditions = (instruction>>18) & 0xF
    if conditions==0 and instruction!=0:
        #IF_NEVER acts as NOP, but instruction isn't NOP.  Probably data.
        dat_is_code = False

    if dat_is_code:
        (opcode,operand_type) = asm_dict.get(instruction>>26, ("long",ASM_OP_NONE) )
        effects = (instruction>>22) & 0xF

        if operand_type==ASM_OP_RD_WR_HUB:
            if conditions==0:
                opcode = "nop"
                operand_type = ASM_OP_NOP
                conditions = 0xf #suppress "IF_NEVER" output
            elif effects&0x02:
                opcode = "rd"+opcode
            else:
                opcode = "wr"+opcode
        elif operand_type==ASM_OP_JMP:
            dat_is_code = False

        operand = Operand(instruction,operand_type,effects)
        PrintDatCodeLine(address,cog_p,instruction,condition_dict[conditions],opcode,operand)
    else:
        PrintDatDataLine(address,cog_p,instruction)
    cog_p+=1
    return FOLLOW_ON

def PrintClassFrame(address,name,size,start_of_data,num_objects):
    printo
    printo(  "' *******************************************************************************************************")
    printo(  "'                                         Name,Size,End_Method_Table_Offset,Num_Objects")
    printo( ("                CLASS                     %-25s ' %04X: %02X %02X %02X %02X" % (
        ",".join((name,str(size),hexa(start_of_data),str(num_objects))),address,size&0xFF,size>>8,start_of_data,num_objects)))
    printo(  "' *******************************************************************************************************")

def PrintMethodTableLine(address,name,start,length_of_local_variables):
    printo( ("                DECLARE_METHOD            %-25s ' %04X: %02X %02X %02X %02X" % (",".join((name,hexa(start+0x10,4),str(length_of_local_variables/4))),address,start&0xFF,start>>8,length_of_local_variables&0xFF,length_of_local_variables>>8)))

def PrintObjectTableLine(address,name,objectType,start,var_base):
    #print name,hexa(start+0x10,4),hexa(unknown)
    operand = ",".join( (name,objectType,hexa(var_base)) )
    #print class_dict
    #print class_table
    printo( ("                DECLARE_OBJECT            %-25s ' %04X: %02X %02X %02X %02X" % (
        operand,
        address,
        start&0xFF,
        start>>8,
        var_base&0xFF,
        var_base>>8
        )) )

def PrintDatCodeLine(address,cog_address,the_long,conditions,opcode,operand):
    printo("   %-12s %-25s %-25s ' %04X [%03X]: %02X_%02X_%02X_%02X" % (conditions,opcode,operand,address,cog_address,(the_long>>24)&0xFF,(the_long>>16)&0xFF,(the_long>>8)&0xFF,(the_long)&0xFF))

def PrintDatDataLine(address,cog_address,the_long):
    printo("                long                      $%08X                 ' %04X [%03X]: %02X_%02X_%02X_%02X" % (the_long,address,cog_address,(the_long>>24)&0xFF,(the_long>>16)&0xFF,(the_long>>8)&0xFF,(the_long)&0xFF))

def PrintSpinLine(address,bytes,opcode,operand,comment):
    #symbols max 30 chars
    global output
    if output:
        t_bytes = []
        for byte in bytes:
            t_bytes.append("%02X" % byte)
        t_bytes.extend( ("","","","","") )
        printo("                %-25s %-25s ' %04X: %2s %2s %2s %2s %2s    %-20s" % (opcode,operand,address,t_bytes[0],t_bytes[1],t_bytes[2],t_bytes[3],t_bytes[4],comment))

def DecodeSpin():
    global p
    global _main
    global _data
    operand = ""
    comment = ""
    if label_dict.has_key(p):
        printo("\n"+label_table[label_dict[p]][0])
    address = p
    bytes = [GetByte()]
    (opcode,operand_type) = dict.get(bytes[0], ("BYTE",OP_NONE) )
    if operand_type==OP_PACKED_LITERAL:
        bytes.append(GetByte())
        pow2=bytes[1] & 0x1f
        diff=bytes[1]>>5 & 0x1
        complement=bytes[1]>>6
        #print pow2,diff,complement
        if complement:
            operand = hexa(~(1<<(pow2+1))+diff)
        else:
            operand = hexa((1<<(pow2+1))-diff)
    elif operand_type==OP_BYTE_LITERAL:
        bytes.append(GetByte())
        operand=str(bytes[1])
    elif operand_type==OP_WORD_LITERAL:
        bytes.append(GetByte())
        bytes.append(GetByte())
        operand=str((bytes[1]<<8)+bytes[2])
    elif operand_type==OP_SEMILONG_LITERAL:
        bytes.append(GetByte())
        bytes.append(GetByte())
        bytes.append(GetByte())
        operand=str( (bytes[1]<<16) + (bytes[2]<<8) + bytes[3] )
    elif operand_type==OP_LONG_LITERAL:
        bytes.append(GetByte())
        bytes.append(GetByte())
        bytes.append(GetByte())
        bytes.append(GetByte())
        operand=str( (bytes[1]<<24) + (bytes[2]<<16) + (bytes[3]<<8) + bytes[4] )
    elif operand_type==OP_BYTE_METHOD_NUMBER:
        bytes.append(GetByte())
        operand=label_table[bytes[1]-1][0]
    elif operand_type==OP_BYTE_ADDRESS:
        bytes.append(GetByte())
        operand=hex(bytes[1])
    elif operand_type==OP_DO:
        bytes.append(GetByte())
        operand = do_dict.get(bytes[1]&0x7F, "Unknown op" )
        if operand == "repeat_compare":
            bytes.append(GetByte())
            offset = bytes[2]
            if bytes[2]&0x40:
                offset -= 128
            if bytes[2]&0x80:
                bytes.append(GetByte)
                offset = (var<<8) | bytes[3]
            operand+=","+hexa(offset)
    elif operand_type==OP_LOC_DO:
        bytes.append(GetByte())
        bytes.append(GetByte())
        var = hex(bytes[1])
        operand = do_dict.get(bytes[2], "Unknown op" )
        if operand == "repeat_compare":
            bytes.append(GetByte())
            offset = bytes[3]
            if bytes[3]&0x40:
                offset -= 128
            if bytes[3]&0x80:
                bytes.append(GetByte)
                offset = (var<<8) | bytes[4]
            operand+=","+hexa(offset)
        opcode += var
    elif operand_type==OP_BRANCH:
        bytes.append(GetByte())
        offset = bytes[1]
        if bytes[1]&0x40:
            offset -= 128
        if bytes[1]&0x80:
            bytes.append(GetByte())
            offset = (offset<<8) | bytes[2]
        operand = AddLabel("H",p+offset)
    elif operand_type==OP_UNSIGNED_OFFSET:
        bytes.append(GetByte())
        offset = bytes[1] & 0x7f
        if bytes[1]&0x80:
            bytes.append(GetByte())
            offset = (offset<<8) | bytes[2]
        if offset<0:
            operand = "$%02X" % -offset
        else:
            operand = "$%02X" % offset
    elif operand_type==OP_OBJECT_OFFSET:
        bytes.append(GetByte())
        offset = bytes[1] & 0x7f
        if bytes[1]&0x80:
            bytes.append(GetByte())
            offset = (offset<<8) | bytes[2]
        operand = AddLabel("H",object_start+offset)
    elif operand_type==OP_COG_REGISTER_OPERATION:
        bytes.append(GetByte())
        operation = bytes[1]&0xE0
        if operation==0x80:
            operand="PUSH"
        elif operation==0xA0:
            operand="POP"
        elif operation==0xC0:
            bytes.append(GetByte())
            operand=do_dict[bytes[2]]
        else:
            operand="UNKNOWN"
        operand += " "+cog_register_dict[bytes[1]&0x1F]

    elif opcode == "BYTE":
        operand = hexa(bytes[0])
    PrintSpinLine(address,bytes,opcode,operand,comment)
    if opcode == "RETURN":
        return SEPARATE_BLANK
    elif opcode.startswith("pop") or opcode=="branch":
        return SEPARATE_COMMENT
    return FOLLOW_ON

def AddCogLabel(label,cog_index,cog_p):
    label = label+str(cog_index)+"_"+("%03X")%cog_p
    if not cog_label_dict.has_key( (cog_index,cog_p) ):
        cog_label_dict[(cog_index,cog_p)] = len(cog_label_table)
        cog_label_table.append( (label, -1) )
    return label

def AddLabel(label,address):
    #print label,hex(address),locals
    label = label+("%04X")%address
    if not label_dict.has_key(address):
        label_dict[address] = len(label_table)
        label_table.append( (label, -1) )
    return label

def AddMethodLabel(label,address,locals):
    #print label,hex(address),locals
    if not label_dict.has_key(address):
        label_dict[address] = len(label_table)
        label_table.append( (label, locals) )
    return label

def AddObjectLabel(label,address,var_base):
    key = (address,var_base)
    if object_dict.has_key( key ):
        return object_table[object_dict[key]]
    else:
        label = label+str(len(object_table))
        object_dict[key] = len(object_table)
        object_table.append(label)
        return label

def AddClassLabel(label,address):
    key = address
    if class_dict.has_key( key ):
        return class_table[class_dict[key]]
    else:
        label = label+str(len(class_table)+1)
        class_dict[key] = len(class_table)
        class_table.append(label)
        return label

def GetLong():
    return GetByte()+GetByte()*0x100+GetByte()*0x10000+GetByte()*0x1000000

def GetWord():
    return GetByte()+GetByte()*0x100

def GetByte():
    global buffer
    global p
    ret = ord(buffer[p])
    p += 1
    return ret

if __name__	== '__main__':
    f=open(sys.argv[1],"rb")
    buffer=f.read()
    print "Pass 1..."
    output = False
    DeSpin(buffer)
    print "Pass 2..."
    output = True
    DeSpin(buffer)
    f.close()

