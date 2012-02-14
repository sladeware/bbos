#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import os.path

from bb.builder.projects import CatalinaProject
from bb.builder.loaders import BSTLLoader
from bb.utils import module

BE_VERBOSE = True
LOAD_BINARY_FLAG = False # Do we need to use loader to load the binary?
HUM_RAM_SIZE = 32 * 1024

project = CatalinaProject("vegimeter", verbose=BE_VERBOSE)

# Let us setup catalina compiler first
compiler = project.get_compiler()
compiler.add_include_dirs([
  "/opt/catalina/include",
  "./../..",
  "."])

# Add required libraries
compiler.add_library("ci") # Use this when float output not required
#compiler.add_library("c")

# Definitions
for macro in (\
    # Load a PC terminal emulator HMI plugin with screen and keyboard support
    "PC",
    # Reduce some plugins in order to save as much cogs as we can :)
    "NO_MOUSE",
    "NO_KEYBOARD",
    #"NO_SCREEN",
    "NO_GRAPHICS",
    #"NO_HMI",
    ):
    compiler.define_macro(macro)
# Propeller Demo Board support
compiler.define_macro("DEMO")


# Add sources
for filename in ("./../../bb/os.c",
                 "./../../bb/os/drivers/gpio/button.c",
                 "./../../bb/os/drivers/gpio/lh1500.c",
                 "./../../bb/os/drivers/onewire/onewire_bus.c",
                 "./../../bb/os/drivers/onewire/slaves/ds18b20.c",
                 "./../../bb/os/kernel.c",
                 "./../../bb/os/kernel/schedulers/fcfsscheduler.c"):
    project.add_source(filename)
for filename in ("temp_sensor_driver_soil_a.c",
                 "temp_sensor_driver_soil_b.c",
                 "temp_sensor_driver_soil_c.c",
                 "temp_sensor_driver_soil_d.c",
                 "temp_sensor_driver_water.c",
                 "ui.c",
                 "controller.c",
                 "pump_driver.c",
                 "button_driver.c",
                 "heater_driver.c",
                 "main.c",):
    project.add_source(os.path.join(module.get_dir(), filename))

# Build the project
project.build(verbose=BE_VERBOSE)

image_size = os.path.getsize(project.output_filename)
if image_size > HUM_RAM_SIZE:
    print >>sys.stderr, "Too large image size: %d > %d" % (image_size, HUM_RAM_SIZE)

# Skip the last part if we do not need to load binary
if not LOAD_BINARY_FLAG:
    exit(0)

# Setup loader to load our binary
loader = BSTLLoader(verbose=BE_VERBOSE,
                    mode=BSTLLoader.Modes.RAM_ONLY,
                    device_filename="/dev/ttyUSB0")
project.set_loader(loader)

# Load the project binary
project.load()
