{
HYDRA XTREME 512K SRAM CARD Driver (SPIN version)
Author: Andre' LaMothe, (C) 2007 Nurve Networks LLC

Update Log:

4.10.07 - Split driver into SPIN only version by stripping all ASM driver related code.
4.9.07  - Cleaned up driver more, added sub-function 16 - sum range of bytes. This is used for DSP algorithms.
3.29.07 - Driver asm/spin versions complete, cleaning up documenting, testing.

Description: This is the SPIN version of the driver. The other drivers are:

HX512SRAM_UNIFIED_DRV_010.spin  - Unified ASM/SPIN based driver that has all the code for both the SPIN and ASM drivers to make things easier.
HX512SRAM_ASM_DRV_010.spin      - ASM based driver that runs asynchronously to primary COG.

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

  ' size of spin based local memory cache in bytes used for sram copying etc. to speed up process
  LOCAL_MEM_CACHE_SIZE = 256

'//////////////////////////////////////////////////////////////////////////////
' VARIABLES SECTION ///////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

VAR
  ' SRAM Spin driver working variables 
  long sram_addr
  byte sram_ctrl
  byte sram_data

 '//////////////////////////////////////////////////////////////////////////////
' OBJECT DECLARATION SECTION //////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

'//////////////////////////////////////////////////////////////////////////////
' PUBLIC FUNCTIONS ////////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

' ////////////////////////////////////////////////////////////////////
' SPIN VERSION INTERFACE FOR 512K SRAM DRIVER
' ////////////////////////////////////////////////////////////////////

PUB SRAM_InitalizeIO_S
  ' this function initializes the IO pins for proper operation with the SRAM controller
  ' as well as all the run-time variables, normally you would call this function first if you are using the unified or spin only driver
  ' Parameters: None

  ' initialize sram var, only sram_data, and sram_addr important, others for testing purposes
  sram_data      := $00
  sram_addr      := $00

  ' set SRAM bus I/O directions for bus and controle
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := $00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00            ' $FF ouput, $00 input

  ' set control bits
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_11
  DIRA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := $03            ' set to outputs 

  ' set strobe
  OUTA[ SRAM_STROBE ]              := %0000000_0
  DIRA[ SRAM_STROBE ]              := $01            ' set to outputs                 

  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00

' ////////////////////////////////////////////////////////////////////

PUB SRAM_WriteControl_S( _data8 )     
' this function writes the initial control word to the controller, the control word or "program"
' instructs the SRAM controller to either post inc/dec on reads/write or neither. Call this function if and only if you are using
' the spin only driver or unified driver and you do NOT want ASM support, the point is, only one driver can "program" the memory
' controller at start up. The the lower 4-bits of the sent data are encoded as follows:
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
'  Parmeters: _data8 - the byte data to write (lower 4-bits used only)
 
  ' set global address
  sram_addr := 0
  sram_data := _data8

  ' set bus to write 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $FF ' $FF ouput, $00 input

  ' output control byte
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := sram_data
    
  ' set control bits for load low memory address, doesn't matter what operation really
  DIRA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := $03            ' set to outputs
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
 
  ' now strobe sram clk line
  DIRA[ SRAM_STROBE ]              := $01            ' set to outputs
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_data)

' ////////////////////////////////////////////////////////////////////

PUB SRAM_MemSet_S( _dest_addr, _data8, _num_bytes)      | _index
' this function sets a contiguous block of SRAM to a byte value anywhere in the 512K and of any length 
'
' Parameters: _dest_addr - 16-bit address to start memory set at 
'             _data8     - 8-bit data to write
'             _num_bytes - number of bytes to write
' NOTE: assumes increment mode is post increment for both read and write

  ' set destination address in SRAM controller
  ' if destination < 64K then directly load the address into latch, else  set latch to nearest neighbor
  ' and advance via dummy reads

  ' test for null set  
  if ( _num_bytes == 0 )
    return( _num_bytes)

  ' set final data and address
  sram_data      := _data8
  sram_addr      := _dest_addr + _num_bytes

  if ( _dest_addr =< $FFFF )
    ' set starting address
    SRAM_LoadAddr64K_S( _dest_addr )
  else
    ' need to walk out to starting address, we know that starting address is greater than 64K, so start there
    SRAM_LoadAddr64K_S( $FFFF )    
    ' now walk the rest of the way with dummy reads...
    repeat _index from 0 to (_dest_addr - $FFFF) - 1    
      SRAM_ReadAuto_S
     
  ' now fill memory
  repeat _index from 0 to _num_bytes-1
    SRAM_WriteAuto_S( _data8 )  

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input
   
  return ( _num_bytes )

' ////////////////////////////////////////////////////////////////////

PUB SRAM_MemCopy_S( _dest_addr, _src_addr,  _num_bytes)      | _index, _bytes_to_copy
' this function copies _num_bytes bytes from _src_addr to _dest_addr within the SRAM
' NOTE: does NOT work properely on overlapping copies
' NOTE: function assumes both auto inc after read and write operations
'
' Parameters: _dest_addr - 19-bit destination address in SRAM  
'             _src_addr  - 19-bit source address in SRAM
'             _num_bytes   - number of bytes to copy
  
  ' if destination and source copies < 64K then directly load the address into latch, else more complex block copy is needed
  ' and local cache

  ' test for null copy 
  if ( _num_bytes == 0 )
    return( _num_bytes)

  ' if destination block and source block start and end addresses are BOTH within the lower 64K then copy directly
  ' else use local cache to speed up process, cache is set for 128-1024 bytes

  if ( (_dest_addr + _num_bytes ) =< $FFFF and (_src_addr + _num_bytes ) =< $FFFF )
    ' copy straight from source to destination
    repeat _index from 0 to _num_bytes - 1
      SRAM_Write64K_S( _dest_addr++, SRAM_Read64K_S( _src_addr++ ) )
  else
    ' need to copy in blocks using local prop mem cache, walking out from source to destination could take thousands of cycles each time
    ' n + (n+1) + (n+2) + ... + (n+m) = O(n^2), so lets try to cache things a bit

    repeat while _num_bytes > 0

      ' determine how many bytes to copy this pass min(LOCAL_MEM_CACHE_SIZE, _num_bytes)
      if (_num_bytes < LOCAL_MEM_CACHE_SIZE)
        ' this pass needs to copy less than a cache page size
        _bytes_to_copy := _num_bytes
      else
        _bytes_to_copy := LOCAL_MEM_CACHE_SIZE

      ' re-compute number of bytes left
      _num_bytes := _num_bytes - _bytes_to_copy
      
      ' read bytes from SRAM, seek SRAM out to src_addr
      SRAM_LoadAddr512K_S( _src_addr )

      ' read data into cache
      repeat _index from 0 to _bytes_to_copy-1
        local_mem_cache[ _index ] := SRAM_ReadAuto_S
        
      ' seek SRAM to destination address, prepare to write back
      SRAM_LoadAddr512K_S( _dest_addr )

      ' write data back to sram from cache
      repeat _index from 0 to _bytes_to_copy-1
        SRAM_WriteAuto_S( local_mem_cache[ _index ] )

      ' update pointers
      _src_addr  += _bytes_to_copy         
      _dest_addr += _bytes_to_copy
      ' end repeat while loop

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  return ( _num_bytes )

' ////////////////////////////////////////////////////////////////////

PUB SRAM_Read64K_S( _addr16 )      
' this function reads the 8-bit byte addressed by the 16-bit sent address
'
' Parameters: addr16 - 16-bit address to read from 

  ' set global address
  sram_addr := _addr16

  ' set bus to write 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $FF ' $FF ouput, $00 input

  ' output low byte of address
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := (_addr16 & $FF)
    
  ' set control bits for load low memory address
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_LOADLO

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' output high byte of address
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := ((_addr16 >> 8) & $FF)
    
  ' set control bits for load low memory address
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_LOADHI

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' now we are ready to read the memory in
  ' set bus to read 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input
  
  ' set control bits for memory read
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_READ

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01

  ' data is now available on data bus
  sram_data := INA[ SRAM_IO_7..SRAM_IO_0 ]

  OUTA[ SRAM_STROBE ]              := $00

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_data)

' ////////////////////////////////////////////////////////////////////

PUB SRAM_ReadAuto_S      
' this function reads the 8-bit byte addressed by the controller currently
' Parameters: None

  ' now we are ready to read the memory in
  ' set bus to read 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input
  
  ' set control bits for memory read
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_READ

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01

  ' data is now available on data bus
  sram_data := INA[ SRAM_IO_7..SRAM_IO_0 ]

  OUTA[ SRAM_STROBE ]              := $00

  ' adjust global sram_addr to reflect operation
  if (sram_ctrl & %10_00) ' test for post increment
    sram_addr += ((sram_ctrl >> 2) & %01)
  else
      sram_addr -= ((sram_ctrl >> 2) & %01)   

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_data)

' ////////////////////////////////////////////////////////////////////

PUB SRAM_LoadAddr64K_S ( _addr16 )       
' this function loads the lower 16-bits of the 19-bit address latch
'
' Parameters: _addr16 - 16-bit address to set the SRAM address latch to, upper 3-bits is zero'ed 

  ' set global address
  sram_addr := _addr16

  ' set bus to write 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $FF ' $FF ouput, $00 input

  ' output low byte of address
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := (_addr16 & $FF)
    
  ' set control bits for load low memory address
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_LOADLO

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' output high byte of address
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := ((_addr16 >> 8) & $FF)
    
  ' set control bits for load low memory address
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_LOADHI

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_addr)

' ////////////////////////////////////////////////////////////////////
 
PUB SRAM_LoadAddrLow_S ( _addr8 )       
' this function loads the lower 8-bits of the address latch
'
' Parameters: _addr8 - 8-bit address to set lower 8-bits of SRAM address latch to 

  _addr8 := (_addr8 & $FF) ' make sure only 8-bits 

  ' set global address by updating only the lower address
  sram_addr := ((sram_addr & $7_FF00) | (_addr8 << 8)) ' note upper 3-bits will remain the same

  ' set bus to write 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $FF ' $FF ouput, $00 input

  ' output low byte of address
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := _addr8
    
  ' set control bits for load low memory address
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_LOADLO

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_addr)

' ////////////////////////////////////////////////////////////////////
 
PUB SRAM_LoadAddrHi_S ( _addr8 )       
' this function loads the upper 8-bits of the address latch, a15..a8, the upper address bits (a18, a17, a16) will be zero'ed by controller
' set global address by updating only the lower address
'
' Parameters: _addr8 - 8-bit address to set upper 8-bits (15..8) of SRAM address latch to 

  _addr8 := (_addr8 & $FF) ' make sure only 8-bits

  sram_addr := ((sram_addr & $0_00FF) | (_addr8 << 8)) ' note upper 3-bits are cleared since controller's side effect is to clear on high latch write

  ' set bus to write 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $FF ' $FF ouput, $00 input

  ' output low byte of address
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := _addr8
    
  ' set control bits for load high memory address
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_LOADHI

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_addr)

' ////////////////////////////////////////////////////////////////////

PUB SRAM_LoadAddr512K_S ( _addr19 ) | _index       
' this function loads the enture 19-bit sent address into the SRAM address latch, first the lower 16-bits
' that are directly accessible, then walks/advanced to the final target with dummy reads if need be
' NOTE: sram controller must be in post inc mode for read
'
' Parameters: _addr19 - 19-bit address to set the SRAM address latch to 

  ' set global address
  sram_addr := _addr19

  if ( _addr19 =< $FFFF )
    ' set starting address
    SRAM_LoadAddr64K_S( _addr19 )
  else
    ' need to walk out to starting address, we know that starting address is greater than 64K, so start there
    SRAM_LoadAddr64K_S( $FFFF )    
    ' now walk the rest of the way with dummy reads...
    repeat _index from 0 to (_addr19 - $FFFF) - 1    
      SRAM_ReadAuto_S

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_addr)

' ////////////////////////////////////////////////////////////////////

PUB SRAM_WriteAuto_S ( _data8 )
' this function writes a single a 8-bit byte to the sram
'
' Parameters: data8  - 8-bit data to write 
'           

  ' set global address
   sram_data := _data8

  ' set bus to write 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $FF ' $FF ouput, $00 input
 
  ' now we are ready to write memory

  ' place data on bus (still in output mode)
  OUTA[ SRAM_IO_7..SRAM_IO_0 ] := _data8 
  
  ' set control bits for memory write
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_WRITE

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' adjust global sram_addr to reflect operation
  if (sram_ctrl & %10_00) ' test for post increment
    sram_addr += ((sram_ctrl >> 2) & %01)
  else
      sram_addr -= ((sram_ctrl >> 2) & %01)   

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_data)

' ////////////////////////////////////////////////////////////////////

PUB SRAM_Write64K_S ( _addr16, _data8 )      
' this function writes a single a 8-bit byte to the sram
'
' Parameters: _addr16 - 16-bit address to write to 
'             _data8  - 8-bit data to write

  ' set global address and data
  sram_addr := _addr16
  sram_data := _data8

  ' set bus to write 
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $FF ' $FF ouput, $00 input

  ' output low byte of address
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := (_addr16 & $FF)
    
  ' set control bits for load low memory address
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_LOADLO

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' output high byte of address
  OUTA[ SRAM_IO_7..SRAM_IO_0 ]     := ((_addr16 >> 8) & $FF)
    
  ' set control bits for load low memory address
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_LOADHI

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' now we are ready to write memory

  ' place data on bus (still in output mode)
  OUTA[ SRAM_IO_7..SRAM_IO_0 ] := _data8 
  
  ' set control bits for memory write
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := SRAM_CMD_WRITE

  ' now strobe sram clk line
  OUTA[ SRAM_STROBE ]              := $00
  OUTA[ SRAM_STROBE ]              := $01
  OUTA[ SRAM_STROBE ]              := $00  

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return data to caller
  return(sram_data)

' /////////////////////////////////////////////////////////////////////////////

PUB MM_Copyto_SRAM_S( _dest_addr19, _src_addr16,  _num_bytes) | _index 
' this function copies bytes anywhere in the propellers 64K main memory into the SRAMs 512K memory
' NOTE: assumes the controller is post increment for write mode 
'
' Parameters: _dest_addr19 - 19-bit destination address in SRAM  
'             _src_addr16  - 16-bit source address in propeller main memory
'             _num_bytes   - number of bytes to copy

' first set the address pointer in the SRAM controller to destination address
  SRAM_LoadAddr512K_S ( _dest_addr19 )

' now simply perform a byte copy from mm to sram
  repeat _index from 0 to _num_bytes-1
    SRAM_WriteAuto_S( byte[ _src_addr16++ ] )

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return number of bytes copied
  return(_num_bytes)

' /////////////////////////////////////////////////////////////////////////////

PUB SRAM_Copyto_MM_S( _dest_addr16, _src_addr19,  _num_bytes) | _index 
' this function copies bytes from the 512K SRAM to anywhere in the propellers 64K main memory
' NOTE: assumes the controller is post increment for read mode
'
' Parameters: _dest_addr16 - 16-bit destination address in propeller main memory  
'             _src_addr19  - 19-bit source address in SRAM 
'             _num_bytes   - number of bytes to copy

  ' first set the address pointer in the SRAM controller to destination address
  SRAM_LoadAddr512K_S ( _src_addr19 )

  ' now simply perform a byte copy from sram to mm
  repeat _index from 0 to _num_bytes-1
    byte[ _dest_addr16++ ] := SRAM_ReadAuto_S 

  ' needed to interact properlly with ASM driver for now
  OUTA[ SRAM_CTRL_1..SRAM_CTRL_0 ] := %000000_00
  DIRA[ SRAM_IO_7..SRAM_IO_0 ]     := $00 ' $FF ouput, $00 input

  ' return number of bytes copied
  return(_num_bytes)

'//////////////////////////////////////////////////////////////////////////////
' DATA SECTION ////////////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

DAT

' local memory cache used for spin SRAM functions when local buffer is needed (256 bytes for now)
local_mem_cache         byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 
                        byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                        byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                        byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

                        