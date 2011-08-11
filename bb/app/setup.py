#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.builder.project import Wrapper

from bb.app import Application, Mapping

@Wrapper.bind("on_build", Application)
def _build_application(application, project):
    pass

@Wrapper.bind("on_add", Mapping)
def _build_process(process, project):
    project.add_source(process.get_kernel())
    project.add_source(process.get_hardware())
