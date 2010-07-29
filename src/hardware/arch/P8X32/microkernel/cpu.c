/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <catalina_cog.h>

void
cpu_init()
{
  int cpu_id;

  cpu_id = _cogid();

  if (cpu_id >= ANY_COG) {
    printf("Unknown CPU configuration (ID %d), continuing anyway...\n", cpu_id);
    return;
  }

  printf("CPU #%d\n", cpu_id);
}



