
CC = /usr/local/lib/catalina/bin/catalina

INCLUDE = ../..
KERNEL = ../../bbos/kernel

CFLAGS = -v -W -lc -D DEMO -x0 -M2m -I. -I$(INCLUDE)

SRCS_C = hello_world.c $(KERNEL)/time.c \
	$(KERNEL)/process/port.c $(KERNEL)/process.c \
	$(KERNEL)/system.c $(KERNEL)/mm/mempool.c \
	$(KERNEL)/process/scheduler/fcfs.c $(KERNEL)/process/scheduler/static.c \
	$(KERNEL)/process/thread.c $(KERNEL)/process/thread/idle.c \
	$(KERNEL)/hardware.c $(KERNEL)/application.c

SRCS = $(SRCS_C)

OBJS = $(SRCS_C:.c=.o)

.PHONY: all
all: demo

demo: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

.PHONY: clean

clean:
	rm -v -f *.o demo $(KERNEL)/*.o $(KERNEL)/hardware/device/*.o \
	$(KERNEL)/mm/*.o $(KERNEL)/process/*.o $(KERNEL)/process/thread/*.o \
	$(KERNEL)/process/scheduler/*.o




