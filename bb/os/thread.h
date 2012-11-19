/*
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
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
#ifndef __BB_OS_THREAD_H
#define __BB_OS_THREAD_H

#define BBOS_ASSERT_THREAD_ID(id) BBOS_ASSERT((id) < BBOS_NUM_THREADS)

/* Thread identifier represents up to 255 threads. */
typedef uint8_t bbos_thread_id_t;

/* Thread execution data type. */
typedef void (*bbos_thread_runner_t)(void);

struct bbos_thread {
  bbos_thread_runner_t runner; /* Pointer to the target function to be called.*/
};
typedef struct bbos_thread bbos_thread_t;

#endif /* __BB_OS_THREAD_H */