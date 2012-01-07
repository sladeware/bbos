
BB_DIR = ../..

all:
	gcc -DBB_CONFIG_OS_H=\"ping_config.h\" -I. -I$(BB_DIR) \
	$(BB_DIR)/bb/os.c $(BB_DIR)/bb/mm/mempool.c \
	$(BB_DIR)/bb/os/kernel.c $(BB_DIR)/bb/os/kernel/itc.c \
	$(BB_DIR)/bb/os/kernel/schedulers/fcfsscheduler.c \
	ping.c  \
	-o ping
