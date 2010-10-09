/*
 * Inter-Thread Communication
 *
 * Message passing is the basic ITC mechanism in BBOS. It allows BBOS threads 
 * to communication via messages.
 *
 * All BBOS ITC is unbuffered. Unbuffered ITC reduces the amount of copying 
 * involved and is thus the key to high performance ITC.
 *
 * More communication mechanisms could be provided as well by developers.
 *
 * Copyright (c) ???? Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

void
bbos_itc_init()
{
  
}

