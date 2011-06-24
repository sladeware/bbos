#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bb.builder.project import Wrapper
from bb.builder.compilers import CCompiler
from bb.os.kernel import Kernel

@Wrapper.bind("on_add", Kernel)
def _add_source(self, project):
    if isinstance(project.get_compiler(), CCompiler):
        project.add_sources(["system.c", "thread.c", "idle.c"])

