
CC = gcc -O

LIBS =

CDEBUG = -g

INCLUDE = ../../include
KERNEL = ../../src/kernel

CFLAGS = $(CDEBUG) -I. -I$(INCLUDE)
LDFLAGS = -g

SRCS_C = hello_world.c $(KERNEL)/process/itc.c $(KERNEL)/time.c \
	$(KERNEL)/process/itc/port.c $(KERNEL)/process.c \
	$(KERNEL)/system.c $(KERNEL)/mm/mempool.c \
	$(KERNEL)/hardware/device.c $(KERNEL)/process/scheduler/basic.c \
	$(KERNEL)/process/thread.c $(KERNEL)/process/itc/mqueue.c \
  $(KERNEL)/hardware.c

SRCS = $(SRCS_C)

OBJS = $(SRCS_C:.c=.o)

.PHONY: all
all: demo

demo: $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBS)

.PHONY: clean

clean:
	rm -v -f *.o demo $(KERNEL)/*.o $(KERNEL)/hardware/device/*.o \
	$(KERNEL)/mm/*.o $(KERNEL)/process/*.o

