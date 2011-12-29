{
HYDRA XTREME 512K SRAM CARD Test v1.0
Author: Andre' LaMothe, (C) Nurve Networks LLC

Update Log:

4.9.07 - Finished test suite, working great. About 15-20 seconds to test a card.

Description: This program exercises the SRAM the card by running a suite of tests below with a PASS/FAIL on each test. This test is
used to test the SRAM card during manufacturing or to confirm normal operation.

The card is booted and programmed with control word 0000_1111 which means auto increment on read and write.
Verify this by looking at the LEDs P3..P0 to the top right of card, they should be lit during normal operation.

SRAM Test Suite

Test 1. 1's fill         - PASS/FAIL
Test 2. 0's fill         - PASS/FAIL.
Test 3. 10's fill        - PASS/FAIL.
Test 4. Random fill      - PASS/FAIL.
Test 5. Incremental fill - PASS/FAIL.
}

'///////////////////////////////////////////////////////////////////////
' CONSTANTS SECTION ////////////////////////////////////////////////////
'///////////////////////////////////////////////////////////////////////

CON

  _clkmode = xtal2 + pll8x            ' enable external clock and pll times 4
  _xinfreq = 10_000_000 + 0000        ' set frequency to 10 MHZ plus some error
  _stack = ($3000 + 64) >> 2          ' accomodate display memory and stack

  ' graphics driver and screen constants
  PARAMCOUNT        = 14        
  ONSCREEN_BUFFER   = $5000           ' onscreen buffer

  ' size of graphics tile map
  X_TILES           = 16
  Y_TILES           = 12
  
  SCREEN_WIDTH      = 256
  SCREEN_HEIGHT     = 192 

  ' color constant's to make setting colors for parallax graphics setup easier
  COL_Black       = %0000_0010
  COL_DarkGrey    = %0000_0011
  COL_Grey        = %0000_0100
  COL_LightGrey   = %0000_0101
  COL_BrightGrey  = %0000_0110
  COL_White       = %0000_0111 

  COL_PowerBlue   = %0000_1_100 
  COL_Blue        = %0001_1_100
  COL_SkyBlue     = %0010_1_100
  COL_AquaMarine  = %0011_1_100
  COL_LightGreen  = %0100_1_100
  COL_Green       = %0101_1_100
  COL_GreenYellow = %0110_1_100
  COL_Yellow      = %0111_1_100
  COL_Gold        = %1000_1_100
  COL_Orange      = %1001_1_100
  COL_Red         = %1010_1_100
  COL_VioletRed   = %1011_1_100
  COL_Pink        = %1100_1_100
  COL_Magenta     = %1101_1_100
  COL_Violet      = %1110_1_100
  COL_Purple      = %1111_1_100

  ' each palette entry is a LONG arranged like so: color 3 | color 2 | color 1 | color 0
  COLOR_0 = (COL_Black  << 0)
  COLOR_1 = (COL_Red    << 8)
  COLOR_2 = (COL_Green  << 16)
  COLOR_3 = (COL_Blue   << 24)  

  ' position of state readouts for the left and right gamepads
  TEXT_X0 = 0
  TEXT_Y0 = 186

  ' memory fill areas for some of the longer tests
  MEMSTART  = 0
  MEMEND    = 512

'//////////////////////////////////////////////////////////////////////////////
' VARIABLES SECTION ///////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

VAR

  long  tv_status     '0/1/2 = off/visible/invisible           read-only
  long  tv_enable     '0/? = off/on                            write-only
  long  tv_pins       '%ppmmm = pins                           write-only
  long  tv_mode       '%ccinp = chroma,interlace,ntsc/pal,swap write-only
  long  tv_screen     'pointer to screen (words)               write-only
  long  tv_colors     'pointer to colors (longs)               write-only               
  long  tv_hc         'horizontal cells                        write-only
  long  tv_vc         'vertical cells                          write-only
  long  tv_hx         'horizontal cell expansion               write-only
  long  tv_vx         'vertical cell expansion                 write-only
  long  tv_ho         'horizontal offset                       write-only
  long  tv_vo         'vertical offset                         write-only
  long  tv_broadcast  'broadcast frequency (Hz)                write-only
  long  tv_auralcog   'aural fm cog                            write-only

  word  screen[X_TILES * Y_TILES] ' storage for screen tile map
  long  colors[64]                ' color look up table

  ' string/key stuff
  byte sbuffer[9]
  long data
  byte memfill
  byte value
 
  long testerror
  byte curr_key

  long offset
  long num_errors
  long rand
  long sum, sum2
 
'//////////////////////////////////////////////////////////////////////////////
' OBJECT DECLARATION SECTION //////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////
OBJ
  tv    : "tv_drv_010.spin"                 ' instantiate a tv object
  gr    : "graphics_drv_010.spin"           ' instantiate a graphics object
  sr    : "HX512KSRAM_ASM_DRV_010.spin"     ' instantiate ASM SRAM driver

'//////////////////////////////////////////////////////////////////////////////
' PUBLIC FUNCTIONS ////////////////////////////////////////////////////////////
'//////////////////////////////////////////////////////////////////////////////

PUB start | i, dx, dy, x, y, t, x1, y1, x0, y0, width, height

  'start tv
  longmove(@tv_status, @tvparams, paramcount)
  tv_screen := @screen
  tv_colors := @colors
  tv.start(@tv_status)

  repeat i from 0 to 64
    colors[i] := COLOR_3 | COLOR_2 | COLOR_1  | COLOR_0
    
  'init tile screen
  repeat dx from 0 to tv_hc - 1
    repeat dy from 0 to tv_vc - 1
      screen[dy * tv_hc + dx] := onscreen_buffer >> 6 + dy + dx * tv_vc + ((dy & $3F) << 10)

  ' start and setup graphics 256x192, with orgin (0,0) at bottom left of screen,
  ' simulating quadrant I of a cartesian coordinate system
  ' notice that the setup call uses the PRIMARY onscreen video buffer, so all graphics
  ' will show immediately on the screen, this is convenient for simple demos where we don't need animation
  gr.start
  gr.setup(X_TILES, Y_TILES, 0, 0, onscreen_buffer)


  ' initialize current COG's IO as not to conflict with ASM SRAM driver's (if its started)
  'sr.SRAM_InitalizeIO_S

  ' initialize ASM driver version of SRAM controller (will work with calls to SPIN version as long as above call is made to SPIN driver)
  sr.SRAM_Start_ASM_Driver(%000_11_11)

  repeat 1000 ' give driver a moment to start...

  ' perform test suite one test at a time
  ' Test 1. 1's fill - PASS/FAIL
  ' Test 2. 0's fill - PASS/FAIL.
  ' Test 3. 10's fill - PASS/FAIL.
  ' Test 4. Random fill - PASS/FAIL.
  ' Test 5. Incremental fill - PASS/FAIL.

  repeat
    gr.clear
    gr.textmode(1,1,6,1)  
    gr.colorwidth(3,0)
    gr.text(TEXT_X0, TEXT_Y0, string("HYDRA XTREME 512K SRAM Card Test Suite"))
    gr.text(TEXT_X0, TEXT_Y0-1*12, string("(C) Nurve Networks LLC 2007, V1.0"))  

    gr.colorwidth(1,0)
    gr.plot(TEXT_X0, TEXT_Y0-20)
    gr.line(TEXT_X0+255, TEXT_Y0-20)

    num_errors := 0
   
    ' Perform Test 1. 1's fill - PASS/FAIL //////////////////////////////////////////////////////////////////////////////
    gr.colorwidth(3,0)
    gr.text(TEXT_X0, TEXT_Y0-3*12, string("Test 1 - 11111111's fill:" ))
   
    ' fill the memory with 1's (255 for each byte)
    gr.text(TEXT_X0+26*6, TEXT_Y0-3*12, string("Writing..." ))
    sr.SRAM_MemSet_A( MEMSTART*1024,255,(MEMEND - MEMSTART)*1024 )
    'repeat 200_000  
   
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-3*12, string("Writing..." ))
   
    gr.colorwidth(3,0)  
    gr.text(TEXT_X0+26*6, TEXT_Y0-3*12, string("Reading..." ))
   
  {
    ' set starting address at $00000
    sr.SRAM_LoadAddr512K_A ( MEMSTART*1024 )
   
   
    sum := 0
    repeat i from MEMSTART*1024 to MEMEND*1024-1
     sum += sr.SRAM_ReadAuto_A
   }
    sum := sr.SRAM_MemSum_A(MEMSTART*1024, (MEMEND - MEMSTART)*1024)
   
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-3*12, string("Reading..." ))
   
    ' test results...
    if (sum == (MEMEND - MEMSTART)*1024*255)
      gr.colorwidth(2,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-3*12, string("PASSED" ))
    else
      gr.colorwidth(1,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-3*12, string("FAILED!" ))
      num_errors++
    
   
    ' Perform Test 2. 0's fill - PASS/FAIL  //////////////////////////////////////////////////////////////////////////////
    gr.colorwidth(3,0)
    gr.text(TEXT_X0, TEXT_Y0-4*12, string("Test 2 - 00000000's fill:" ))
   
    ' fill the memory with 0's (0 for each byte)
    gr.text(TEXT_X0+26*6, TEXT_Y0-4*12, string("Writing..." ))
    sr.SRAM_MemSet_A( MEMSTART*1024,0,(MEMEND - MEMSTART + 1)*1024 )
    'repeat 200_000  
   
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-4*12, string("Writing..." ))
   
    gr.colorwidth(3,0)  
    gr.text(TEXT_X0+26*6, TEXT_Y0-4*12, string("Reading..." ))
   
  {
    ' set starting address at $00000
    sr.SRAM_LoadAddr512K_A ( MEMSTART*1024 )
   
    sum := 0
    repeat i from MEMSTART*1024 to MEMEND*1024-1
     sum += sr.SRAM_ReadAuto_A
  }
   
    sum := sr.SRAM_MemSum_A(MEMSTART*1024, (MEMEND - MEMSTART)*1024)
         
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-4*12, string("Reading..." ))
   
    ' test results...
    if (sum == (MEMEND-MEMSTART)*1024*0)
      gr.colorwidth(2,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-4*12, string("PASSED" ))
    else
      gr.colorwidth(1,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-4*12, string("FAILED!" ))
      num_errors++   
   
    ' Perform Test 3. 10's fill - PASS/FAIL  //////////////////////////////////////////////////////////////////////////////
    gr.colorwidth(3,0)
    gr.text(TEXT_X0, TEXT_Y0-5*12, string("Test 3 - 10101010's fill:" ))
   
    ' fill the memory with 1010_1010's ($AA for each byte)
    gr.text(TEXT_X0+26*6, TEXT_Y0-5*12, string("Writing..." ))
    sr.SRAM_MemSet_A( MEMSTART*1024,$AA,(MEMEND - MEMSTART)*1024 )
    'repeat 200_000  
   
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-5*12, string("Writing..." ))
   
    gr.colorwidth(3,0)  
    gr.text(TEXT_X0+26*6, TEXT_Y0-5*12, string("Reading..." ))
   
  {
    ' set starting address at $00000
    sr.SRAM_LoadAddr512K_A ( MEMSTART*1024 )
   
    sum := 0
    repeat i from MEMSTART*1024 to MEMEND*1024-1
     sum += sr.SRAM_ReadAuto_A
  }
    sum := sr.SRAM_MemSum_A(MEMSTART*1024, (MEMEND - MEMSTART)*1024)
    
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-5*12, string("Reading..." ))
   
    ' test results...
    if (sum == (MEMEND-MEMSTART)*1024*$AA)
      gr.colorwidth(2,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-5*12, string("PASSED" ))
    else
      gr.colorwidth(1,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-5*12, string("FAILED!" ))
      num_errors++   
   
   
    ' Perform Test 4. Random fill - PASS/FAIL  //////////////////////////////////////////////////////////////////////////////
    gr.colorwidth(3,0)
    gr.text(TEXT_X0, TEXT_Y0-6*12, string("Test 4 - Random fill:" ))
   
    ' fill 32-96K with 8-bit random numbers
    gr.text(TEXT_X0+26*6, TEXT_Y0-6*12, string("Writing..." ))
   
    ' set starting address at $8000 (32K)
    sr.SRAM_LoadAddr512K_A ( $8000 )
   
    rand := 135632
    
    sum := 0
    repeat i from 0 to 64*1024-1
     sr.SRAM_WriteAuto_A( rand )
     sum += (rand & $FF)
     rand := rand?
   
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-6*12, string("Writing..." ))
   
    gr.colorwidth(3,0)  
    gr.text(TEXT_X0+26*6, TEXT_Y0-6*12, string("Reading..." ))
   
  {
    ' set starting address at $8000 (32K)
    sr.SRAM_LoadAddr512K_A ( $8000 )
   
    sum2 := 0
    repeat i from 0 to 64*1024-1
     sum2 += sr.SRAM_ReadAuto_A
  }
   
    sum2 := sr.SRAM_MemSum_A($8000, 64*1024)
   
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-6*12, string("Reading..." ))
   
    ' test results...
    if (sum == sum2)
      gr.colorwidth(2,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-6*12, string("PASSED" ))
    else
      gr.colorwidth(1,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-6*12, string("FAILED!" ))
      num_errors++   
   
    ' Perform Test 5. Incremental fill - PASS/FAIL  //////////////////////////////////////////////////////////////////////////////
    gr.colorwidth(3,0)
    gr.text(TEXT_X0, TEXT_Y0-7*12, string("Test 5 - Increment fill:" ))
   
    ' fill the memory with incrementing number 0...255 over and over
    gr.text(TEXT_X0+26*6, TEXT_Y0-7*12, string("Writing..." ))
   
    ' set starting address at $1_0000 (64K)
    sr.SRAM_LoadAddr512K_A ( $1_0000 )
   
    sum := 0
    repeat i from 0 to 64*1024-1
     value := i // 256
     sr.SRAM_WriteAuto_A ( value )
     sum += value
   
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-7*12, string("Writing..." ))
   
    gr.colorwidth(3,0)  
    gr.text(TEXT_X0+26*6, TEXT_Y0-7*12, string("Reading..." ))
   
  {
    ' set starting address at $1_0000 (64K)
    sr.SRAM_LoadAddr512K_A ( $1_0000 )
   
    sum2 := 0
    repeat i from 0 to 64*1024-1
     sum2 += sr.SRAM_ReadAuto_A
  }
   
    sum2 := sr.SRAM_MemSum_A($1_0000, 64*1024)
   
    gr.colorwidth(0,0)
    gr.text(TEXT_X0+26*6, TEXT_Y0-7*12, string("Reading..." ))
   
    ' test results...
    if (sum == sum2)
      gr.colorwidth(2,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-7*12, string("PASSED" ))
    else
      gr.colorwidth(1,0)
      gr.text(TEXT_X0+26*6, TEXT_Y0-7*12, string("FAILED!" ))
      num_errors++   
   
    ' final results
    if (num_errors == 0)
      gr.colorwidth(2,0)
      gr.text(TEXT_X0, TEXT_Y0-9*12, string("Memory Card PASSED" ))
    else
      gr.colorwidth(1,0)
      gr.text(TEXT_X0, TEXT_Y0-9*12, string("Memory Card FAILED!" ))

    repeat 500_000



DAT

' TV PARAMETERS FOR DRIVER /////////////////////////////////////////////
tvparams                long    0               'status
                        long    1               'enable
                        long    %011_0000       'pins
                        long    %0000           'mode
                        long    0               'screen
                        long    0               'colors
                        long    x_tiles         'hc
                        long    y_tiles         'vc
                        long    10              'hx timing stretch
                        long    1               'vx
                        long    0               'ho
                        long    0               'vo
                        long    55_250_000      'broadcast on channel 2 VHF, each channel is 6 MHz above the previous
                        long    0               'auralcog

                        