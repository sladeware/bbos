{
HYDRA XTREME 512K SRAM CARD Driver (ASM version) 
Author: Andre' LaMothe, (C) 2007 Nurve Networks LLC

Update Log:

4.10.07 - Split driver into ASM only version by stripping all SPIN driver related code.
4.9.07  - Cleaned up driver more, added sub-function 16 - sum range of bytes. This is used for DSP algorithms.
3.29.07 - Driver asm/spin versions complete, cleaning up documenting, testing.

Description: This is the ASM version of the driver. The other drivers are:

HX512SRAM_UNIFIED_DRV_010.spin  - Unified ASM/SPIN based driver that has all the code for both the SPIN and ASM drivers to make things easier.
HX512SRAM_SPIN_DRV_010.spin     - SPIN based driver that runs synchronously to primary COG.

NOTE: The spin driver is VERY slow and mostly for tutorial purposes, the asm driver is literally hundreds of times faster,
but obviously harder to follow, so if speed isn't a concern you can start with the spin driver and then work to the asm driver.
Both drivers have more or less the same functions, but the spin driver functions end in "_S" and the asm driver functions end
in "_A", so they can be in the same source file since spin has no functional scoping.

}

'///////////////////////////////////////////////////////////////////////
' CONSTANTS SECTION ////////////////////////////////////////////////////
'///////////////////////////////////////////////////////////////////////

CON


  ' SRAM bus interface pin constants
  SRAM_CTRL_0 = 1 ' NET_RX_CLK       (expansion pin 10)
  SRAM_CTRL_1 = 2 ' NET_TX_DATA      (expansion pin 9)

  SRAM_STROBE = 30 ' USB_RXD (Prop TX ----> USB_RXD Host) (expansion pin 19)

  SRAM_IO_7 = 23 ' IO_7 (pin 28)
  SRAM_IO_6 = 22
  SRAM_IO_5 = 21
  SRAM_IO_4 = 20
  SRAM_IO_3 = 19
  SRAM_IO_2 = 18
  SRAM_IO_1 = 17
  SRAM_IO_0 = 16  ' IO_0 (pin 21)

    ' sram commands
  SRAM_CMD_WRITE   = %000000_00
  SRAM_CMD_READ    = %000000_01
  SRAM_CMD_LOADLO  = %000000_10
  SRAM_CMD_LOADHI  = %000000_11


'//////////////////////////////////////////////////////////////////////////////
' VARIABLES SECTION ///////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

VAR

  long  cogon, cog

  ' sram parameter passing area for ASM driver, this starting address always holds, the command, parameter ptr, and return value, in that order
  long sram_command             ' holds command to SRAM driver, also the starting address of this LONG is assumed to be the start of all parms                        
  long sram_parameter_list_ptr  ' holds pointer to parameter list to driver
  long sram_return_value        ' holds result of sub-function (if there is one)

 '//////////////////////////////////////////////////////////////////////////////
' OBJECT DECLARATION SECTION //////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////


'//////////////////////////////////////////////////////////////////////////////
' PUBLIC FUNCTIONS ////////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_Start_ASM_Driver(sram_init_program)
' this function starts the ASM SRAM driver up and sends the 4-bit initialization program code to it as well as initializes the IO pins for
' proper operation the control word or "program" instructs the SRAM controller to either post inc/dec on reads/write or neither

' Parameters: sram_init_program - this data word (lower 4-bits only) is used to program the behavior of the controller, see below
'             
'
'  4-bit format
'
'  |  3   2   |  1   0 
'  |  sr  r0  |  sw  w0             
'  pgm3............pgm0 
' 
'  sw   - sign bit for write post increment/decrement (1=add, 0=subtract).
'  w0   - 1 bit magnitude for write post increment/decrement (w1 ignored in this version).
'
'  sr   - sign bit for read post increment/decrement  (1=add, 0=subtract).
'  r0   - 1 bit magnitude for read post increment/decrement (r1 ignored in this version).
'
'
'  In most cases, its recommended that controller is initialized with both post increment on read/write
'  which is the value %0000_1111, these program bits will show up on the LEDs to the top right of the SRAM card

  ' if the driver is running kill it, however, there is no way to reset the controller, so the program loaded into the program
  ' from RESET will remain there until another reset
  SRAM_Stop_ASM_Driver

  ' set command in global shared variable
  sram_command            := sram_init_program
  ' set starting address of parameters passed to sub-functions, this is a pointer to pointer, in this case NULL since this operation
  ' has no parms
  sram_parameter_list_ptr := 0

  ' start the driver, return status, set up cog id variables  
  return ( cogon := (cog := cognew(@SRAM_Driver_Entry, @sram_command)) > 0 )

'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_Stop_ASM_Driver
' stops sram driver
'
' Parameters: none.

  if cogon~
    cogstop(cog)

'//////////////////////////////////////////////////////////////////////////////
' These functions makes up the public interface to the ASM SRAM driver, the client
' calls the functions by setting globals that are being "monitored" by driver
'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_Write64K_A(addr16, data8)
' this function writes 8-bit data to the first 64K of the SRAM
'
' Parameters: addr16 - 16-bit address to write to 
'             data8  - 8-bit data to write
  
  sram_parameter_list_ptr := @addr16
  sram_command            := _Write64K ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_WriteAuto_A(data8)
' this function writes data to the SRAM at the current address ptr, then the SRAM controller updates the ptr
' depending on its initially programmed inc/dec behavior
'
' Parameters: data8  - 8-bit data to write 
'           
  
  sram_parameter_list_ptr := @data8
  sram_command            := _WriteAuto ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_Read64K_A(addr16)
' this function reads a byte of data from the first 64K of the SRAM
'
' Parameters: addr16 - 16-bit address to read from 
  
  sram_parameter_list_ptr := @addr16
  sram_command            := _Read64K ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

  return sram_return_value

'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_ReadAuto_A
' this function reads a byte of data from the currently addressed byte in the SRAM by the address pointer
' if the SRAM controller is programmed for auto inc/dec after read then it will take place automatically and the
' address pointer will be updated by the SRAM controller
'
' Parameters: None. 
  
  sram_parameter_list_ptr := 0
  sram_command            := _ReadAuto ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

  return sram_return_value

'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_LoadAddr64K_A(addr16)
' this function sets the SRAM controllers address latch to the sent 16-bit address, clears the upper 3-bits of the address as well
'
' Parameters: addr16 - 16-bit address to set the SRAM address latch to, upper 3-bits is zero'ed 
  
  sram_parameter_list_ptr := @addr16
  sram_command            := _LoadAddr64K ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

  return sram_return_value

'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_LoadAddr512K_A(addr19)
' this function sets the SRAM controllers address latch to the sent 19-bit address, loads the lower 16-bits directly then walks/advances to the final
' 19-bit address if needs
'
' Parameters: addr19 - 19-bit address to set the SRAM address latch to 
  
  sram_parameter_list_ptr := @addr19
  sram_command            := _LoadAddr512K ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

  return sram_return_value

'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_LoadAddrLow_A(addr8)
' this function sets the SRAM controllers lower 8-bits of address latch to the sent 8-bit address
'
' Parameters: addr8 - 8-bit address to set lower 8-bits of SRAM address latch to 
  
  sram_parameter_list_ptr := @addr8
  sram_command            := _LoadAddrLow ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

  return sram_return_value

'//////////////////////////////////////////////////////////////////////////////

PUB SRAM_LoadAddrHi_A(addr8)
' this function sets the SRAM controllers upper 8-bits of the 16-bit address latch to the sent 8-bit address, the upper 3-bit address
' which is not addressable directly is reset to 000 during this operation
'
' Parameters: addr8 - 8-bit address to set upper 8-bits (15..8) of SRAM address latch to 
  
  sram_parameter_list_ptr := @addr8
  sram_command            := _LoadAddrHi ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

  return sram_return_value

' /////////////////////////////////////////////////////////////////////////////

PUB SRAM_MemSet_A(addr19, data8, num_bytes)
' this function sets a contiguous block of SRAM to a byte value anywhere in the 512K and of any length 
'
' Parameters: addr19    - 19-bit address to start memory set at 
'             data8     - 8-bit data to write
'             num_bytes - number of bytes to write
  
  sram_parameter_list_ptr := @addr19
  sram_command            := _MemSet ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

' /////////////////////////////////////////////////////////////////////////////

PUB SRAM_MemSum_A(addr19, num_bytes)
' this function sums a contiguous block of SRAM and returns the 32-bit result 
'
' Parameters: addr19    - 19-bit address to start memory sum at 
'             num_bytes - number of bytes to sum
  
  sram_parameter_list_ptr := @addr19
  sram_command            := _MemSum ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

  return sram_return_value
  
' /////////////////////////////////////////////////////////////////////////////

PUB SRAM_MemCopy_A( dest_addr19, src_addr19,  num_bytes) 
' this function copies a number of bytes from one address in the SRAM to another (non-overlapping)
' NOTE: this function uses a "cache" to speed the operation, the cache is located in COG ram, and thus has size limits due
' to the code space, currently the cache is located at "sram_cache" and has a size of SRAM_CACHE_PAGE_SIZE 
'
' Parameters: dest_addr19 - 19-bit destination address in SRAM  
'             src_addr19  - 19-bit source address in SRAM
'             num_bytes   - number of bytes to copy
  
  sram_parameter_list_ptr := @dest_addr19
  sram_command            := _MemCopy ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

' /////////////////////////////////////////////////////////////////////////////

PUB MM_Copyto_SRAM_A( dest_addr19, src_addr16,  num_bytes) 
' this function copies bytes anywhere in the propellers 64K main memory into the SRAMs 512K memory
'
' Parameters: dest_addr19 - 19-bit destination address in SRAM  
'             src_addr16  - 16-bit source address in propeller main memory
'             num_bytes   - number of bytes to copy
  
  sram_parameter_list_ptr := @dest_addr19
  sram_command            := _MM_Copyto_SRAM ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

' /////////////////////////////////////////////////////////////////////////////

PUB SRAM_Copyto_MM_A( dest_addr16, src_addr19,  num_bytes) 
' this function copies bytes from the 512K SRAM to anywhere in the propellers 64K main memory
'
' Parameters: dest_addr16 - 16-bit destination address in propeller main memory  
'             src_addr19  - 19-bit source address in SRAM 
'             num_bytes   - number of bytes to copy
  
  sram_parameter_list_ptr := @dest_addr16
  sram_command            := _SRAM_Copyto_MM ' always set command last, so command doesn't start before parameter addresses are in 

  repeat while sram_command

'//////////////////////////////////////////////////////////////////////////////

CON

SRAM_DBUS_BIT_SHIFT     = 16
SRAM_CTRL_BIT_SHIFT     = 1
SRAM_STROBE_BIT_SHIFT   = 30

' commands for controller, pre-shifted to left 1-bit, so we don't have to do it during runtime, small enough to fit in constants
SRAM_CMD_WRITE_SHIFTED   = %00000_00_0
SRAM_CMD_READ_SHIFTED    = %00000_01_0
SRAM_CMD_LOADLO_SHIFTED  = %00000_10_0
SRAM_CMD_LOADHI_SHIFTED  = %00000_11_0

' SRAM controller commands (functions)
_Wait           = 0 ' do nothing command

_Write64K       = 1 ' write byte to lower 64K fast mode
_Read64K        = 2 ' read byte from lower 64K fast mode

_Write512K      = 3 ' write byte anywhere in 512K memory, slower (not implemented)
_Read512K       = 4 ' read byte from anywhere in memory, slower  (not implemented)

_WriteAuto      = 5 ' writes to the current address sram controller is set to, then auto inc/dec executes if programmed
_ReadAuto       = 6 ' writes to the current address sram controller is set to, then auto inc/dec executes if programmed

_LoadAddr64K    = 7 ' loads a 16-bit address (0..64K-1) directly into the low and high address latches, clears the upper 3-bits of address
_LoadAddr512K   = 8 ' loads a 19-bit address (0..512K-1) into address buffer, by advancing if necessary using dummy reads

_LoadAddrLow    = 9 ' loads only the lower 8-bits of address into address buffer
_LoadAddrHi     = 10 ' load only the uppper 8-bits of address into address buffer, also clears upper 3-bits, good to select 256 bytes "pages"

_MemSet         = 11 ' fills memory anywhere in the 512K region with a byte value
_MemCopy        = 12 ' copies a number of bytes in the SRAM from source to destination, doesn't support overlapping copies

_MM_Copyto_SRAM = 13 ' copies bytes from the Propeller's main memory to the SRAM's 512K space
_SRAM_Copyto_MM = 14 ' copies bytes from the SRAMs 512K to the Propeller's main memory

_ReadAddr       = 15 ' returns the current value of the 19-bit address buffer in the SRAM controller (not implemented)  

_MemSum         = 16 ' sum a region of memory and returns the 32-bit result, helps with diagnostics and DSP stuff

' SRAM cache constants
SRAM_CACHE_PAGE_SIZE = 192 ' number of bytes in local COG memory cache page

'//////////////////////////////////////////////////////////////////////////////

DAT
              org $000                                  ' set the code emission for COG at $000

SRAM_Driver_Entry
              ' this is the entry point for the ASM SRAM driver, the driver is meant as an example to be used from other
              ' programs, but is by no means the most optimized it could be. moreover, to get optimal performance from the sram you
              ' must blend the sram access code right inline with your COG code since the difference between maximum speed is a few instructions
              ' any overhead can slow the system down considerable. the sram can operation faster than the prop can push it, so all bottlenecks
              ' are in the prop access in most cases. the sequence of steps to access the sram are basically bit banging the control lines and
              ' writing and reading the 8-bit bus in parallel
              
              ' the driver is commanded by means of a global shared memory region where the caller/client passes commands into, and the
              ' driver is "listening" for a new command, when a command is detected, the its executed and the driver resets the global command
              ' inidicating that the command is complete, this way the client doens't try to send commands until the current command is processed

              ' additionally the communication parameter passing area consists of 3 variables that must be declared by the client in the following order
              ' and format:
              '
              ' sram parameter passing area, this starting address always holds, the command, parameter ptr, and return value, in that order
              '
              ' long sram_command             ' holds command to SRAM driver, also the starting address of this LONG is assumed to be the start of all parms                        
              ' long sram_parameter_list_ptr  ' holds pointer to parameter list to driver
              ' long sram_return_value        ' holds result of sub-function (if there is one)

              ' so the client on start up passes the addressed of @sram_command from his globals, and the driver records this, then the client
              ' must place the command into sram_command, and set sram_parameter_list_ptr to point to the parameters for the function in question,
              ' in many cases, this might be the first parm on the stack or some other location, by using this extra layer of indirection the SRAM driver
              ' has the most flexibility
              ' finally, if there are any results or return valuse they will show up in sram_return_value 

              ' the driver also makes use of a COG memory cache to speed up SRAM <-> SRAM copies, performance degrades considerably when the source
              ' and target addresses are over the 64K directly addressable region of the SRAM, thus by at least caching blocks we can minimize how
              ' many seeks need to be made, the cache is located in the DAT section at the end of the program, make it whatever you wish that will fit:
              ' sram_cache - cache
              ' its size must be set in BYTES in this variable located in the CON section:
              ' SRAM_CACHE_PAGE_SIZE = 192
              '
              ' which leave about 40 longs left for more code space!! So if you want to increase the cache size you will have to comment out some of the
              ' functions 
              
              mov sram_parms_base_ptr, par              ' copy boot parameter into sram_parms_base_ptr
              rdlong sram_cmd, sram_parms_base_ptr      ' read the SRAM initialization command from client, store in cmd
                                                        ' this is only done the 1st time, after this the main command waiting loop is entered
              mov sram_cmd_parms_ptr_ptr, par
              add sram_cmd_parms_ptr_ptr, #4            ' set pointer to pointer where parms are, this ptr must be dereferenced each function call

              mov sram_result_ptr, par
              add sram_result_ptr, #8                   ' store pointer to return variable global that driver uses           

              ' set the IO direction and states for SRAM interface
              mov outa, SRAM_CTRL_MASK                  ' write 1's to interface, control lines only, so we don't accidentally fire a program clock

              ' one by one set pin groups to output
              or dira, SRAM_DBUS_CTRL_STROBE_MASK       ' set I/Os for sram interface all to outputs for now

              and outa, nSRAM_CTRL_MASK                 ' set control lines to code "00" which means next clock strobe read program                        


              ' initialize the memory controller, need to put the command on the data bus, and pulse strobe
              and outa, nSRAM_DBUS_MASK                 ' outa = (outa & !sram_dbus_mask), make hole for data

              mov r1, sram_cmd                          ' r1 = sram_cmd, which during startup is the program code for sram controller
              shl r1, #SRAM_DBUS_BIT_SHIFT              ' r1 = sram_cmd < 16, place data into proper position
              or outa, r1                               ' finally, outa = (outa & !sram_dbus_mask) | sram_cmd

              ' now pulse the strobe line
              or outa, SRAM_STROBE_MASK                 ' strobe = 1
              and outa, nSRAM_STROBE_MASK               ' strobe = 0

              ' now that we are done, set DBUS to inputs, leave control to outputs.
              mov outa, #0
              and dira, nSRAM_DBUS_MASK

              ' at this point, we have the following status
              ' MM[ sram_cmd ] -> current command from client
              ' MM [sram_cmd_parms_ptr, sram_cmd_parms_ptr+1, sram_cmd_parms_ptr+2,...,sram_cmd_parms_ptr+n ] -> sram parameters in MM 

              ' write 0 out to sram command to signify first command was processed
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

'//////////////////////////////////////////////////////////////////////////////
' MAIN COMMAND WAITING LOOP
'//////////////////////////////////////////////////////////////////////////////

SRAM_Cmd_Wait_Loop
             ' enter into command loop waiting for command 
              rdlong sram_cmd, sram_parms_base_ptr      wz                      ' read command from MM in global shared variable
        if_z  jmp #SRAM_Cmd_Wait_Loop                                           ' if non-zero then execute command, else continue to loop                             

              ' retreive latest pointer to parameters
              rdlong sram_cmd_parms_ptr, sram_cmd_parms_ptr_ptr ' sram_cmd_parms_ptr -> parameter list starting address for 0...(n-1) parameters

              ' ok now we basically need to do case (sram_cmd) and for each value execute the code body
              mov r0, #SRAM_Jump_Table          ' r0 = base address of jump table
              add r0, sram_cmd                  ' r0 = r0 + cmd
              movs :Read_Jumpvec, r0            ' access vector address in jump table at [r0 + cmd] -> destination of jmp (self modify code)
              nop       ' wait a second for pre-fetch, let self modifying code complete downstream       

:Read_Jumpvec mov r1, 0 ' dummy 0 value has been overwritten with jump vector above              
              jmp r1    ' jump to sub-function starting address

' this is an inline jump table, more or less implements an assembly language "case" statement
SRAM_Jump_Table  ' to save memory convert to words or bytes later, but means more code above to perform select logic
                 ' table holds starting address of each sub-function
                 
              long Wait_           '= 0 , do nothing command (DONE)

              long Write64K_       '= 1 , write byte to lower 64K fast mode (DONE)
              long Read64K_        '= 2 , read byte from lower 64K fast mode (DONE)

              long Write512K_      '= 3 , write byte anywhere in 512K memory, slower (not implemented), instead load the address with LoadAddr512K_ then use ReadAuto/WriteAuto 
              long Read512K_       '= 4 , read byte from anywhere in memory, slower  (not implemented)

              long WriteAuto_      '= 5 , writes to the current address sram controller is set to, then auto inc/dec executes if programmed (DONE)
              long ReadAuto_       '= 6 , writes to the current address sram controller is set to, then auto inc/dec executes if programmed (DONE)

              long LoadAddr64K_    '= 7 , loads a 16-bit address (0..64K-1) directly into the low and high address latches, also clears the upper 3-bits of address (DONE)
              long LoadAddr512K_   '= 8 , loads a 19-bit address (0..512K-1) into address buffer, by advancing if necessary using dummy reads (DONE)

              long LoadAddrLow_    '= 9 , loads only the lower 8-bits of address into address buffer (DONE)
              long LoadAddrHi_     '= 10 , load only the uppper 8-bits of address into address buffer, also clears upper 3-bits, good to select 256 bytes "pages" (DONE)

              long MemSet_         '= 11 , fills memory anywhere in the 512K region with a byte value (DONE)
              long MemCopy_        '= 12 , copies a number of bytes in the SRAM from source to destination, doesn't support overlapping copies (DONE)

              long MM_Copyto_SRAM_ '= 13 , copies bytes from the Propeller's main memory to the SRAM's 512K space (DONE)
              long SRAM_Copyto_MM_ '= 14 , copies bytes from the SRAMs 512K to the Propeller's main memory (DONE)

              long ReadAddr_       '= 15 , returns the current value of the 19-bit address buffer in the SRAM controller (not implemented)  

              long MemSum_         ' = 16 ' sum a region of memory and returns the 32-bit result, helps with diagnostics and DSP stuff

'//////////////////////////////////////////////////////////////////////////////
' COMMAND SUB-FUNCTION IMPLEMENTATIONS
'//////////////////////////////////////////////////////////////////////////////
Wait_         ' = 0 ' do nothing command, should never get here

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
Write64K_     ' = 1 ' write byte to lower 64K fast mode. Eg. Write64K(address16, data8)
              ' this sub-function writes a byte to the lower 64K of memory, both the low and high address latches are written to with the sent 64K
              ' address, then the data byte is written.
              ' parameters: two longs, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): address to write, 16-bits
              ' parm 1 (32-bit): data to write, 8-bits 

              ' retrieve long holding 16-bit address
              rdlong sram_parm0, sram_cmd_parms_ptr
              mov r0, sram_cmd_parms_ptr
              add r0, #4
              
              ' retrieve long holding 8-bit data
              rdlong sram_parm1, r0                        

              ' call set address routing, exprext sram_parm0 = 16-bit address
              mov r7, sram_parm0
              call #SetAddr64K_Proc

              ' place 8-bit data on data bus -----------------------------------------------
              mov r0, sram_parm1
              and r0, #$FF                      ' mask lower 8-bits (precaution)
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for write memory
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_WRITE_SHIFTED   ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_WRITE_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK                 ' strobe = 1
              and outa, nSRAM_STROBE_MASK               ' strobe = 0

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
              
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
Read64K_      ' = 2 ' read byte from lower 64K fast mode, Eg. Read64K(address16)
              ' this sub-function reades a byte from the lower 64K of memory, both the low and high address latches are written to with the sent 64K
              ' address, then the data byte is retrieved and stored in sram_result_ptr
              ' parameters: one long, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): address to read from, 16-bits
 
              ' retrieve long holding 16-bit address
              rdlong sram_parm0, sram_cmd_parms_ptr

              ' call set address routing, expect sram_parm0 = 16-bit address
              mov r7, sram_parm0
              call #SetAddr64K_Proc

              ' place data bus into read mode and retrieve 8-bit data ---------------------
              and dira, nSRAM_DBUS_MASK
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for read memory
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_READ_SHIFTED   ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_READ_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK                 ' strobe = 1

              ' data is now on bus, retrieve it...
              mov r0, ina                       ' pull data from external pins
              shr r0, #SRAM_DBUS_BIT_SHIFT      ' shift the data 16 time to the right [23..16] is location of data pins 
              and r0, #$FF                      ' mask the data to 8-bits

              ' write data back out to global client parameter passing area
              wrlong r0, sram_result_ptr 

              ' finally finish the clocking of the read
              and outa, nSRAM_STROBE_MASK               ' strobe = 0

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
              
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
Write512K_    ' = 3 ' write byte anywhere in 512K memory, slower

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done
 
'//////////////////////////////////////////////////////////////////////////////
Read512K_     ' = 4 ' read byte from anywhere in memory, slower

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
WriteAuto_    ' = 5 ' writes to the current address sram controller is set to, then auto inc/dec executes if programmed
              ' this sub-function writes a byte to the currently addressed memory location in the 512K memory
              ' parameters: one longs, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): data to write, 8-bits 

              ' retrieve long holding 8-bit data
              rdlong sram_parm0, sram_cmd_parms_ptr
               
              ' now place data bus into output mode
              or dira, SRAM_DBUS_MASK

              ' place 8-bit data on data bus -----------------------------------------------
              mov r0, sram_parm0
              and r0, #$FF                      ' mask lower 8-bits (precaution)
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for write memory
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_WRITE_SHIFTED  ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_WRITE_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK         ' strobe = 1
              and outa, nSRAM_STROBE_MASK       ' strobe = 0

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
              
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
ReadAuto_    ' = 6 ' reads the current byte addressed by the sram controller, then auto inc/dec executes if programmed
             ' this sub-function reads a byte from the currently addressed memory location in the 512K memory
             ' parameters: none 

             ' place data bus into read mode and retrieve 8-bit data ---------------------
              and dira, nSRAM_DBUS_MASK
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for read memory
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_READ_SHIFTED   ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_READ_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK                 ' strobe = 1

              ' data is now on bus, retrieve it...
              mov r0, ina                       ' pull data from external pins
              shr r0, #SRAM_DBUS_BIT_SHIFT      ' shift the data 16 time to the right [23..16] is location of data pins 
              and r0, #$FF                      ' mask the data to 8-bits

              ' write data back out to global client parameter passing area
              wrlong r0, sram_result_ptr 

              ' finally finish the clocking of the read
              and outa, nSRAM_STROBE_MASK               ' strobe = 0

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
              
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done
 
 '//////////////////////////////////////////////////////////////////////////////
LoadAddr64K_  ' = 7 ' loads a 16-bit address (0..64K-1) directly into the low and high address latches, clears the upper 3-bits of address

              ' this sub-function sets the SRAMs' 16-bit latch, low and high address latches are written to with the sent 64K
              ' parameters: one long, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): address to set latches to (lower 16-bit used)

               ' retrieve long holding 16-bit address
              rdlong sram_parm0, sram_cmd_parms_ptr

              ' call set address routing, exprext sram_parm0 = 16-bit address
              mov r7, sram_parm0
              call #SetAddr64K_Proc

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
               
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
LoadAddr512K_ ' = 8 ' loads a 19-bit address (0..512K-1) into address buffer, by advancing if necessary using dummy reads

              ' this sub-function simple sets the addressing latch to the sent location in the 512K memory
              ' after which a readauto or writeauto would normally be performed
              ' if the address is <= 64K then the address is directly latched into the 16-bit address latc
              ' if the address is > 64K the $FFFF is latched into the address latch, then the memory controller is "walked" with dummy reads
              ' until its to the write location
              ' NOTE: this function only works with SRAM controller pre-programmed with post increment on reads.
              ' parameters: two longs, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): address to write, 19-bits used

              ' retrieve long holding 19-bit address, store in sram_parm0
              rdlong sram_parm0, sram_cmd_parms_ptr
              mov r0, sram_cmd_parms_ptr             ' advance pointer to next parameters which holds data
              add r0, #4
              
             ' retrieve long holding 8-bit data store in sram_parm1
              rdlong sram_parm1, r0

              mov r7, sram_parm0
              call #SetAddr512K_Proc

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
              
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
LoadAddrLow_  ' = 9 ' loads only the lower 8-bits of address into address buffer

              ' this sub-function sets the SRAMs' lower 8 bits of 16-bit address latch, more or less updating the 0-255 address, but leaving the upper 8-bits
              ' of the latch as well as the internal upper 3-bits which are not accessible unless under controller control
              ' parameters: one long, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): address to set latches to (lower 8-bit used)

               ' retrieve long holding low 8-bits of 16-bit address
              rdlong sram_parm0, sram_cmd_parms_ptr
               
              ' now place data bus into output mode
              or dira, SRAM_DBUS_MASK
 
              ' place lower 8-bits of address on data bus -----------------------
              mov r0, sram_parm0
              and r0, #$FF                      ' mask lower 8-bits
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for load low address
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_LOADLO_SHIFTED ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_LOADLO_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK         ' strobe = 1
              and outa, nSRAM_STROBE_MASK       ' strobe = 0

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK

              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
LoadAddrHi_   ' = 10 ' load only the uppper 8-bits of address into address buffer, also clears upper 3-bits, good to select 256 bytes "pages"

              ' this sub-function sets the SRAMs' upper 8 bits of 16-bit address latch (19-total bits, 16 addressable)
              ' more or less updating the 0-255 page address, but leaving the lower 8-bits
              ' of the latch alone. Also,the internal upper 3-bits which are not accessible unless under controller control are reset to 000
              ' parameters: one long, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): address to set latches to (upper 8-bit used)

               ' retrieve long holding upper 8-bits of 16-bit address
              rdlong sram_parm0, sram_cmd_parms_ptr
               
              ' now place data bus into output mode
              or dira, SRAM_DBUS_MASK
 
              ' place upper 8-bits of 16-bit address onto data bus ------------------------
              mov r0, sram_parm0
              shr r0, #8                        ' move upper 8-bits into lower 8-bits
              and r0, #$FF                      ' mask lower 8-bits (precaution)
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for load high address
              and outa, nSRAM_CTRL_MASK          ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_LOADHI_SHIFTED  ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_LOADHI_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK                 ' strobe = 1
              and outa, nSRAM_STROBE_MASK               ' strobe = 0

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
               
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
MemSet_       ' = 11 ' fills memory anywhere in the 512K region with a byte value
              ' parameters: three longs, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): destination address, 19-bits used
              ' parm 1 (32-bit): data to write, 8-bits used
              ' parm 2 (32-bit): number of bytes to fill/set  32-bit (only makes sense to move 512K at a time.

              ' retrieve long holding 19-bit address, store in sram_parm0
              rdlong sram_parm0, sram_cmd_parms_ptr
              mov r0, sram_cmd_parms_ptr             ' advance pointer to next parameters which holds data
              add r0, #4

             ' retrieve long holding 8-bit data store in sram_parm1
              rdlong sram_parm1, r0
              add r0, #4              

              ' retrieve long holding number of bytes (32-bit value)
              rdlong sram_parm2, r0

              ' advance memory pointer to starting address
              mov r7, sram_parm0
              call #SetAddr512K_Proc

              ' now place data bus into output mode
              or dira, SRAM_DBUS_MASK

              ' place 8-bit data on data bus -----------------------------------------------
              mov r0, sram_parm1
              and r0, #$FF                      ' mask lower 8-bits (precaution)
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for write memory
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_WRITE_SHIFTED  ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_WRITE_SHIFTED)                                          

              ' now we are ready to fill/set the memory, simply toggle the clock line (assumes auto increment on write)
:AddrAdvance
              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK                 ' strobe = 1
              and outa, nSRAM_STROBE_MASK               ' strobe = 0
              djnz sram_parm2, #:AddrAdvance            ' repeat while sram_parm2 (num_bytes) > 0

:AddrAdvanceEnd

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
               
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                                                          


              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
MemCopy_      ' = 12 ' copies a number of bytes in the SRAM from source to destination, doesn't support overlapping copies, will do it, but results
              ' won't be as expected.
              ' NOTE: Function operates by reading blocks of memory at a time and moving it, the blocks are stored locallly in a "sram cache", this cache
              ' can be any size, suggested 64-256 bytes for any kind of performance 
              ' parameters: three longs, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): destination address, 19-bits used
              ' parm 1 (32-bit): source address, 19-bits used
              ' parm 2 (32-bit): number of bytes to copy 32-bit (only makes sense to move 512K at a time.

              ' first compute number of pages and bytes that need copying
              ' copy pages, one at a time from SRAM to cache back to SRAM in cache size blocks 64-256 bytes at a time
              ' then copy remaining bytes

              ' READ PARAMETERS FROM CALLER ---------------------------------------------------------------------------
              rdlong sram_parm0, sram_cmd_parms_ptr  ' sram_parm0 hold destination address 19-bit   
              mov r0, sram_cmd_parms_ptr             ' advance pointer to next parameters which holds data
              add r0, #4

             ' retrieve long holding 19-bit source address store in sram_parm1
              rdlong sram_parm1, r0
              add r0, #4              

              ' retrieve long holding number of bytes (32-bit value) to copy
              rdlong sram_parm2, r0

               ' parameters now retrieved, at this point we have
              ' sram_parm0 = dest_addr
              ' sram_parm1 = src_addr
              ' sram_parm2 = num_bytes_to_copy

              ' MAIN MEMCPY LOOP ---------------------------------------------------------------------------------------

              ' we need to copy a number of bytes from SRAM to SRAM, too slow to copy if copying splits between 64K mark, thus
              ' use internal COG memory as a cache and copy "pages" from 64-256 bytes at a time from SRAM -> COG Cache -> SRAM

              mov num_bytes_to_copy, sram_parm2         ' this is the total number of bytes requested to be copied from client


                         
:CopyLoop ' ------------------------------------------------------------------------------------------------------------- LOOP
              cmp num_bytes_to_copy, #SRAM_CACHE_PAGE_SIZE    wc, wz      ' copy one page at a time, whatever memory permits 
        if_ae jmp #:CopyMorePages               ' if num_bytes_to_copy >= SRAM_CACHE_PAGE_SIZE then.. 
              'else num_bytes_to_copy < SRAM_CACHE_PAGE_SIZE then..

              mov num_copy_bytes, num_bytes_to_copy     ' set number of bytes to copy this pass
              mov num_bytes_to_copy, #0                 ' and we are done next time around
              
              jmp #:SetSrcAddr
              ' end else

:CopyMorePages ' if num_bytes_to_copy >= SRAM_CACHE_PAGE_SIZE then..
              mov num_copy_bytes, #SRAM_CACHE_PAGE_SIZE       ' lets copy the maximum page size this pass
              sub num_bytes_to_copy, #SRAM_CACHE_PAGE_SIZE    ' and adjust the bytes left to copy next pass, when num_bytes_to_copy == 0, we are done!
              ' end if



              ' COPY NEXT SRAM PAGE (OR LESS) INTO COG CACHE------------------------------------------------------------
:SetSrcAddr
              ' starting address of local cog SRAM cache
              mov sram_cache_entry_ptr, #sram_cache        

              ' set source address in memory latch for reads
              mov r7, sram_parm1                ' r7 = source address
              call #SetAddr512K_Proc
              

             ' place data bus into read mode and retrieve 8-bit data ---------------------------------------------------
              and dira, nSRAM_DBUS_MASK
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for read memory
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_READ_SHIFTED   ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_READ_SHIFTED)                                          
              
              ' outer most "page size" loop, this will either be <= SRAM_CACHE_PAGE_SIZE, we need to copy this many bytes, but we need to perform
              ' the copies in groups of 4, since the COG memory is LONG based and the SRAM is BYTE based, thus this disparity causes
              ' a second interior loop or step to read the 4 bytes out at a time, position them in a long then write the long to the cache

              
              mov curr_byte, #0                 ' current byte loop counter, need to copy a total of num_copy_bytes from SRAM to cache 

:ByteCacheReadLoop ' ---------------------------------------------------------------------------------------------------- LOOP

              ' read bytes 0,1,2,3 from SRAM sequentially and store into cache_entry which will then be written to cache
              ' (note if only 1-3 bytes need to be written then this is redundant, but mork worth to conditionally test it              
              mov cache_byte, #4                ' cache byte index in packed long, used as counter here
              mov num_shifts, #0                ' number of shifts per byte copy iteration, shifts byte read into packed position in long
              mov cache_entry, #0               ' used to hold packed LONG constructed via 4 bytes read from SRAM then this is written at once to local COG cache        

:ReadBytesIntoCacheEntryLoop ' ------------------------------------------------------------------------------------------- LOOP

              ' clock the strobe line and tell the sram controller to initiate the read and auto inc/dec
              or outa, SRAM_STROBE_MASK         ' strobe = 1

              ' data is now on bus, retrieve it...
              mov r0, ina                       ' pull data from external pins
              shr r0, #SRAM_DBUS_BIT_SHIFT      ' shift the data 16 time to the right [23..16] is location of data pins 
              and r0, #$FF                      ' mask the data to 8-bits
              shl r0, num_shifts                ' r0 = r0 << num_shifts, used to place bits into correct LONG byte position
              or cache_entry, r0                ' store byte 0 into cache entry
              add num_shifts, #8                ' num_shifts = num_shifts + 8, next byte read needs to be shifted 8 more bits

              ' finally finish the clocking of the read
              and outa, nSRAM_STROBE_MASK       ' strobe = 0

              djnz cache_byte, #:ReadBytesIntoCacheEntryLoop        ' while cache_byte > 0, loop


              ' we have the next packed LONG of bytes from the SRAM read in, now its time to store them in the cache and advance
              ' cache pointer..
              ' COGMEM[ sram_cache_entry_ptr++ ]  = cache_entry
              movd :WriteCache, sram_cache_entry_ptr    ' modify destination address, so we can write to local COG memory with packed cache entry
              add sram_cache_entry_ptr, #1              ' increment cache pointer for next iteration (also give pre-fetch time to complete modify downstream)

:WriteCache   mov 0, cache_entry                        ' self modifying code, dummy "0" destination modified above receives packed 4-byte sram data
                
 
              add curr_byte, #4                  wc, wz   ' bytes always copied 4 at a time, so at worst case an extra 3 bytes will be copied into cache
                                                          ' but has no effect on final write operation, which will always copy out EXACTLY the correct number of bytes
                                                          
              cmp curr_byte, num_copy_bytes      wc, wz
         if_b jmp #:ByteCacheReadLoop                     ' loop while current byte being copied < total number of bytes to copy


              ' WRITE CACHED COG PAGE BACK TO SRAM --------------------------------------------------------------------

              ' at this point we have a cache page full of bytes (in long size chunks), could be a full page or less than full size
              ' if total number of bytes to copy was less than cache page size OR we are on the last copy and copying the remaining
              ' left over bytes from the last full page size copy

              ' advance address pointer to destination location in SRAM
              mov r7, sram_parm0                ' r7 = destination address
              call #SetAddr512K_Proc


              ' copy bytes from COG cache into sram now...
              ' perform what setup we can outside the loop


              ' place data bus into write mode and prepare to write cache page out to sram ---------------------
              or dira, SRAM_DBUS_MASK

              ' command lines should already be in output mode, so only need to write 2-bit command code for write memory
              and outa, nSRAM_CTRL_MASK          ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_WRITE_SHIFTED   ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_WRITE_SHIFTED)                                          
              
              ' outer most "page size" loop, this will either be <= SRAM_CACHE_PAGE_SIZE, we need to copy this many bytes, but we need to perform
              ' the copies in groups of 4, since the COG memory is LONG based and the SRAM is BYTE based, thus this disparity causes
              ' some work to have to be done to extract the packed bytes from the long and then send them to sram
                            
              mov curr_byte, #0                 ' byte loop counter, need to copy num_copy_bytes from cache to SRAM completing the memory move (a page at a time) 

:ByteCacheWriteLoop
              ' need to do this more or less
              ' SRAM [ curr_byte ] = (COG_CACHE [ curr_byte / 4 ] >> (curr_byte MOD 4) ) && $FF

              ' compute COG index in sram cache to read from (long data containing packed bytes)
              mov cache_index, curr_byte
              shr cache_index, #2               ' cache_index = curr_byte / 4

              ' compute the byte index in the long to read 
              mov cache_byte, curr_byte
              and cache_byte, #3                ' cache_byte = curr_byte mod 4

              ' at this point we know the long in the cache memory and the byte within the long we need to read
              mov r0, #sram_cache
              add r0, cache_index 
     
              movs :ReadCache, r0               ' want to read COGMEM_SRAM_CACHE [ cache_index ], modify source operand downstream
              nop                               ' put some work from downstream here to optimize, but leave for now to see what's going on 
              
:ReadCache    mov cache_entry, 0                ' cache_entry = COGMEM_SRAM_CACHE [ cache_index ], dummy "0" is overwritten with actual index by self modify code
              
              ' now we simply need to extract the proper byte from the cache entry and write it to sram

              mov num_shifts, cache_byte
              shl num_shifts, #3                ' num_shifts = cache_byte * 8

              shr cache_entry, num_shifts       ' place the requested byte into the lower 8-bits position

              ' we have everything we need, now let's write the data
              mov r0, cache_entry
              and r0, #$FF                      ' mask lower 8-bits (precaution)
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK         ' strobe = 1
              and outa, nSRAM_STROBE_MASK       ' strobe = 0


              add curr_byte, #1                         ' if (++curr_byte < num_copy_bytes) then repeat loop  
              cmp curr_byte, num_copy_bytes wc, wz
        if_b  jmp #:ByteCacheWriteLoop               


              ' done with current cache page pass, may or may not have read/written an entire page, either way update source and destination pointers
              add sram_parm0, num_copy_bytes
              add sram_parm1, num_copy_bytes

              ' END OF MAIN COPY LOOP, TEST IF MORE BYTES NEED TO BE COPIED, AND LOOP BACK ----------------------------

              ' if num_bytes_to_copy > 0 then continue copying pages, jump back up to outer most loop
              cmp num_bytes_to_copy, #0 wc ,wz
        if_a  jmp #:CopyLoop               

              
              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
               
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
MM_Copyto_SRAM_ ' = 13 ' copies bytes from the Propeller's main memory to the SRAM's 512K space
                ' NOTE: assumes that controller is in auto inc after write mode
                ' parameters: three longs, starting address: sram_cmd_parms_ptr 
                ' parm 0 (32-bit): destination address in sram, 19-bits used
                ' parm 1 (32-bit): source address in main memory, 16-bits used (propeller only has 64K address space, lower 32K RAM, upper 32K ROM)
                ' parm 2 (32-bit): number of bytes to copy 32-bit (only makes sense copy up to 64K though, since that's how big the prop memory is

              ' READ PARAMETERS FROM CALLER ---------------------------------------------------------------------------
              rdlong sram_parm0, sram_cmd_parms_ptr  ' sram_parm0 hold destination address 19-bit   
              mov r0, sram_cmd_parms_ptr             ' advance pointer to next parameters which holds data
              add r0, #4

             ' retrieve long holding 16-bit source address referring to main memory store in sram_parm1
              rdlong sram_parm1, r0                     
              add r0, #4              

              ' retrieve long holding number of bytes (32-bit value) to copy
              rdlong sram_parm2, r0


              ' parameters now retrieved, at this point we have
              ' sram_parm0 = dest_addr in SRAM
              ' sram_parm1 = src_addr in prop main memory (MM)
              ' sram_parm2 = num_bytes_to_copy to copy

              ' we want to perform the following algorithm in the abstract...
              'for (index = 0; index < num_bytes_to_copy; index++)
              '  SRAM[dest_addr + index] = MM[src_addr + index]

              ' this isn't too bad, since we are not copying sram to sram, we only have to place the sram at the destination address to write to

              ' advance SRAM address pointer to destination location in SRAM
              mov r7, sram_parm0                        ' r7 = destination address in SRAM
              call #SetAddr512K_Proc

              ' place data bus into write mode and prepare to write byte stream from main memory
              or dira, SRAM_DBUS_MASK

              ' command lines should already be in output mode, so only need to write 2-bit command code for write memory
              and outa, nSRAM_CTRL_MASK                 ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_WRITE_SHIFTED          ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_WRITE_SHIFTED)                                          

              '  ----------------------------------------------------------------------------------------------------- LOOP
              ' at loop entry, sram_parm2 holds total number of bytes requested to be copied from client
:CopytoSramLoop

              rdbyte r0, sram_parm1                     ' r0 = MM [ src_addr ]
              ' we have everything we need, now let's write the data

              and r0, #$FF                      ' mask lower 8-bits (precaution)
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (r0 << 16)                             

              ' finally clock the strobe line and tell the sram controller to complete the operation
              ' SRAM [ dest_addr ] <- r0 <- MM [ src_addr] 
              or outa, SRAM_STROBE_MASK         ' strobe = 1
              and outa, nSRAM_STROBE_MASK       ' strobe = 0
              
              ' SRAM address will auto increment, but have to increment source MM address manually
              add sram_parm1, #1

              djnz sram_parm2, #:CopytoSramLoop  ' repeat while sram_parm2 (number of bytes to copy ) > 0

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
               
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////
SRAM_Copyto_MM_ ' = 14 ' copies bytes from the SRAMs 512K to the Propeller's main memory
                ' NOTE: assumes that controller is in auto inc after write mode
                ' parameters: three longs, starting address: sram_cmd_parms_ptr 
                ' parm 0 (32-bit): source address in main memory, 16-bits used (propeller only has 64K address space, lower 32K RAM, upper 32K ROM)
                ' parm 1 (32-bit): destination address in sram, 19-bits used
                ' parm 2 (32-bit): number of bytes to copy 32-bit (only makes sense copy up to 64K though, since that's how big the prop memory is

              ' READ PARAMETERS FROM CALLER ---------------------------------------------------------------------------
              rdlong sram_parm0, sram_cmd_parms_ptr  ' sram_parm0 hold destination address in main memory 16-bit used   
              mov r0, sram_cmd_parms_ptr             ' advance pointer to next parameters which holds data
              add r0, #4

             ' retrieve long holding 19-bit source address referring to SRAM store in sram_parm1
              rdlong sram_parm1, r0                     
              add r0, #4              

              ' retrieve long holding number of bytes (32-bit value) to copy
              rdlong sram_parm2, r0


              ' parameters now retrieved, at this point we have
              ' sram_parm0 = dest_addr in main memory (MM)
              ' sram_parm1 = src_addr in SRAM
              ' sram_parm2 = num_bytes_to_copy to copy

              ' we want to perform the following algorithm in the abstract...
              'for (index = 0; index < num_bytes_to_copy; index++)
              '  MM[dest_addr + index] = SRAM[src_addr + index]

              ' this isn't too bad, since we are not copying sram to sram, we only have to place the sram at the source location to read from

              ' advance SRAM address pointer to source location in SRAM
              mov r7, sram_parm1                        ' r7 = source address in SRAM
              call #SetAddr512K_Proc

              ' place data bus into read mode and prepare to read byte stream from SRAM
              and dira, nSRAM_DBUS_MASK

              ' command lines should already be in output mode, so only need to write 2-bit command code for read memory
              and outa, nSRAM_CTRL_MASK                 ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_READ_SHIFTED          ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_READ_SHIFTED)                                          

              '  ----------------------------------------------------------------------------------------------------- LOOP
              ' at loop entry, sram_parm2 holds total number of bytes requested to be copied from client
:CopytoMainMemoryLoop

              rdbyte r0, sram_parm1                     ' r0 = MM [ src_addr ]
              ' we have everything we need, now let's write the data

              ' clock the strobe line and tell the sram controller to initiate the read and auto inc/dec
              or outa, SRAM_STROBE_MASK         ' strobe = 1

              ' data is now on bus, retrieve it...
              mov r0, ina                       ' pull data from external pins
              shr r0, #SRAM_DBUS_BIT_SHIFT      ' shift the data 16 time to the right [23..16] is location of data pins 
              and r0, #$FF                      ' mask the data to 8-bits

              ' write the data to main memory
              wrbyte r0, sram_parm0

              ' finally finish the clocking of the read
              and outa, nSRAM_STROBE_MASK       ' strobe = 0
              
              ' SRAM address will auto increment, but have to increment source MM address manually
              add sram_parm0, #1

              djnz sram_parm2, #:CopytoMainMemoryLoop  ' repeat while sram_parm2 (number of bytes to copy ) > 0

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK
               
              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                        


              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done

'//////////////////////////////////////////////////////////////////////////////              
ReadAddr_       ' = 15 ' returns the current value of the 19-bit address buffer in the SRAM controller  


              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done


'//////////////////////////////////////////////////////////////////////////////
MemSum_       ' = 16 ' sum a region of memory and returns the 32-bit result, helps with diagnostics and DSP stuff
              ' parameters: three longs, starting address: sram_cmd_parms_ptr 
              ' parm 0 (32-bit): source address to sum, 19-bits used
              ' parm 1 (32-bit): number of bytes to sum  32-bit (only makes sense to move 512K at a time.

              ' retrieve long holding 19-bit address, store in sram_parm0
              rdlong sram_parm0, sram_cmd_parms_ptr
              mov r0, sram_cmd_parms_ptr             ' advance pointer to next parameters which holds data
              add r0, #4

              ' retrieve long holding number of bytes (32-bit value)
              rdlong sram_parm1, r0

              ' advance memory pointer to starting address
              mov r7, sram_parm0
              call #SetAddr512K_Proc

              ' place data bus into read mode and prepare to read byte stream from SRAM
              and dira, nSRAM_DBUS_MASK

              ' command lines should already be in output mode, so only need to write 2-bit command code for read memory
              and outa, nSRAM_CTRL_MASK                ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_READ_SHIFTED          ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_READ_SHIFTED)                                          

              ' now we are ready to read/sum the memory, simply toggle the clock line (assumes auto increment on read)
              mov r1, #0                        ' r1 holds sum
:AddrAdvance
              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK                 ' strobe = 1

              ' data is now on bus, retrieve it...
              mov r0, ina                       ' pull data from external pins
              shr r0, #SRAM_DBUS_BIT_SHIFT      ' shift the data 16 time to the right [23..16] is location of data pins 
              and r0, #$FF                      ' mask the data to 8-bits
              add r1, r0                        ' sum += data

              ' finally finish the clocking of the read
              and outa, nSRAM_STROBE_MASK               ' strobe = 0

              djnz sram_parm1, #:AddrAdvance            ' repeat while sram_parm2 (num_bytes) > 0

:AddrAdvanceEnd

              ' write sum out to caller
              wrlong r1, sram_result_ptr 

              ' reset data bus to input before leaving
              mov outa, #0
              and dira, nSRAM_DBUS_MASK

              ' command complete reset global, so caller/client can issue another command
              mov r0, #0
              wrlong r0, sram_parms_base_ptr                                                          

              jmp #SRAM_Cmd_Wait_Loop           ' return to main command fetch loop when done


'//////////////////////////////////////////////////////////////////////////////
' END OF SRAM COMMANDS
'//////////////////////////////////////////////////////////////////////////////

'//////////////////////////////////////////////////////////////////////////////
' INTERNAL "HELPER" FUNCTIONS TO SAVE CODE SPACE
'//////////////////////////////////////////////////////////////////////////////

SetAddr64K_Proc
              ' internal sub-routine that sets the 64K lower 16-bit latch address
              ' expects r7 holding 16-bit address to advance to

              ' now place data bus into output mode
              or dira, SRAM_DBUS_MASK
 
              ' place lower 8-bits of 16-bit address onto data bus -----------------------

              and r7, #$FF                      ' mask lower 8-bits
              shl r7, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r7                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for load low address
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_LOADLO_SHIFTED ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_LOADLO_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK         ' strobe = 1
              and outa, nSRAM_STROBE_MASK       ' strobe = 0

              ' place upper 8-bits of 16-bit address onto data bus ------------------------
              mov r7, sram_parm0
              shr r7, #8                        ' move upper 8-bits into lower 8-bits
              and r7, #$FF                      ' mask lower 8-bits (precaution)
              shl r7, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r7                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for load high address
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_LOADHI_SHIFTED ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_LOADHI_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK         ' strobe = 1
              and outa, nSRAM_STROBE_MASK       ' strobe = 0

SetAddr64K_Proc_Ret ret 

'//////////////////////////////////////////////////////////////////////////////

SetAddr512K_Proc
              ' internal sub-routine that sets the 512K 19-bit address latch completely
              ' expects r7 holding 19-bit address to advance to
              ' side effects destroys, r0, r6, r7

              ' compare desired target address to $FFFF, if less than simply latch address and write data, else
              ' write $FFFF and then advance to final location with dummy reads
              mov r6, r7                       ' make copy of address in r6

              cmp r7, MAX_SHORT          wz, wc 
       if_be  jmp #:LoadAddr                   ' if addr <= $FFFF then load it into 16-bit latch, jump to latch code
                                               
              mov r7, MAX_SHORT                ' else latch $FFFF then advance to write location in SRAM using post increment on read


:LoadAddr    ' we are at the target address either by a short 16-bit direct latch or by advancing to the location via dummy reads...
             ' either way, we can now write the data as usual
             ' now place data bus into output mode

'//////////////////////////////////////////////////////////////////////////////////////////////////////
' EXCISE this code later and merge into load address generic call, this is just a little faster ///////
'//////////////////////////////////////////////////////////////////////////////////////////////////////

              or dira, SRAM_DBUS_MASK
 
              ' place lower 8-bits of 16-bit address onto data bus -----------------------
              mov r0, r7
              and r0, #$FF                      ' mask lower 8-bits
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for load low address
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_LOADLO_SHIFTED ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_LOADLO_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK         ' strobe = 1
              and outa, nSRAM_STROBE_MASK       ' strobe = 0

              ' place upper 8-bits of 16-bit address onto data bus ------------------------
              mov r0, r7
              shr r0, #8                        ' move upper 8-bits into lower 8-bits
              and r0, #$FF                      ' mask lower 8-bits (precaution)
              shl r0, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r0                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for load high address
              and outa, nSRAM_CTRL_MASK          ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_LOADHI_SHIFTED  ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_LOADHI_SHIFTED)                                          

              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK                 ' strobe = 1
              and outa, nSRAM_STROBE_MASK               ' strobe = 0

'//////////////////////////////////////////////////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////////////////////////////

              ' now advance memory, set up read address in 512K ----------------------------

              ' advance the address pointer by using the post increment behavior (if needed)                            
              sub r6, r7 wz, wc                         ' compute difference between addr19 and latched address 
        if_z  jmp #:AddrAdvanceEnd                      ' if (addr19 - $FFFF) > 0 then perform advance, else no advance needed, jump over code              

              ' place data bus into read mode for dummy read, data is ignored
              and dira, nSRAM_DBUS_MASK
              
              ' command lines should already be in output mode, so only need to write 2-bit command code for read memory
              and outa, nSRAM_CTRL_MASK         ' clear control lines to "00", make hole for command
              or outa, #SRAM_CMD_READ_SHIFTED   ' outa = (outa & nSRAM_CTRL_MASK) | (SRAM_CMD_READ_SHIFTED)                                          

              ' advance address pointer (addr19 - $FFFF) times, Eg. ($10000 - $FFFF) = 1, one clock then exit

:AddrAdvance
              ' finally clock the strobe line and tell the sram controller to complete the operation
              or outa, SRAM_STROBE_MASK                 ' strobe = 1
              and outa, nSRAM_STROBE_MASK               ' strobe = 0
              djnz r6, #:AddrAdvance                    ' repeat while sram_parm0 (difference from target and latched)  > 0

:AddrAdvanceEnd

SetAddr512K_Proc_Ret ret

'//////////////////////////////////////////////////////////////////////////////////////////////////////

DAT

' general purpose registers
r0                          long      $0                             
r1                          long      $0
r2                          long      $0
r3                          long      $0
r4                          long      $0
r5                          long      $0
r6                          long      $0
r7                          long      $0

' 32-bit constants, masks, anything that is greater than 9-bits and can't be represented as an immediate
SRAM_CTRL_MASK              long      %0000_0000_0000_0000_0000_0000_0000_0110
SRAM_DBUS_MASK              long      %0000_0000_1111_1111_0000_0000_0000_0000 
SRAM_STROBE_MASK            long      %0100_0000_0000_0000_0000_0000_0000_0000
SRAM_DBUS_CTRL_STROBE_MASK  long      %0100_0000_1111_1111_0000_0000_0000_0110

nSRAM_CTRL_MASK             long      %1111_1111_1111_1111_1111_1111_1111_1001
nSRAM_DBUS_MASK             long      %1111_1111_0000_0000_1111_1111_1111_1111 
nSRAM_STROBE_MASK           long      %1011_1111_1111_1111_1111_1111_1111_1111
nSRAM_DBUS_CTRL_STROBE_MASK long      %1011_1111_0000_0000_1111_1111_1111_1001

' used for debugging
DEBUG_LED_MASK              long      %0000_0000_0000_0000_0000_0000_0000_0001
nDEBUG_LED_MASK             long      %1111_1111_1111_1111_1111_1111_1111_1110

' math constants 
MAX_INT                     long      $FFFFFFFF               ' largest integer also -1 in 2's complement
MAX_SHORT                   long      $0000FFFF
ZERO                        long      $00000000

' sram interface variables and working variables
sram_parms_base_ptr         long      $0 ' pointer to main memory where the sram interface parameter passing area is
                                         ' 0 - sram command
                                         ' 1 - pointer to sram parameters from caller

sram_cmd                    long      $0 ' the requested sram controller command                                
sram_cmd_parms_ptr          long      $0 ' pointer to sram parameters  
sram_cmd_parms_ptr_ptr      long      $0 ' pointer to pointer pointing at sram parameters
sram_result_ptr             long      $0 ' pointer to global used to hold result from driver

' local storage for all the sram parameters needed for function call
sram_parm0                  long      $0
sram_parm1                  long      $0
sram_parm2                  long      $0
sram_parm3                  long      $0

' this is the cache storage for sram to sram memory copy/moves, we need a temporary buffer to move the data (64-256 bytes is a good choice)
' resize depending on what code you include, can use RES to save typing, but used data statements to be able to initialize cache for different reasons..
' if you need more cache size you can comment out functional chunks of the ASM driver code that you aren't using
sram_cache                  long 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ' 64 bytes per line of storage
                            long 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                                                    
' cache algorithm working vars
num_bytes_to_copy           long 0 ' total number of bytes to copy
num_copy_bytes              long 0 ' number of bytes to copy this pass, page 0 to SRAM_CACHE_PAGE_SIZE
curr_byte                   long 0 ' current byte being processed
num_shifts                  long 0 ' number of times to shift operand
sram_cache_entry_ptr        long 0 ' points to sram cache entry being processed 
cache_entry                 long 0 ' a data entry from the cache
cache_byte                  long 0 ' a byte in cache entry
cache_index                 long 0 ' index into the cache

' cut and paste code area...

{
              ' light blink
              or dira, DEBUG_LED_MASK
              and outa, nDEBUG_LED_MASK
              mov r0, #1
              and r0, DEBUG_LED_MASK
              or outa, r0
}

              
{
' //////////// DEBUG /////////////////////////////////////
              ' now place data bus into output mode
              or dira, SRAM_DBUS_MASK

              ' place 8-bit data on data bus -----------------------------------------------
              mov r7, sram_cmd
              and r7, #$FF                      ' mask lower 8-bits (precaution)
              shl r7, #SRAM_DBUS_BIT_SHIFT      ' shift data into position

              and outa, nSRAM_DBUS_MASK         ' outa = (outa & !sram_dbus_mask), make hole for data
              or  outa, r7                      ' outa = (outa & !sram_dbus_mask) | (sram_parm0 << 16)                             

              or dira, DEBUG_LED_MASK
              and outa, nDEBUG_LED_MASK
              mov r7, #1
              and r7, DEBUG_LED_MASK
              or outa, r7
:iloop        jmp #:iloop              
' ////////////////////////////////////////////////////////
}
                        