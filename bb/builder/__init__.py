#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The BB Builder (simply builder or BBB) provides an environment for
application development. It allows the application developer to map software to
computational resources and is a a key part of Bionic Bunny.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Alexander Sviridenko <oleks.sviridenko@gmail.com>"

import math
import multiprocessing
import optparse
import os
import random
import signal
import subprocess
import sys
import tempfile
import time

import bb
from bb.app.mapping import Mapping, verify_mapping
from bb import app
from bb import 
from bb.builder.toolchains import simulator
from bb.builder.configs import Config
from bb.os import os_factory

_config = Config()

# Captured application instance
_application = None

def get_config():
    global _config
    return _config

def set_application(application):
    global _application
    # TODO(team): verify application object
    _application = application

def get_application():
    global _application
    return _application

def stop():
    """Stop building application."""
    print "Stopping..."

def build(application=None, toolchain_class=None):
    """Start the application build process. Application will randomly pick
    mappings one by one with specified delay (see
    :func:`set_mappings_execution_interval`).

    .. note::

       The only one application can be executed per session.
    """
    if application:
        set_application(application)
    application = get_application()
    if not application:
        print "No application to be built"
        return

    print "Build application", application

    if not application.get_num_mappings():
        print "Nothing to build. Please, add at least one mapping "\
            "to this application."
        return
    # First of all, create an build order of mappings.
    build_order = range(application.get_num_mappings())
    random.shuffle(build_order)
    # Build mappings one by one by using build order. Track keyboard
    # interrupts and system exit.
    try:
        for i in build_order:
            mapping = application.get_mappings()[i]
            _build_mapping(mapping)
            # Check for delay. Sleep for some time before the
            # next mapping will be executed.
            time.sleep(_application.get_mappings_execution_interval())
        # Wait for each process
        for process in _processes:
            process.join()
    except KeyboardInterrupt, e:
        stop()
    except SystemExit, e:
        stop()

def _build_mapping(mapping):
    threads = mapping.get_threads()
    if not threads:
        print "Mapping", mapping, "doesn't have threads"
        return
    processor = mapping.hardware.get_processor()
    if not processor:
        print "Mapping", mapping, "doesn't connected to any processor"
        return
    cores = mapping.hardware.get_processor().get_cores()
    step = int(math.ceil(float(len(threads)) / float(len(cores))))
    threads_per_core = [threads[x : x + step] for x in xrange(0, len(threads), step)]
    for i in range(len(threads_per_core)):
        core = cores[i]
        os_class = os_factory(threads=threads_per_core[i])
        if mapping.hardware.is_simulation_mode():
            toolchain_class = simulator.SimulationToolchain
        if not toolchain_class:
            raise NotImplemented()
        print 'Build OS "', os_class, '" by using toolchain', toolchain_class.__name__
        toolchain = toolchain_class(sources=[os_class])
        toolchain.build(verbose=True)
