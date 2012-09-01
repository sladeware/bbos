/*
 * Copyright (c) 2012 Sladeware LLC
 * Authro: Oleksandr Sviridenko
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_SHMEM_H
#define __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_SHMEM_H

#include <bb/os/config.h>

/* Reads and returns a byte from provided address of HUB RAM. */
int8_t shmem_read_byte(int32_t addr);

/*
 * Reads n bytes from HUB RAM address to the buffer. Caller has to manage
 * buffer memory.
 */
void shmem_read(int32_t addr, void* buf, size_t n);

/* Writes a byte to the HUB RAM. */
void shmem_write_byte(int32_t addr, int8_t byte);

/*
 * Writes n bytes to the HUB RAM.
 *
 * NOTE: a single long in the hub will be updated in one hub turn. Thus the
 * routine will use the locks, since we are updating a multi-long structure.
 */
void shmem_write(int32_t addr, void* buf, size_t n);

#endif /* __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_SHMEM_H */
