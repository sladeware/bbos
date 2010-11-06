
# Hello world demo

ROOT = ../../bbos
KERNEL = $(ROOT)/kernel
HARDWARE = $(ROOT)/hardware
DRIVERS = $(HARDWARE)/drivers

HEX = demo.hex
DEVICE = 32MX795F512L
PK2 = pk2cmd -PPIC$(DEVICE) -R
CFLAGS = $(CDEBUG) -I. -I../..
CC = pic32mx-gcc -I. -I../.. -O3 -mips16 -s -mprocessor=$(DEVICE) -D__PIC32_FEATURE_SET__=795
LDFLAGS = -g

SRCS_C = hello_world.c $(KERNEL)/system.c $(ROOT)/hardware.c $(KERNEL)/process.c \
	$(KERNEL)/time.c \
	$(KERNEL)/mm/mempool.c $(KERNEL)/process/port.c \
	$(KERNEL)/process/thread.c $(KERNEL)/process/scheduler/fcfs.c \
	$(KERNEL)/process/thread/idle.c

.PHONY: all
all: $(HEX)

OBJS = $(SRCS_C:.c=.o)

$(HEX): demo.elf
	pic32mx-bin2hex -a demo.elf

.PHONY: demo.elf

#demo.elf: $(SRCS_C)
#	$(CC) -o $@ $(SRCS_C)

demo.elf: $(OBJS)
	$(CC) -o $@ $(OBJS)

write:
	$(PK2) -M -B$(PK2DEVFILE) -F$(HEX)

erase:
	$(PK2) -E

clean:
	rm -v -f ./*.o $(ROOT)/*.o $(KERNEL)/*.o $(KERNEL)/*.pyc $(KERNEL)/hardware/device/*.o \
	$(KERNEL)/mm/*.o $(KERNEL)/process/*.o $(KERNEL)/process/scheduler/*.o \
	$(KERNEL)/process/thread/*.o $(DRIVERS)/*.o $(DRIVERS)/gpio/.*o $(DRIVERS)/gpio/p8x32a.o \
	./*.elf ./*.hex

on:
	$(PK2) -T

off:
	$(PK2) -W

