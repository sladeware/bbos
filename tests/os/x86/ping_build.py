#!/usr/bin/env python

import os.path

from bb.builder.projects import CProject
from bb.utils import module

project = CProject("ping", verbose=False)

compiler = project.get_compiler()
compiler.add_include_dirs(["./../../..", "."])
compiler.define_macro("BB_CONFIG_OS_H", '"ping_config.h"')

# Take the sources from the same folder
for filename in ("./../../../bb/os.c", "./../../../bb/os/kernel.c",
                 "./../../../bb/os/kernel/itc.c", "./../../../bb/mm/mempool.c",
                 "./../../../bb/os/kernel/schedulers/fcfsscheduler.c"):
  project.add_source(filename)
for filename in ("ping.c",):
  project.add_source(os.path.join(module.get_dir(), filename))

project.build()