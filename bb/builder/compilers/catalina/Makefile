# Copyright (c) 2012 Alexander Sviridenko

LCC_DIR=/usr/local/lib/catalina

all:
	homespun -b $(LCC_DIR)/target/Catalina_LMM_dynamic.spin -o catalina_lmm
	spinc catalina_lmm.binary > include/catalina_lmm_array.h
	dos2unix include/catalina_lmm_array.h
	cp include/* $(LCC_DIR)/include/
	make -C lib/libmulticog/ $@
	cp -Rvf lib/libmulticog $(LCC_DIR)/lib/
