
CC = gcc -O

LIBS =

CDEBUG = -g

ROOT = ../../bbos
KERNEL = ../../bbos/kernel
HARDWARE = ../../bbos/hardware
DRIVERS = $(HARDWARE)/drivers

CFLAGS = $(CDEBUG) -I. -I../..
LDFLAGS = -g

SRCS_C = test_yield.c $(KERNEL)/system.c $(ROOT)/hardware.c $(KERNEL)/process.c \
	$(KERNEL)/time.c \
	$(KERNEL)/mm/mempool.c $(KERNEL)/process/port.c \
	$(KERNEL)/process/thread.c $(KERNEL)/process/scheduler/fcfs.c \
	$(KERNEL)/process/thread/idle.c \
	$(DRIVERS)/gpio.c $(DRIVERS)/gpio/p8x32a.c

SRCS = $(SRCS_C)

OBJS = $(SRCS_C:.c=.o)

.PHONY: all
all: demo

demo: $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBS)

.PHONY: clean

clean:
	rm -v -f *.o $(KERNEL)/*.o $(KERNEL)/*.pyc $(KERNEL)/hardware/device/*.o \
	$(KERNEL)/mm/*.o $(KERNEL)/process/*.o $(KERNEL)/process/scheduler/*.o \
	$(KERNEL)/process/thread/*.o $(DRIVERS)/*.o $(DRIVERS)/gpio/.*o $(DRIVERS)/gpio/p8x32a.o


