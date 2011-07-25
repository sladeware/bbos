
BBOS=../../bbos

all:
	gcc \
	-I. -I../.. \
	$(BBOS)/kernel/idle.c $(BBOS)/kernel/system.c $(BBOS)/kernel/port.c \
	$(BBOS)/kernel/thread.c \
	$(BBOS)/kernel/schedulers/fcfs.c demo.c \
	-o demo


