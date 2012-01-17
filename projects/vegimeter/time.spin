' LCC 4.2 for Parallax Propeller
' (Catalina code generator by Ross Higson)
'
CON

#include "Constants.inc"

PUB Base : addr
   addr := @@0 ' Catalina Base Address

' Catalina Import main

DAT
        org  0
'
' first 2 longs reserved (for POD)
'
        long 0          '$00
        long 0          '$01
'                           
INIT    jmp  0          '$02
LODL    jmp  0          '$03
LODA    jmp  0          '$04
LODF    jmp  0          '$05
PSHL    jmp  0          '$06
PSHB    jmp  0          '$07
CPYB    jmp  0          '$08
NEWF    jmp  0          '$09
RETF    jmp  0          '$0a
CALA    jmp  0          '$0b
RETN    jmp  0          '$0c
CALI    jmp  0          '$0d
JMPA    jmp  0          '$0e
JMPI    jmp  0          '$0f
DIVS    jmp  0          '$10
DIVU    jmp  0          '$11
MULT    jmp  0          '$12
BR_Z    jmp  0          '$13
BRNZ    jmp  0          '$14
BRAE    jmp  0          '$15
BR_A    jmp  0          '$16
BRBE    jmp  0          '$17
BR_B    jmp  0          '$18
SYSP    jmp  0          '$19
PSHA    jmp  0          '$1a
FADD    jmp  0          '$1b
FSUB    jmp  0          '$1c
FMUL    jmp  0          '$1d
FDIV    jmp  0          '$1e
FCMP    jmp  0          '$1f
FLIN    jmp  0          '$20
INFL    jmp  0          '$21
PSHM    jmp  0          '$22
POPM    jmp  0          '$23
PSHF    jmp  0          '$24
RLNG    jmp  0          '$25
RWRD    jmp  0          '$26
RBYT    jmp  0          '$27
WLNG    jmp  0          '$28
WWRD    jmp  0          '$29
WBYT    jmp  0          '$2a
'                           
PC      long 0          '$2b
SP      long 0          '$2c
FP      long 0          '$2d
RI      long 0          '$2e
BC      long 0          '$2f
BA      long 0          '$30
BZ      long 0          '$31
CS      long 0          '$32
'
r0      long 0          '$33
r1      long 0          '$34
r2      long 0          '$35
r3      long 0          '$36
r4      long 0          '$37
r5      long 0          '$38
r6      long 0          '$39
r7      long 0          '$3a
r8      long 0          '$3b
r9      long 0          '$3c
r10     long 0          '$3d
r11     long 0          '$3e
r12     long 0          '$3f
r13     long 0          '$40
r14     long 0          '$41
r15     long 0          '$42
r16     long 0          '$43
r17     long 0          '$44
r18     long 0          '$45
r19     long 0          '$46
r20     long 0          '$47
r21     long 0          '$48
r22     long 0          '$49
r23     long 0          '$4a
'
Bit31   long  $80000000 '$4b
all_1s  long  $ffffffff '$4c
cviu_m1 long  $000000ff '$4d
cviu_m2 long  $0000ffff '$4e
top8    long  $ff000000 '$4f   ' top 8 bits bitmask
low24   long  $00ffffff '$50   ' low 24 bits bitmask
'
init_BZ long  @sbrkinit '$51   ' end of code / start of heap
init_PC long  @C_main   '$52   ' the initial PC
'
' seglayout specifies the layout of the segments (0, 1, 2, 3, 4, 5)
'
seglayout
        long  SEGMENT_LAYOUT
'
' segtable contains the start address of each of the segments
'
segtable
        long  @Catalina_Code
        long  @Catalina_Cnst
        long  @Catalina_Init
        long  @Catalina_Data
        long  @Catalina_Ends
        long  @Catalina_RO_Base
        long  @Catalina_RW_Base
'
' initial file is catalina_progbeg.s

' input file /usr/local/lib/catalina/target/catalina_default.s 

' input file time.spin 

' input file /usr/local/lib/catalina/target/lmm_progend.s 


CON

SEGMENT_LAYOUT=0 ' LMM segment layout (Code, Cnst, Init, Data)


DAT

Catalina_RO_Base

' Catalina Code

DAT ' Code segment

 long ' align long

Catalina_Code
'
DAT ' code segment

 long ' align long
'
' Initial PASM goes here (if any) ...
'
'

DAT ' code segment

' Catalina Export _exit

 long ' align long

C__exit
' jmp #JMPA
' long @C__exit
 mov r0,#$80
 clkset r0

' Catalina Export _sys_plugin

C__sys_plugin
 jmp #SYSP
 jmp #RETN

{
#ifdef REG_PASSING

' not too bad ...
C__sys_plugin
 jmp #SYSP
 jmp #RETN

#else

' very inefficient! ...
C__sys_plugin
 jmp #NEWF
 mov RI, FP
 add RI, #8
 rdlong r2,RI
 mov RI, FP
 add RI, #12
 rdlong r3,RI
 jmp #SYSP
 jmp #RETF

#endif
}

DAT ' code segment

'
' C_arg_setup : setup argc in r3 and argv in r2
'
C_arg_setup
 jmp #LODA                 ' point to argc address
 long @C_argc_locn
#ifdef LARGE
 jmp #RLNG
#elseifdef SMALL
 jmp #RLNG
#else
 rdlong BC,RI
#endif 
 rdword r3,BC              ' load argc
 add BC,#2
 rdword r2,BC              ' load argv
 jmp #RETN                 ' done

C_argc_locn
 long $7F30                ' must match value in Catalina_Common.spin

'
' C_debug_init : just in case we use '-g' but then specify the default target
'
C_debug_init
 jmp #RETN                 ' done

'
' Target-specific PASM goes here ...
'

DAT ' code segment

'
' Final PASM goes here (if any) ...
'


' Catalina Cnst

DAT ' Cnst segment

 long ' align long

Catalina_Cnst

DAT

Catalina_RW_Base

' Catalina Init

DAT ' Init segment

 long ' align long

Catalina_Init

DAT ' initalized data segment

' Catalina Export errno

 long ' align long

C_errno long 0


' Catalina Data

DAT ' Data segment

 long ' align long

Catalina_Data

DAT ' unitialized data segment

 long ' align long
'
' sbrkinit is used by sbrk - it must be after all variables and data
'
sbrkinit  ' heap starts here

 long 0 ' this long is required to workaround an obscure homespun bug!!!



 long ' align long
Catalina_Ends ' end of segments
