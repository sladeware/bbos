#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.builder.project import Wrapper
from bb.os.hardware import Hardware

@Wrapper.bind("on_add", Hardware)
def _add_hardware(hardware, project):
    if hardware.is_processor_defined():
        processor = hardware.get_processor()
        project.add_source(processor)
