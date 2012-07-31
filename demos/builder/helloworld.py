#!/usr/bin/env python

import os.path

from bb.builder.projects import CProject
from bb.utils import module

project = CProject("helloworld", verbose=True)
# Take the sources from the same folder
sources = [os.path.join(module.get_dir(), _) for _ in ("helloworld.c",)]
project.add_sources(sources)
project.build()
