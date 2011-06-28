/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_CONFIG_H
#define __BBOS_CONFIG_H

/**
 * @file config.h
 * @brief BB Operating System config
 */

// Always goes first
#include <bbos.h>

// Hardware
#ifndef BBOS_PROCESSOR
#error "BBOS_PROCESSOR was not defined"
#endif
#define BBOS_FIND_PROCESSOR_FILE(filename) <bb/os/hardware/processors/BBOS_PROCESSOR/filename>

#endif
