
#include <stdlib.h>

typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;

#include <bbos/boot/image.h>
#include <bbos/lib/elf.h>
#include <stdio.h>
#include <sys/mman.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <string.h>

int 
main() 
{
  int err;
  struct stat info;
	
  char *fname = "image";

  int fd = open(fname, O_RDONLY|O_SYNC);
  fstat(fd, &info);
  printf("Image file\n");
  printf("\tName: %s\n", fname);
  printf("\tSize: %d\n", (int)info.st_size);

  image_header_t *image_header = malloc(sizeof(image_header_t));
  if (sizeof(image_header_t) != read(fd, image_header, sizeof(image_header_t)))
	{
	  printf("Can not read image header\n");
	  return 0;
	}
  print_image_header(image_header);

  Elf32_Ehdr *EH = malloc(sizeof(Elf32_Ehdr));
  if (sizeof(Elf32_Ehdr) != read(fd, EH, sizeof(Elf32_Ehdr)))
	{
	  printf("\nOn Elf header reading error : %d\n", errno);
	  printf("%s",strerror(errno));
	  return 1;
	}

  Elf32_Phdr *EPH = malloc(EH->e_phentsize);

  lseek(fd, EH->e_phoff + sizeof(image_header_t), SEEK_SET);
  int counter = EH->e_phnum;

  while (counter--)
	{
	  if (EH->e_phentsize != read(fd, EPH, EH->e_phentsize))
		{
		  printf("Can not read %d bytes\n", EH->e_phentsize);
		  return 1;
		}

	  printf("Reading finished successfully, type of section: %u\n", EPH->p_type);
	  if (EPH->p_type == 1)
		{
		  printf("\tVirtual address\t: 0x%x\n", EPH->p_vaddr);
		  printf("\tMemory size\t: %ld (take %ld)\n", 
				 (long)EPH->p_memsz, 
				 (long int)((EPH->p_memsz & ~(sysconf(_SC_PAGE_SIZE) - 1)) + 
							(long)(sysconf(_SC_PAGE_SIZE) * ((EPH->p_memsz & ~(sysconf(_SC_PAGE_SIZE) - 1))==0))));
		  printf("\tIn-file offset\t: %ld\n", (long)EPH->p_offset);

		  int pa = (int) mmap((void*)((EPH->p_vaddr)), 
							  (size_t)((EPH->p_memsz & ~(sysconf(_SC_PAGE_SIZE) - 1)) + 
									   (sysconf(_SC_PAGE_SIZE) * ((EPH->p_memsz & ~(sysconf(_SC_PAGE_SIZE) - 1))==0))), 
							  PROT_EXEC|PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED, fd, 
							  EPH->p_offset);

          printf("Results, we got: we wanted to have prog at 0x%x and got 0x%x and error code %d\n", 
				 EPH->p_vaddr, pa, errno);
		}
	}
  
  if (close(fd))
	{
	  fprintf(stderr, "Cannot close file\n");
	  return 1;
	}

  printf("Starting at 0x%x\n\n", EH->e_entry);

  int (*function_main)(int argc, char *argv[]) = EH->e_entry;
  int result = (*function_main) (0, 0);  
  printf("%d!", result);
  
  return 0;
}



