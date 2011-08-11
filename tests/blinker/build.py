#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import sys

import bb.builder
from bb.builder.projects import CatalinaProject
from bb.builder.loaders import BSTLLoader

import module

from blinker import blinker

def build(project):
    project = CatalinaProject("Blinker", [blinker])
    for source_file in ('blinker.c',):
        project.add_source(module.get_file(__name__, source_file))
    # Setup compiler
    compiler = project.get_compiler()
    compiler.add_include_dir(module.get_dir())
    compiler.add_library('c')
    compiler.define_macro("SMALL")
    compiler.define_macro("LED", 18, c_symbol=True)
    # Build application
    project.build()

def load(project):
    project.set_loader(BSTLLoader())
    project.load()

if __name__=='__main__':
    bb.builder.config.parse_command_line()
    project = None
    # Build
    build(project)
    # Load
    if bb.builder.config.options.use_loader:
        load(project)
