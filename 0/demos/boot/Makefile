
OBJCOPY = objcopy

BBOS_HOST_ARCH := $(shell uname -m | \
	sed -e s/i.86/i386/ \
	    -e s/sun4u/sparc64/ \
	    -e s/arm.*/arm/ \
	    -e s/sa110/arm/ \
	    -e s/powerpc/ppc/ \
	    -e s/macppc/ppc/)

BBOS_HOST_OS := $(shell uname -s | tr '[:upper:]' '[:lower:]' | \
	    sed -e 's/\(cygwin\).*/cygwin/')

export	BBOS_HOST_ARCH BBOS_HOST_OS

ifeq ($(BBOS_HOST_ARCH),i386)
BBOS_LOAD_ADDR = 0x40000
endif

ELF	= demo
BIN	= demo.bin
SREC	= demo.srec

#LIBAOBJS=
COBJS	:= $(SREC:.srec=.o)

LIBOBJS	= $(addprefix $(obj),$(LIBAOBJS) $(LIBCOBJS))

SRCS := $(COBJS:.o=.c) $(LIBCOBJS:.o=.c) $(if $(LIBAOBJS),$(LIBAOBJS:.o=.S))
OBJS := $(addprefix $(obj),$(COBJS))
ELF	:= $(addprefix $(obj),$(ELF))
BIN	:= $(addprefix $(obj),$(BIN))

gcclibdir := $(shell dirname `$(CC) -print-libgcc-file-name`)
clibdir := $(shell dirname `$(CC) $(CFLAGS) -print-file-name=libc.a`)

all: $(obj).depend $(OBJS) $(LIB) $(BIN) $(ELF)

$(LIB):	$(obj).depend $(LIBOBJS)
		$(AR) $(ARFLAGS) $@ $(LIBOBJS)

$(ELF):
$(obj)%:	$(obj)%.o $(LIB)
			$(LD) -g $(EX_LDFLAGS) -Ttext 0x07000000 -Tdata 0x07040000 \
			-o $@ -e $(notdir $(<:.o=)) $< $(LIB) \
			-L$(gcclibdir) -lgcc

$(BIN):
$(obj)%.bin:	$(obj)%
				$(OBJCOPY) -O binary $< $@ 2>/dev/null

_depend: $(obj).depend

BBOS_PLATFORM_CPPFLAGS += -DCONFIG_I386 -D__I386__

RELFLAGS= $(BBOS_PLATFORM_RELFLAGS)
DBGFLAGS= -g # -DDEBUG
OPTFLAGS= -Os #-fomit-frame-pointer

OBJCFLAGS += --gap-fill=0xff

CPPFLAGS := $(DBGFLAGS) $(OPTFLAGS) $(RELFLAGS)		\
	-D__KERNEL__ 

CPPFLAGS += -fno-builtin -ffreestanding -nostdinc 	\
	-isystem $(gccincdir) -pipe $(BBOS_PLATFORM_CPPFLAGS)

$(obj).depend: $(SRCS)
	@rm -f $@
	@for f in $(SRCS); do \
		g=`basename $$f | sed -e 's/\(.*\)\.\w/\1.o/'`; \
		$(CC) -M $(HOST_CFLAGS) $(CPPFLAGS) -MQ $(obj)$$g $$f >> $@ ; \
	done

clean:
	find . -type f \
		\( -name '*.bak' -o -name '*~' \
		-o -name '*.o'  -o -name '*.a'  \) -print \
		| xargs rm -f
	@rm demo
	@rm demo.bin
