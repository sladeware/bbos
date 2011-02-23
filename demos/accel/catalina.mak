
BBOS=../../bbos

all:
	catalina -M2m -v -y -lci -DPC -DDEMO \
	-I. -I../.. \
	$(BBOS)/kernel/idle.c $(BBOS)/kernel/system.c $(BBOS)/kernel/port.c \
	$(BBOS)/kernel/thread.c $(BBOS)/hardware/drivers/accel/h48c.c \
	$(BBOS)/hardware/drivers/spi/spi_stamp.c $(BBOS)/kernel/schedulers/fcfs.c demo.c \
	-o demo

load:
	bstl -p 3 demo.binary


