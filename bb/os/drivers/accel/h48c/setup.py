#!/usr/bin/env python

import module

from bb.builder.project import Wrapper
from bb.builder.compilers import CatalinaCompiler
from bb.os.hardware.drivers.accel.h48c import H48CDriver

@Wrapper.bind("on_add", H48CDriver)
def add_h48c_source(driver, project):
    if isinstance(project.get_compiler(), CatalinaCompiler):
        # temporary include spi_stamp here
        for filename in ("core.c","../../spi/spi_stamp.c"):
            project.add_source(module.get_file(__name__, filename))
