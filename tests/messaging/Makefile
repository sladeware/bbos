ROOT = ../..
SRCS = messaging.c $(ROOT)/bb/os/kernel/system.c \
  $(ROOT)/bb/os/hardware/processors/x86/delay.c \
	$(ROOT)/bb/os/kernel/schedulers/staticscheduler.c \
	$(ROOT)/bb/mm/mempool.c
INCS = $(ROOT)
OUT = messaging

all:
	gcc -I$(INCS) -I. $(SRCS)

