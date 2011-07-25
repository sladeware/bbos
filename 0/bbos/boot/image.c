
#include <bbos/kernel/types.h>
#include <bbos/boot/image.h>

#include <stdio.h>

static void
print_image_type(image_header_t *hdr)
{
  char *os, *arch, *type, *comp;

  switch (hdr->ih_os)
	{
	case IH_OS_BBOS: os = "BBOS"; break;
	case IH_OS_INVALID:	os = "Invalid OS";		break;
	case IH_OS_NETBSD:	os = "NetBSD";			break;
	case IH_OS_LINUX:	os = "Linux";			break;
	case IH_OS_VXWORKS:	os = "VxWorks";			break;
	case IH_OS_QNX:		os = "QNX";			break;
	case IH_OS_U_BOOT:	os = "U-Boot";			break;
	case IH_OS_RTEMS:	os = "RTEMS";			break;
#ifdef CONFIG_ARTOS
	case IH_OS_ARTOS:	os = "ARTOS";			break;
#endif
#ifdef CONFIG_LYNXKDI
	case IH_OS_LYNXOS:	os = "LynxOS";			break;
#endif
	default:		os = "Unknown OS";		break;
	}
  
  switch (hdr->ih_arch)
	{
	case IH_CPU_INVALID:	arch = "Invalid CPU";		break;
	case IH_CPU_ALPHA:	arch = "Alpha";			break;
	case IH_CPU_ARM:	arch = "ARM";			break;
	case IH_CPU_AVR32:	arch = "AVR32";			break;
	case IH_CPU_I386:	arch = "Intel x86";		break;
	case IH_CPU_IA64:	arch = "IA64";			break;
	case IH_CPU_MIPS:	arch = "MIPS";			break;
	case IH_CPU_MIPS64:	arch = "MIPS 64 Bit";		break;
	case IH_CPU_PPC:	arch = "PowerPC";		break;
	case IH_CPU_S390:	arch = "IBM S390";		break;
	case IH_CPU_SH:		arch = "SuperH";		break;
	case IH_CPU_SPARC:	arch = "SPARC";			break;
	case IH_CPU_SPARC64:	arch = "SPARC 64 Bit";		break;
	case IH_CPU_M68K:	arch = "M68K"; 			break;
	case IH_CPU_MICROBLAZE:	arch = "Microblaze"; 		break;
	case IH_CPU_NIOS:	arch = "Nios";			break;
	case IH_CPU_NIOS2:	arch = "Nios-II";		break;
	default:		arch = "Unknown Architecture";	break;
	}

  switch (hdr->ih_type)
	{
	case IH_TYPE_INVALID:	type = "Invalid Image";		break;
	case IH_TYPE_STANDALONE:type = "Standalone Program";	break;
	case IH_TYPE_KERNEL:	type = "Kernel Image";		break;
	case IH_TYPE_RAMDISK:	type = "RAMDisk Image";		break;
	case IH_TYPE_MULTI:	type = "Multi-File Image";	break;
	case IH_TYPE_FIRMWARE:	type = "Firmware";		break;
	case IH_TYPE_SCRIPT:	type = "Script";		break;
	case IH_TYPE_FLATDT:	type = "Flat Device Tree";	break;
	default:		type = "Unknown Image";		break;
	}

  switch (hdr->ih_comp)
	{
	case IH_COMP_NONE:	comp = "uncompressed";		break;
	case IH_COMP_GZIP:	comp = "gzip compressed";	break;
	case IH_COMP_BZIP2:	comp = "bzip2 compressed";	break;
	default:		comp = "unknown compression";	break;
	}

  printf ("%s %s %s (%s)", arch, os, type, comp);
}

void
print_image_header(image_header_t *hdr)
{
  int size;
	
  size = ntohl(hdr->ih_size);

  printf("Image header dump\n");
  printf("\tImage Name\t: %.*s\n", IH_NMLEN, hdr->ih_name);
  printf("\tImage Type\t: "); print_image_type(hdr); printf("\n");
  printf("\tData Size\t: %d Bytes = %.2f kB = %.2f MB\n", size, (double)size/1.024e3, (double)size/1.048576e6);
  printf("\tLoad Address\t: 0x%08x\n", ntohl(hdr->ih_load));
  printf("\tEntry Point\t: 0x%08x\n", ntohl(hdr->ih_ep));
}


