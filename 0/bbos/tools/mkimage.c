
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef __WIN32__
#include <netinet/in.h>		/* for host / network byte order conversions	*/
#endif
#include <sys/mman.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

#if defined(__BEOS__) || defined(__NetBSD__) || defined(__APPLE__)
#include <inttypes.h>
#endif

#ifdef __WIN32__
typedef unsigned int __u32;

#define SWAP_LONG(x) \
  ((__u32)(											 \
		   (((__u32)(x) & (__u32)0x000000ffUL) << 24) | \
		   (((__u32)(x) & (__u32)0x0000ff00UL) <<  8) | \
		   (((__u32)(x) & (__u32)0x00ff0000UL) >>  8) | \
		   (((__u32)(x) & (__u32)0xff000000UL) >> 24) ))
typedef		unsigned char	uint8_t;
typedef		unsigned short	uint16_t;
typedef		unsigned int	uint32_t;

#define  ntohl(a) SWAP_LONG(a)
#define  htonl(a) SWAP_LONG(a)
#endif	/* __WIN32__ */

#ifndef	O_BINARY /* should be define'd on __WIN32__ */
#define O_BINARY 0
#endif

#include <bbos/boot/image.h>

extern int errno;

#ifndef MAP_FAILED
#define MAP_FAILED (-1)
#endif

char *cmdname;

extern unsigned long crc32 (unsigned long crc, const char *buf, unsigned int len);

typedef struct table_entry {
  int	val;		/* as defined in image.h	*/
  char	*sname;		/* short (input) name		*/
  char	*lname;		/* long (output) name		*/
} table_entry_t;

table_entry_t arch_name[] = {
    {	IH_CPU_INVALID,		NULL,		"Invalid CPU", },
    {	IH_CPU_ALPHA,		"alpha",	"Alpha", },
    {	IH_CPU_ARM,         "arm",      "ARM", },
    {	IH_CPU_I386,		"x86",		"Intel x86", },
    {	IH_CPU_IA64,		"ia64",		"IA64", },
    {	IH_CPU_M68K,		"m68k",		"MC68000", },
    {	IH_CPU_MICROBLAZE,	"microblaze",	"MicroBlaze", },
    {	IH_CPU_MIPS,		"mips",		"MIPS",		},
    {	IH_CPU_MIPS64,		"mips64",	"MIPS 64 Bit",	},
    {	IH_CPU_NIOS,		"nios",		"NIOS",		},
    {	IH_CPU_NIOS2,		"nios2",	"NIOS II",	},
    {	IH_CPU_PPC,	        "ppc",      "PowerPC",	},
    {	IH_CPU_S390,		"s390",		"IBM S390",	},
    {	IH_CPU_SH,		    "sh",       "SuperH",	},
    {	IH_CPU_SPARC,		"sparc",	"SPARC",	},
    {	IH_CPU_SPARC64,		"sparc64",	"SPARC 64 Bit",	},
    {	IH_CPU_BLACKFIN,	"blackfin",	"Blackfin",	},
    {	IH_CPU_AVR32,		"avr32",	"AVR32",	},
    {	-1,			"",		"",		},
};

table_entry_t os_name[] = {
  {	IH_OS_INVALID,	NULL,		"Invalid OS",		},
  {	IH_OS_4_4BSD,	"4_4bsd",	"4_4BSD",		},
  {	IH_OS_ARTOS,	"artos",	"ARTOS",		},
  {	IH_OS_DELL,	"dell",		"Dell",			},
  {	IH_OS_ESIX,	"esix",		"Esix",			},
  {	IH_OS_FREEBSD,	"freebsd",	"FreeBSD",		},
  {	IH_OS_IRIX,	"irix",		"Irix",			},
  {	IH_OS_LINUX,	"linux",	"Linux",		},
  {	IH_OS_LYNXOS,	"lynxos",	"LynxOS",		},
  {	IH_OS_NCR,	"ncr",		"NCR",			},
  {	IH_OS_NETBSD,	"netbsd",	"NetBSD",		},
  {	IH_OS_OPENBSD,	"openbsd",	"OpenBSD",		},
  {	IH_OS_PSOS,	"psos",		"pSOS",			},
  {	IH_OS_QNX,	"qnx",		"QNX",			},
  {	IH_OS_RTEMS,	"rtems",	"RTEMS",		},
  {	IH_OS_SCO,	"sco",		"SCO",			},
  {	IH_OS_SOLARIS,	"solaris",	"Solaris",		},
  {	IH_OS_SVR4,	"svr4",		"SVR4",			},
  {	IH_OS_U_BOOT,	"u-boot",	"U-Boot",		},
  {	IH_OS_VXWORKS,	"vxworks",	"VxWorks",		},
  { IH_OS_BBOS, "bbos", "BBOS", },
  {	-1,		"",		"",			},
};

table_entry_t type_name[] = {
  {	IH_TYPE_INVALID,    NULL,	  "Invalid Image",	},
  {	IH_TYPE_FILESYSTEM, "filesystem", "Filesystem Image",	},
  {	IH_TYPE_FIRMWARE,   "firmware",	  "Firmware",		},
  {	IH_TYPE_KERNEL,	    "kernel",	  "Kernel Image",	},
  {	IH_TYPE_MULTI,	    "multi",	  "Multi-File Image",	},
  {	IH_TYPE_RAMDISK,    "ramdisk",	  "RAMDisk Image",	},
  {	IH_TYPE_SCRIPT,     "script",	  "Script",		},
  {	IH_TYPE_STANDALONE, "standalone", "Standalone Program", },
  {	IH_TYPE_FLATDT,     "flat_dt",    "Flat Device Tree",	},
  {	-1,		    "",		  "",			},
};

table_entry_t comp_name[] = {
  {	IH_COMP_NONE,	"none",		"uncompressed",		},
  {	IH_COMP_BZIP2,	"bzip2",	"bzip2 compressed",	},
  {	IH_COMP_GZIP,	"gzip",		"gzip compressed",	},
  {	-1,		"",		"",			},
};

static void copy_file(int, const char *, int);
static void usage(void);
static void print_header(image_header_t *);
static int get_table_entry(table_entry_t *, char *, char *);
static int get_arch(char *);
static int get_comp(char *);
static int get_os(char *);
static int get_type(char *);

char *datafile;
char *imagefile;

char *opt_name = "";
int opt_dflag = 0;
int opt_eflag = 0;
int opt_lflag = 0;
int opt_vflag = 0;
int opt_xflag = 0;
uint32_t opt_addr = 0;
uint32_t opt_ep = 0;
int opt_os = IH_OS_LINUX;
int opt_arch = IH_CPU_PPC;
int opt_type = IH_TYPE_KERNEL;
int opt_comp = IH_COMP_GZIP;

image_header_t header;
image_header_t *hdr = &header;

void
banner()
{
  printf("BBOS image maker v0.0.1\n");
}

int
main(int argc, char **argv)
{
  int ifd;
  uint32_t checksum;
  struct stat sbuf;
  unsigned char *ptr;

  banner();

  cmdname = *argv;

  while (--argc > 0 && **++argv == '-') {
	while (*++*argv) {
	  switch (**argv)
		{
		case 'h':
		  usage();
		case 'l':
		  opt_lflag = 1;
		  break;
		case 'A':
		  if ((--argc <= 0) || (opt_arch = get_arch(*++argv)) < 0)
			usage();
		  goto NEXT_ARG;
		case 'C':
		  if ((--argc <= 0) || (opt_comp = get_comp(*++argv)) < 0)
			usage ();
		  goto NEXT_ARG;
		case 'O':
		  if ((--argc <= 0) || (opt_os = get_os(*++argv)) < 0)
			usage ();
		  goto NEXT_ARG;
		case 'T':
		  if ((--argc <= 0) || (opt_type = get_type(*++argv)) < 0)
			usage ();
		  goto NEXT_ARG;
		case 'a':
		  if (--argc <= 0)
			usage();
		  opt_addr = strtoul(*++argv, (char **)&ptr, 16);
		  if (*ptr)
			{
			  fprintf(stderr, "%s: invalid load address %s\n", cmdname, *argv);
			  exit(EXIT_FAILURE);
			}
		  goto NEXT_ARG;
		case 'd':
		  if (--argc <= 0)
			usage ();
		  datafile = *++argv;
		  opt_dflag = 1;
		  goto NEXT_ARG;
		case 'e':
		  if (--argc <= 0)
			usage ();
		  opt_ep = strtoul(*++argv, (char **)&ptr, 16);
		  if (*ptr)
			{
			  fprintf(stderr, "%s: invalid entry point %s\n", cmdname, *argv);
			  exit(EXIT_FAILURE);
			}
		  opt_eflag = 1;
		  goto NEXT_ARG;
		case 'n':
		  if (--argc <= 0)
			usage();
		  opt_name = *++argv;
		  goto NEXT_ARG;
		case 'v':
		  opt_vflag++;
		  break;
		case 'x':
		  opt_xflag++;
		  break;
		default:
		  usage();
		}
	}
  NEXT_ARG: ;
  }

  if ((argc != 1) || ((opt_lflag ^ opt_dflag) == 0))
  	usage();

  if (!opt_eflag) {
	opt_ep = opt_addr;
	/* If XIP, entry point must be after the U-Boot header */
	if (opt_xflag)
	  opt_ep += sizeof(image_header_t);
  }

  /*
   * If XIP, ensure the entry point is equal to the load address plus
   * the size of the U-Boot header.
   */
  if (opt_xflag)
	if (opt_ep != opt_addr + sizeof(image_header_t)) {
	  fprintf(stderr, "%s: For XIP, the entry point must be the load addr + %lu\n", 
			  cmdname, (unsigned long)sizeof(image_header_t));
	  exit(EXIT_FAILURE);
	}

  imagefile = *argv;

  if (opt_lflag)
	ifd = open(imagefile, O_RDONLY|O_BINARY);
  else
	{
	  printf("Create '%s' image file\n", imagefile);
	  ifd = open(imagefile, O_RDWR|O_CREAT|O_TRUNC|O_BINARY, 0666);
	}

  if (ifd < 0) {
	fprintf(stderr, "%s: Can't open %s: %s\n", cmdname, imagefile, strerror(errno));
	exit(EXIT_FAILURE);
  }

  if (opt_lflag)
	{
	  int len;
	  char *data;
	  /*
	   * list header information of existing image
	   */
	  if (fstat(ifd, &sbuf) < 0)
		{
		  fprintf (stderr, "%s: Can't stat %s: %s\n",  cmdname, imagefile, strerror(errno));
		  exit (EXIT_FAILURE);
		}

	  if ((unsigned)sbuf.st_size < sizeof(image_header_t))
		{
		  fprintf (stderr,  "%s: Bad size: \"%s\" is no valid image\n",   cmdname, imagefile);
		  exit (EXIT_FAILURE);
		}

	  ptr = (unsigned char *)mmap(0, sbuf.st_size, PROT_READ, MAP_SHARED, ifd, 0);
	  if ((caddr_t)ptr == (caddr_t)-1)
		{
		  fprintf (stderr, "%s: Can't read %s: %s\n",  cmdname, imagefile, strerror(errno));
		  exit (EXIT_FAILURE);
		}

	/*
	 * create copy of header so that we can blank out the
	 * checksum field for checking - this can't be done
	 * on the PROT_READ mapped data.
	 */
	memcpy (hdr, ptr, sizeof(image_header_t));

	if (ntohl(hdr->ih_magic) != IH_MAGIC) {
	  fprintf (stderr,  "%s: Bad Magic Number: \"%s\" is no valid image\n",   cmdname, imagefile);
	  exit (EXIT_FAILURE);
	}

	data = (char *)hdr;
	len  = sizeof(image_header_t);

	checksum = ntohl(hdr->ih_hcrc);
	hdr->ih_hcrc = htonl(0);	/* clear for re-calculation */

	if (crc32 (0, data, len) != checksum) {
	  fprintf (stderr, "%s: ERROR: \"%s\" has bad header checksum!\n",  cmdname, imagefile);
	  exit (EXIT_FAILURE);
	}

	data = (char *)(ptr + sizeof(image_header_t));
	len  = sbuf.st_size - sizeof(image_header_t) ;

	if (crc32 (0, data, len) != ntohl(hdr->ih_dcrc)) {
	  fprintf (stderr,"%s: ERROR: \"%s\" has corrupted data!\n",cmdname, imagefile);
	  exit (EXIT_FAILURE);
	}

	/* for multi-file images we need the data part, too */
	print_header ((image_header_t *)ptr);

	(void) munmap((void *)ptr, sbuf.st_size);
	(void) close (ifd);

	exit (EXIT_SUCCESS);
  }

  /*
   * Must be -w then:
   *
   * write dummy header, to be fixed later
   */
  memset (hdr, 0, sizeof(image_header_t));

  if (write(ifd, hdr, sizeof(image_header_t)) != sizeof(image_header_t))
	{
	  fprintf (stderr, "%s: Write error on %s: %s\n",	cmdname, imagefile, strerror(errno));
	  exit (EXIT_FAILURE);
  }

  if (opt_type == IH_TYPE_MULTI || opt_type == IH_TYPE_SCRIPT) {
	char *file = datafile;
	uint32_t size;

	for (;;) {
	  char *sep = NULL;

	  if (file) {
		if ((sep = strchr(file, ':')) != NULL)
		  *sep = '\0';

		if (stat (file, &sbuf) < 0) {
		  fprintf (stderr, "%s: Can't stat %s: %s\n",  cmdname, file, strerror(errno));
		  exit (EXIT_FAILURE);
		}
		size = htonl(sbuf.st_size);
	  } else {
		size = 0;
	  }

	  if (write(ifd, (char *)&size, sizeof(size)) != sizeof(size)) {
		fprintf (stderr, "%s: Write error on %s: %s\n", cmdname, imagefile, strerror(errno));
		exit (EXIT_FAILURE);
	  }

	  if (!file) {
		break;
	  }

	  if (sep) {
		*sep = ':';
		file = sep + 1;
	  } else {
		file = NULL;
	  }
	}

	file = datafile;

	for (;;) {
	  char *sep = strchr(file, ':');
	  if (sep) {
		*sep = '\0';
		copy_file (ifd, file, 1);
		*sep++ = ':';
		file = sep;
	  } else {
		copy_file (ifd, file, 0);
		break;
	  }
	}
  } else {
	copy_file(ifd, datafile, 0);
  }

  /* We're a bit of paranoid */
#if defined(_POSIX_SYNCHRONIZED_IO) && !defined(__sun__) && !defined(__FreeBSD__)
  (void) fdatasync (ifd);
#else
  (void) fsync (ifd);
#endif

  if (fstat(ifd, &sbuf) < 0)
	{
	  fprintf (stderr, "%s: Can't stat %s: %s\n", cmdname, imagefile, strerror(errno));
	  exit(EXIT_FAILURE);
	}
  
  ptr = (unsigned char *)mmap(0, sbuf.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, ifd, 0);
  if (ptr == (unsigned char *)MAP_FAILED)
	{
	  fprintf(stderr, "%s: Can't map %s: %s\n",cmdname, imagefile, strerror(errno));
	  exit(EXIT_FAILURE);
	}
  
  hdr = (image_header_t *)ptr;

  checksum = crc32(0, (const char *)(ptr + sizeof(image_header_t)), sbuf.st_size - sizeof(image_header_t));

  /* Build new header */
  hdr->ih_magic = htonl(IH_MAGIC);
  hdr->ih_time = htonl(sbuf.st_mtime);
  hdr->ih_size = htonl(sbuf.st_size - sizeof(image_header_t));
  hdr->ih_load = htonl(opt_addr);
  hdr->ih_ep = htonl(opt_ep);
  hdr->ih_dcrc = htonl(checksum);
  hdr->ih_os = opt_os;
  hdr->ih_arch = opt_arch;
  hdr->ih_type = opt_type;
  hdr->ih_comp = opt_comp;

  strncpy((char *)hdr->ih_name, opt_name, IH_NMLEN);

  checksum = crc32(0,(const char *)hdr,sizeof(image_header_t));

  hdr->ih_hcrc = htonl(checksum);

  print_header (hdr);

  (void) munmap((void *)ptr, sbuf.st_size);

	/* We're a bit of paranoid */
#if defined(_POSIX_SYNCHRONIZED_IO) && !defined(__sun__) && !defined(__FreeBSD__)
  (void) fdatasync (ifd);
#else
  (void) fsync (ifd);
#endif

  if (close(ifd))
	{
	  fprintf(stderr, "%s: Write error on %s: %s\n", cmdname, imagefile, strerror(errno));
	  exit(EXIT_FAILURE);
	}

  exit(EXIT_SUCCESS);
}

static void
copy_file (int ifd, const char *datafile, int pad)
{
  int dfd;
  struct stat sbuf;
  unsigned char *ptr;
  int tail;
  int zero = 0;
  int offset = 0;
  int size;

  if (opt_vflag)
	fprintf (stderr, "Copy image '%s'\n", datafile);

  if ((dfd = open(datafile, O_RDONLY|O_BINARY)) < 0)
	{
	  fprintf(stderr, "%s: Can't open %s: %s\n",cmdname, datafile, strerror(errno));
	  exit(EXIT_FAILURE);
	}

  if (fstat(dfd, &sbuf) < 0)
	{
	  fprintf(stderr, "%s: Can't stat %s: %s\n", cmdname, datafile, strerror(errno));
	  exit(EXIT_FAILURE);
	}

  printf("\tSize\t: %d Bytes\n", (int)sbuf.st_size);

  ptr = (unsigned char *)mmap(0, sbuf.st_size, PROT_READ, MAP_SHARED, dfd, 0);
  if (ptr == (unsigned char *)MAP_FAILED)
	{
	  fprintf(stderr, "%s: Can't read %s: %s\n", cmdname, datafile, strerror(errno));
	  exit(EXIT_FAILURE);
	}

  if (opt_xflag)
	{
	  unsigned char *p = NULL;
	  /*
	   * XIP: do not append the image_header_t at the
	   * beginning of the file, but consume the space
	   * reserved for it.
	   */

	  if ((unsigned)sbuf.st_size < sizeof(image_header_t))
		{
		  fprintf(stderr, "%s: Bad size: \"%s\" is too small for XIP\n", cmdname, datafile);
		  exit(EXIT_FAILURE);
		}

	  for (p=ptr; p < ptr+sizeof(image_header_t); p++)
		if ( *p != 0xff )
		  {
			fprintf (stderr, "%s: Bad file: \"%s\" has invalid buffer for XIP\n", cmdname, datafile);
			exit (EXIT_FAILURE);
		  }

	  offset = sizeof(image_header_t);
	}

	size = sbuf.st_size - offset;

	if (write(ifd, ptr + offset, size) != size)
	  {
		fprintf(stderr, "%s: Write error on %s: %s\n", cmdname, imagefile, strerror(errno));
		exit(EXIT_FAILURE);
	  }

	if (pad && ((tail = size % 4) != 0))
	  if (write(ifd, (char *)&zero, 4-tail) != 4-tail)
		{
		  fprintf(stderr, "%s: Write error on %s: %s\n", cmdname, imagefile, strerror(errno));
		  exit(EXIT_FAILURE);
		}

	(void) munmap((void *)ptr, sbuf.st_size);
	(void) close(dfd);
}

void
usage ()
{
  fprintf(stderr, 
		  "Usage:\t%s [options] image...\n"
		  "\t%s -l image\n", cmdname, cmdname);
  fprintf(stderr,
		  "Options:\n"
		  " -h\t\t\tPrint this help message\n"
		  " -v\t\t\tBe verbose\n"
		  " -l\t\t\tList image header information\n"
		  " -A <arch>\t\tSet architecture\n"
		  " -O <os>\t\tSet operating system\n"
		  " -T <type>\t\tSet image type\n"
		  " -C <compression>\tSet compression type\n"
		  " -a <addr>\t\tSet load address (hex)\n"
		  " -e <ep>\t\tSet entry point (hex)\n"
		  " -n <name>\t\tSet image name\n"
		  " -d <file>[:<file>...]\tCopy image data from file\n"
		  " -x\t\t\tSet XIP (execute in place)\n");
	exit(EXIT_FAILURE);
}

static void
print_header (image_header_t *hdr)
{
  print_image_header(hdr);

  if (hdr->ih_type == IH_TYPE_MULTI || hdr->ih_type == IH_TYPE_SCRIPT) {
	uint32_t size;
	int i, ptrs;
	uint32_t pos;
	uint32_t *len_ptr = (uint32_t *) ((unsigned long)hdr + sizeof(image_header_t));

	/* determine number of images first (to calculate image offsets) */
	for (i=0; len_ptr[i]; ++i);	/* null pointer terminates list */
	ptrs = i; /* null pointer terminates list */

	pos = sizeof(image_header_t) + ptrs * sizeof(long);
	printf ("Contents:\n");
	for (i=0; len_ptr[i]; ++i)
	  {
		size = ntohl(len_ptr[i]);
		
		printf ("\tImage %d: %8d Bytes = %4d kB = %d MB\n",i, size, size>>10, size>>20);
		if (hdr->ih_type == IH_TYPE_SCRIPT && i > 0)
		  {
			/*
			 * the user may need to know offsets
			 * if planning to do something with
			 * multiple files
			 */
			printf ("\tOffset = %08X\n", pos);
		  }
		/* copy_file() will pad the first files to even word align */
		size += 3;
		size &= ~3;
		pos += size;
	  }
  }
}

static int 
get_arch(char *name)
{
  return (get_table_entry(arch_name, "CPU", name));
}


static int 
get_comp(char *name)
{
  return (get_table_entry(comp_name, "Compression", name));
}


static int 
get_os(char *name)
{
  return (get_table_entry(os_name, "OS", name));
}


static int 
get_type(char *name)
{
  return (get_table_entry(type_name, "Image", name));
}

static int 
get_table_entry(table_entry_t *table, char *msg, char *name)
{
  table_entry_t *t;
  int first = 1;

  for (t=table; t->val>=0; ++t) {
	if (t->sname && strcasecmp(t->sname, name)==0)
	  return (t->val);
  }
  fprintf (stderr, "\nInvalid %s Type - valid names are", msg);
  for (t=table; t->val>=0; ++t) {
	if (t->sname == NULL)
	  continue;
	fprintf (stderr, "%c %s", (first) ? ':' : ',', t->sname);
	first = 0;
  }
  fprintf (stderr, "\n");
  return (-1);
}
