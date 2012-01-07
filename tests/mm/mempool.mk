BB_DIR = ../..

all:
	gcc -I. -I$(BB_DIR) \
	$(BB_DIR)/bb/mm/mempool.c mempool.c \
	-o mempool