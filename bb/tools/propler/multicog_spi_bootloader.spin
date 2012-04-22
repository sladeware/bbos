'_____________________________________________________________________
'
' Bootloader.
'
' Copyright (c) 2012 Sladeware LLC
'_____________________________________________________________________
'

CON
  ' Set these to suit the platform by modifying "Catalina_Common"
  ' Also, that is now where the PIN definitions for the platform
  ' are defined. Do not modify these in this file.
  _clkmode  = Common#CLOCKMODE
  _xinfreq  = Common#XTALFREQ
  _stack    = Common#STACKSIZE

  ' Debugging options (note that enabling debugging will also require
  ' SLOW_XMIT to be enabled to avoid comms timeouts):
'#define SLOW_XMIT

  NR_COGS = 8
  LAST_COG = NR_COGS ' last cog to be stoped. 

  PAGE_SIZE = Common#FLIST_SSIZ
  ' Set these to suit the Generic SD Loader, or whatever other
  ' program is executed on the master propeller.
  MODE      = Common#SIO_LOAD_MODE
  BAUD      = Common#SIO_BAUD

  ' Set up Proxy, HMI and CACHE symbols and constants:
#include "Constants.inc"

'_____________________________________________________________________

OBJ
  Common     : "Catalina_Common"     ' Common definitions
  SIO        : "Catalina_SIO_Plugin" ' SIO plugin

'_____________________________________________________________________

PUB Start : ok | REG, DATA, PAGE, BLOCK, XFER, MAX_LOAD
  ' Set up the Registry - required to use the SIO Plugin
  Common.InitializeRegistry

  REG      := Common#REGISTRY
  DATA     := Common#LOADTIME_ALLOC
  PAGE     := DATA - PAGE_SIZE
  BLOCK    := PAGE - SIO#BLOCK_SIZE
  XFER     := BLOCK - 8
  DATA     := XFER
  MAX_LOAD := XFER ' cannot load past here

  ' Start the SIO plugin
  SIO.Start(BLOCK, Common#SI_PIN, Common#SO_PIN, MODE, BAUD, TRUE)

  ' Load a program from serial I/O to Hub and XMM RAM.
  ' The first 31k (32k minus any buffer space) is loaded
  ' into Hub RAM, and any data beyond 32k is loaded into
  ' XMM. Then the Propeller is restarted.
  '
  ' Initiate the low level bootloader
  max_hub_load := MAX_LOAD
  SIO_IO_Block := BLOCK
  cognew(@entry, @REG)

'_____________________________________________________________________

DAT
        org 0
'
'------------------------------------ ENTRY ------------------------------------
'

entry

'
'--------------------------------- REGISTRATION --------------------------------
'
        mov    r0,par                         ' point to parameters
        rdlong reg_addr,r0                    ' get registry address
        add    r0,#4
        'rdlong SIO_IO_Block,r0               ' get io block address
        add    r0,#4
        rdlong page_addr,r0                   ' get page buffer address
        add    r0,#4
        rdlong xfer_addr,r0                   ' get xfer buffer address

        rdlong SavedFreq,#0                   ' save the current clock freq
        rdbyte SavedMode,#4                   ' ... and mode

        mov r0, #32                   '
        mov img_addr, img_mapping     '
        mov r1, #$0 ' fill it by -1   '
clear_img_mapping                     ' clear
        wrbyte r1, img_addr           ' map of images
        add img_addr, #1
        djnz r0, #clear_img_mapping

wait_loop
        call   #SIO_ReadSync                 ' wait ...
        cmps   r0, #0 wz, wc                 ' ... for ...
  if_be jmp    #wait_loop                    ' ... sync signal
        mov    nr_imgs, r0                   ' number of images to be read

read_img                          ' start reading
        tjz    nr_imgs, #restart  ' ... required number of images
        sub    nr_imgs, #1

img_wait_loop                                 ' start waiting for the image
        call   #SIO_ReadSync                  ' wait ...
        cmps   r0,#0 wz,wc                    ' ... for ...
  if_be jmp    #img_wait_loop                 ' ... sync signal

        mov r0, #1
        mov img_addr, img_mapping
:place_for_img_addr                           '
        cmp r0, cpu_no wz
   if_z jmp #read_page
        add img_addr, #4
        add r0, #1
        jmp #:place_for_img_addr

read_page
        call   #clear_page                    ' clear the page
        mov    Hub_Addr, page_addr            ' read a page from SIO ...
        call   #sio_read_page                 ' ... to page buffer
        cmp    SIO_Addr,SIO_EOP wz            ' all done?
 if_z   jmp    #read_img                      ' yes - read next image

        mov    r7, SIO_Addr
        add    r7, #1
        cmp    img_addr, #0 wz                ' save image address
 if_nz  wrlong r7, img_addr
        mov    img_addr, #0

        mov    dst_addr, SIO_Addr             ' no - is addr less than ...
        cmp    SIO_Addr, hub_size wz,wc       ' ... than size of hub (32k)?
 if_ae  jmp    #:ignore                       ' no - ignore it
        cmp    SIO_Addr,max_hub_load wz,wc    ' yes - is addr less than
                                              ' maxmium loadable hub addr (31k)?
 if_b   jmp    #:copy_page_to_hub             ' yes - copy to hub

:ignore
        mov    lrc_addr,page_addr             ' no - ignore it
        jmp    #:send_lrc                     ' calculate lrc and send back

:copy_page_to_hub
        mov    end_addr,dst_addr
        mov    lrc_addr,dst_addr
        call   #copy_to_hub                   ' yes - copy page buffer to Hub RAM
        jmp    #:send_lrc                     ' calculate lrc and send back

:send_lrc
        mov    r0, lrc_addr                   ' if we didn't copy ...
        add    r0, max_page                   ' ... the whole sector ..
        cmp    r0, max_hub_load wz,wc         ' ... to hub RAM ...
 if_ae  mov    lrc_addr, page_addr            ' ... then return LRC of page buffer
        mov    lrc_size,max_page

        call   #calc_lrc_checksum
        call   #SIO_WriteSync
        mov    r0, lrc_rslt
        call   #SIO_WriteByte
        jmp    #read_page                     ' continue till all pages loaded

restart
        mov     time, cnt
        add     time, rst_delay
        waitcnt time, #0
        
        ' stop all cogs other than this one (up to LAST_COG), and restart
        ' this cog as a SPIN interpreter to execute the program now
        ' loaded in Hub RAM.

        cogid   r6              ' set our cog id
        mov     r1, #LAST_COG   ' don't restart beyond this cog
:stop_cog
        sub     r1,#1
        cmp     r1,r6 wz
 if_nz  cogstop r1
        tjnz    r1, #:stop_cog

        rdlong  r3,#8           ' Get vbase value
        and     r3,WordMask

        ' zero hub RAM from vbase to runtime_end, omitting
        ' any Hub RAM specified for use by the reserve cog.

        mov r5, img_mapping 'mov     r5,runtime_end
        mov     r4,r3
        jmp     #:chckRam

:zeroRam
        wrlong  Zero,r4
:incrRam
        add     r4,#4
        cmp     r4,rsv_begin wz,wc              ' don't overwrite ...
  if_b  jmp     #:chckRam                       ' ...
        cmp     r4,rsv_end wz,wc                ' ...
  if_b  jmp     #:incrRam                       ' ... reserved cog block
:chckRam
        cmp     r4,r5 wz,wc
  if_b  jmp     #:zeroRam

        rdlong  r2,#0
        cmp     r2,SavedFreq wz                 ' Is the clock frequency the same?
  if_ne jmp     #:change_clock
        rdbyte  r2,#4                           ' Get the clock mode
        cmp     r2,SavedMode wz                 ' If both same, just go start COG
  if_e  jmp     #:start_up
:change_clock
        and     r2,#$F8                         ' Force use of RCFAST clock while
        clkset  r2                              ' letting requested clock start
        mov     r2,XtalTime
:provide_startup_delay
        djnz    r2, #:provide_startup_delay     ' Allow 20ms@20MHz for xtal/pll to settle
        rdlong  r2, #4
        and     r2, #$FF                        ' Then switch to selected clock
        clkset  r2

:start_up
        mov r0, #0            ' start from the COG0
        mov r1, img_mapping   ' start from the first image
:load_next_img
        cmp r0, NR_COGS wz    ' check whether it is the last cog
   if_z jmp #:finish          ' ... yes - jump to finish
        rdlong img_addr, r1   ' read image addr
        add r1, #4            ' ... and move to the next one
        mov cpu_no, r0        ' save cog id and ...
        add r0, #1            ' move to the next one
        cmp img_addr, #$0 wz  ' jump if nothing to run for this cog
   if_z jmp #:load_next_img

'        cmp cpu_no, #5 wz
'   if_z jmp #:load_next_img
'        cmp cpu_no, #5 wz
'   if_nz cmp cpu_no, #3 wz
'   if_nz jmp #:load_next_img

        sub img_addr, #1        ' fix image address

        mov r2, img_addr     ' put image address
        add r2, #4           ' ... as PAR argument for
        shl r2, #16          ' ... coginit instruction

        mov r6, interpreter  ' start working on COG initialization ...
        or r6, r2            ' ... set image address ...
        or r6, cpu_no        ' ... set cpu no ...
        coginit r6           ' initialize COG

        mov time, cnt        ' small ...
        add time, rst_delay  ' ... delay to allow COG
        waitcnt time, #0     ' ... to settle

        jmp #:load_next_img  ' load next available image

:finish
        nop
        'cogid   r6
        'cogstop r6        

SavedFreq     long      $0
SavedMode     long      $0
StackMark     long      $FFF9FFFF               ' Two of these mark the base of the stack
WordMask      long      $0000FFFF
Zero          long      $0
XtalTime      long      20 * 20000 / 4 / 1      ' 20ms (@20MHz, 1 inst/loop)

time          long 0
rst_delay     long 80000000 ' 8000000
next_delay    long 80000000

'-------------------------------- Utility routines -----------------------------

'_____________________________________________________________________
'
' copy_to_hub - copy page buffer to Hub RAM.
'
' Input:
'   dst_addr : address to copy to (note - will not copy beyond
'              max_hub_load).
'
' NOTE: We assume everything is LONG aligned.
'_____________________________________________________________________
'

copy_to_hub mov    r1, page_addr
            mov    r0, max_page
            shr    r0, #2                           ' divide by 4 to get longs
:write_loop cmp    dst_addr, max_hub_load wc,wz     ' don't overwrite ...
      if_ae jmp    #copy_to_hub_ret                 ' ... beyond max_hub_load
            cmp    dst_addr,rsv_begin wc, wz        ' don't overwrite ...
      if_ae jmp    #copy_to_hub_ret                 ' ... reserved cog RAM block
            rdlong r2, r1
            wrlong r2, dst_addr
            add    r1, #4
            add    dst_addr, #4
            djnz   r0, #:write_loop
copy_to_hub_ret ret

'_____________________________________________________________________
'
' clear_page - clear the page
'_____________________________________________________________________
'
clear_page
        mov    r0, #0
        mov    r1, max_page
        mov    r2, page_addr
:clear_loop
        wrbyte r0, r2
        add    r2, #1
        djnz   r1, #:clear_loop
clear_page_ret
        ret

'_____________________________________________________________________
'
' calc_lrc_checkum - Calculate LRC checksum value of buffer
'
' Input
'    lrc_size = size of buffer
'    lrc_addr = address of buffer
' Output
'    lrc_rslt = result of XOR
'_____________________________________________________________________
'
calc_lrc_checksum
        mov    lrc_rslt,#0
        mov    r1,lrc_size
        mov    r2,lrc_addr
:calc_lrc_checksum_loop
        rdbyte r0,r2
        xor    lrc_rslt,r0
        add    r2,#1
        djnz   r1,#:calc_lrc_checksum_loop
calc_lrc_checksum_ret
        ret

lrc_addr      long      $0
lrc_size      long      $0
lrc_rslt      long      $0

'=====================================================================
' SIO Routines
'=====================================================================

'_____________________________________________________________________
'
' sio_read_page : Read data from SIO to HUB RAM.
' On Entry:
'    SIO_Addr  (32-bit): source address (not used, but updated after read)
'    Hub_Addr  (32-bit): destination address in main memory, 16-bits used
'    SIO_Len   (32-bit): number of bytes read, (max PAGE_SIZE)
'
' NOTE: data packets are:
'    4 bytes CPU + address
'    4 bytes size (but only a max of PAGE_SIZE will actually get loaded)
'    size bytes of data
'
' NOTE: The top byte of the address ($nn) is the CPU number (1 .. 3).
'
' NOTE ($nn $FF $FF $FF) ($00 $00 $00 $00) indicates end of data
'
' NOTE: to maintain synchronization, all data is read even if the CPU
'       number indicates the packet is not for this CPU.
'_____________________________________________________________________
'
sio_read_page
              call      #sio_read_long           ' read ...
              mov       SIO_Addr,SIO_Temp       ' ... address

              call      #sio_read_long           ' read ...
              mov       SIO_Len,SIO_Temp        ' ... size

              mov       SIO_Cnt1,SIO_Len        ' assume ...
              mov       SIO_Cnt2,#0             ' ... we will not discard data
              tjz       SIO_Len,#:SIO_AddrChk   ' check address if no data to read

              cmp       SIO_Len,max_page wc,wz  ' do we need to discard data?
        if_be jmp       #:SIO_RdLoop1           ' no - just read and save ...

              mov       SIO_Cnt2,SIO_Len        ' yes - calculate size of data to save ...
              sub       SIO_Cnt2,max_page       ' ... and size of data ...
              mov       SIO_Cnt1,max_page       ' ... to discard
              mov       SIO_Len,SIO_Cnt1        ' save size of data
:SIO_RdLoop1
              call      #SIO_ReadByte           ' read ...
              wrbyte    r0,Hub_Addr             ' ... and save ...
              add       Hub_Addr,#1             ' ... up to ...

              djnz      SIO_Cnt1,#:SIO_RdLoop1  ' ... max_page bytes
              tjz       SIO_Cnt2,#:SIO_AddrChk  ' if no more bytes, check address
:SIO_RdLoop2
              call      #SIO_ReadByte           ' read but discard ...

              djnz      SIO_Cnt2,#:SIO_RdLoop2  ' ... any remaining bytes
:SIO_AddrChk
              mov       r0,SIO_Addr             ' was this packet ...
              shr       r0,#24                  ' ... intended ...
              cmp       r0,cpu_no wz            ' ... for this CPU?
        if_nz jmp       #sio_read_page          ' no - read another packet
              mov       r0,SIO_Addr             ' yes - remove CPU number ...
              and       r0, low24               ' ... from ...
              mov       SIO_Addr,r0             ' ... data address

sio_read_page_ret
              ret

'_____________________________________________________________________
'
' sio_read_long : Read 4 bytes from SIO to SIO_Temp
'_____________________________________________________________________

sio_read_long
              mov       SIO_Cnt1,#4
:SIO_ReadLoop
              call      #SIO_ReadByte
              and       r0,#$FF                 ' mask the data to 8-bits
              andn      SIO_Temp,#$FF           ' combine byte read into SIO_Temp
              or        SIO_Temp,r0
              ror       SIO_Temp,#8
              djnz      SIO_Cnt1,#:SIO_ReadLoop
sio_read_long_ret
              ret

'_____________________________________________________________________
'
' SIO_DataReady - check if SIO data is ready.
' On exit:
'    r1 = rx_head
'    r2 = address of rx_tail
'    r3 = rx_tail
'    Z flag set is no data ready (i.e. rx_tail = rx_head).
'_____________________________________________________________________
'
SIO_DataReady
              rdlong    r1,SIO_IO_Block         ' get rx_head
              mov       r2,SIO_IO_Block         ' get ...
              add       r2,#4                   ' ...
              rdlong    r3,r2                   ' ... rx_tail
              cmp       r1,r3 wz                ' rx_tail = rx_head?
SIO_DataReady_ret
              ret

'_____________________________________________________________________
'
' SIO_ReadByteRaw : Read byte from SIO to r0, without byte unstuffing
'_____________________________________________________________________
'
SIO_ReadByteRaw
              mov       r0,cnt
              cmp       r0,SIO_StartTime wc
        if_nc sub       r0,SIO_StartTime
        if_c  subs      r0,SIO_StartTime
              cmp       r0,one_sec wz,wc
        if_a  jmp       #SIO_ReadByteRaw_err
              call      #SIO_DataReady          ' any SIO data available?
        if_z  jmp       #SIO_ReadByteRaw        ' no - wait
              mov       r1,SIO_IO_Block         ' yes - get received byte ...
              add       r1,#9*4                 ' ... from ...
              add       r1,r3                   ' ... rx_buffer ...
              rdbyte    r0,r1                   ' ... [rx_tail] ...
              add       r3,#1                   ' calculate ...
              and       r3,#$0f                 ' ... (rx_tail + 1) & $0f
              wrlong    r3,r2                   ' rx_tail := (rx_head + 1) & $0f

              jmp       #SIO_ReadByteRaw_ret
SIO_ReadByteRaw_err
              neg       r0,#1
SIO_ReadByteRaw_ret
              ret

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' SIO_ReadByte : Read byte from SIO to r0, unstuffing $FF $00 to just $FF
'
'          NOTE: returns -1 if the timeout expires, or -2 if a sync signal
'                (i.e. $FF CPU_no) is detected. Any other $FF $xx sequence
'                just returns as normal.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
SIO_ReadByte
              mov       SIO_StartTime,cnt
              test      save_data,#$100 wz      ' have we saved a byte?
        if_z  jmp       #:read_byte             ' no - read a new byte
              cmp       save_data,#$1FF wz      ' yes - was it $FF?
        if_z  jmp       #:read_byte             ' yes - read a new byte
              mov       r0,save_data            ' no - return ...
              and       r0,#$FF                 ' ... saved byte ...
              jmp       #:clear_saved_data      ' ... and clear saved data
:read_byte
              call      #SIO_ReadByteRaw        ' read a new byte
              cmps      r0,#0 wz,wc             ' read error?
        if_b  jmp       #SIO_ReadByte_ret       ' yes - return the error
              cmp       save_data,#$1FF wz      ' have we saved $FF?
        if_nz jmp       #:check_for_ff          ' no - check the byte we just read
              cmp       r0,cpu_no wz            ' yes - did we just read our CPU no?
        if_z  jmp       #:read_sync             ' yes - this is a sync signal
              cmp       r0,#0 wz                ' no - did we just read $00?
        if_z  jmp       #:unstuff_ff            ' yes - unstuff the $FF
              or        r0,#$100                ' no - save ...
              mov       save_data,r0            ' ... the byte we just read ...
              mov       r0,#$FF                 ' ... and return ...
              jmp       #SIO_ReadByte_ret       ' ... $FF instead
:unstuff_ff
              mov       r0,#$FF                 ' return unstuffed $FF
              jmp       #:clear_saved_data
:check_for_ff
              cmp       r0,#$ff wz              ' did we just read $FF?
        if_nz jmp       #:clear_saved_data      ' no - clear saved data and return the byte
              mov       save_data,#$1FF         ' yes - save the $FF ...
              jmp       #:read_byte             ' ... and read another byte
:read_sync
              neg       r0,#2                   ' return sync flag
:clear_saved_data
              mov       save_data,#0            ' clear saved data
SIO_ReadByte_ret
              ret
'
save_data     long      $0                      ' $100 + byte saved (e.g. $1FF if saved $FF)
'

'_____________________________________________________________________
'
' SIO_ByteDelay : Time to wait between bytes - this is currently set by
'                 trial and error, but to a fairly conservative value.
'_____________________________________________________________________
'
SIO_ByteDelay
              mov       r1,cnt
              add       r1,ByteDelay
              waitcnt   r1,#0
SIO_ByteDelay_ret
              ret

#ifdef SLOW_XMIT
ByteDelay long Common#CLOCKFREQ/50
#else
ByteDelay long Common#CLOCKFREQ/6000
#endif

'_____________________________________________________________________
'
' SIO_WriteByte : Write byte in r0 to SIO, without byte stuffing
'_____________________________________________________________________
'
SIO_WriteByteRaw
              call      #SIO_ByteDelay          ' delay between characters
              mov       r1,SIO_IO_Block         ' get ...
              add       r1,#8                   ' ...
              rdlong    r1,r1                   ' ... tx_head
              mov       r2,SIO_IO_Block         ' get ...
              add       r2,#12                  ' ...
              rdlong    r2,r2                   ' ... tx_tail
              mov       r3,r1                   ' calculate
              add       r3,#1                   ' (tx_head + 1) ...
              and       r3,#$0f                 ' ... & $0f
              cmp       r3,r2 wz                ' tx_tail = (tx_head + 1) & $0f ?
        if_z  jmp       #SIO_WriteByteRaw       ' yes - wait
              mov       r2,SIO_IO_Block         ' no ...
              add       r2,#13*4                ' ... tx_buffer ...
              add       r2,r1                   ' ... [tx_head] ...
              wrbyte    r0,r2                   ' ... := r0
              mov       r1,SIO_IO_Block         ' tx_head :=
              add       r1,#8                   ' (tx_head +1) ...
              wrlong    r3,r1                   ' ... & $0f
              mov       r1,SIO_IO_Block         ' should ...
              add       r1,#6*4                 ' ... we ...
              rdlong    r1,r1                   ' ... ignore ...
              and       r1,#%1000 wz            ' ... echo ?
        if_z  jmp       #SIO_WriteByteRaw_ret   ' no - just return
              call      #SIO_ReadByte           ' yes - recieve echo before returning
SIO_WriteByteRaw_ret
              ret
'
' SIO_WriteByte : Write byte in r0 to SIO, performing byte stuffing
'                 by converting each $FF into $FF $00 to ensure that
'                 the sync signal of $FF $02 is never transmitted
'                 except when specifically intended.
'
SIO_WriteByte
              and       r0,#$FF
              cmp       r0,#$FF wz
        if_nz jmp       #:no_stuff
              call      #SIO_WriteByteRaw
              mov       r0,#$00
:no_stuff
              call      #SIO_WriteByteRaw
SIO_WriteByte_ret
              ret

'_____________________________________________________________________
'
' SIO_WriteSync : Write the Sync signal ($FF $01 for CPU #1, or $FF $03 for CPU #3).
'                 These sequences can never be generated accidentally because during
'                 normal sending $FF is stuffed to $FF $00
' On Entry:
'    cpu_no : CPU number (must be non zero!)
'_____________________________________________________________________
'
SIO_WriteSync
              mov       r0,#$FF
              call      #SIO_WriteByteRaw
              mov       r0,cpu_no
              call      #SIO_WriteByteRaw
SIO_WriteSync_ret
              ret

'_____________________________________________________________________
'
' SIO_ReadSync : Wait for the Sync Signal ($FF $01 for CPU #1, or
' $FF $03 for CPU #3).
'                These sequences can never be generated accidentally because during
'                normal sending $FF is stuffed to $FF $00, so we can wait for this
'                without the risk of accidentally being triggered by a program being
'                sent to another CPU.
'
'                NOTE: ReadByteRaw returns failure if timeout expires
'_____________________________________________________________________
'
SIO_ReadSync
              mov       SIO_StartTime,cnt
:read_loop
              mov       r0,cnt
              cmp       r0,SIO_StartTime wc
        if_nc sub       r0,SIO_StartTime
        if_c  subs      r0,SIO_StartTime
              cmp       r0,one_sec wz,wc
        if_a  jmp       #:read_err
              call      #SIO_ReadByteRaw
              cmp       r0,#$FF wz
        if_nz jmp       #:read_loop
:check_cpu
              call      #SIO_ReadByteRaw
        '      cmp       r0,cpu_no wz
        'if_z  jmp       #SIO_ReadSync_ret
              tjnz      r0,#:define_cpu
              cmp       r0,#$FF wz
        if_z  jmp       #:check_cpu
              jmp       #:read_loop
:read_err
              neg       r0,#1
:define_cpu
              mov       cpu_no, r0
SIO_ReadSync_ret
              ret

'_____________________________________________________________________
'
' SIO-specific variables
'_____________________________________________________________________
'
SIO_Addr      long      $0
SIO_Len       long      $0
SIO_Cnt1      long      $0
SIO_Cnt2      long      $0
SIO_Temp      long      $0
SIO_IO_Block  long      $0                      ' address of shared I/O block
SIO_EOP       long      $00FFFFFE               ' end of page marker
SIO_StartTime long      $0
one_sec       long      Common#CLOCKFREQ

'
'------------------------------- Common Variables ------------------------------
'
top8          long      $FF000000
low24         long      $00FFFFFF

r0            long      $0
r1            long      $0
r2            long      $0
r3            long      $0
r4            long      $0
r5            long      $0
r6            long      $0
r7            long      $0

reg_addr      long      $0
page_addr     long      $0
page_end      long      $0
xfer_addr     long      $0
cpu_no        long      $0
nr_imgs       long      $0
booting_addr  long      $0
img_mapping   long      $7918
img_addr      long      $0

max_page      long      PAGE_SIZE
hub_size      long      $8000                   ' Hub RAM size is 32k (on the Prop I)
rsv_begin     long      $8000                   ' address of start of reserved cog block
rsv_end       long      $8000                   ' address of end of reserved cog block
              max_hub_load  long      $8000                   ' address we can load up to
runtime_end   long      Common#RUNTIME_ALLOC    ' address we can zero up to

src_addr      long      $0
dst_addr      long      $0
end_addr      long      $0
sect_count    long      $0

' see http://forums.parallax.com/forums/default.aspx?f=25&m=363100
'interpreter   long    ($0004 << 16) | ($F004 << 2) | %0000
interpreter   long    ($0000 << 16) | ($F004 << 2) | %0000

'
' temporary storage used in mul & div calculations
'
ftemp         long      $0
ftmp2         long      $0
ftmp3         long      $0
'
Hub_Addr      long      $0
'
              fit       $1f0                    ' max size
