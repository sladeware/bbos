
CC = /usr/local/lib/catalina/bin/catalina

LIBS =

CDEBUG = -g

KERNEL = ../../bbos/kernel
HARDWARE = ../../bbos/hardware
DRIVERS = $(HARDWARE)/drivers

CFLAGS = -v -W -lc -DDEMO -x0 -M2m -I. -I../.. -I../../../../data/downloads/catalina_2.6_linux/include
LDFLAGS = -g

SRCS_C = test_yield.c $(KERNEL)/system.c $(KERNEL)/hardware.c $(KERNEL)/process.c \
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


