#!/usr/bin/env python

import os
import time
from bb.utils import module
from bb.tools import propler
from bb.tools.propler import gen_ld_script

def create_propgcc_project():
    from bb.builder.projects import CProject
    from bb.builder.compilers import PropGCCCompiler
    project = CProject("vegimeter", verbose=True)
    compiler = PropGCCCompiler()
    project.set_compiler(compiler)
    # At some point propgcc doesn't provide platform macro so we need to
    # define it manually
    compiler.define_macro("__linux__")
    compiler.define_macro("BB_HAS_STDINT_H")
    compiler.define_macro("printf", "__simple_printf")
    compiler.set_memory_model("LMM") # case insensetive
    compiler.set_extra_preopts(["-Os", "-Wall"])
    return project

def setup_common_instance(project):
    for filename in ("./../../bb/os.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/delay.c",
                     "./../../bb/os/kernel.c",
                     #"./../../bb/os/kernel/schedulers/fcfsscheduler.c"
                     ):
        project.add_source(filename)
    compiler = project.get_compiler()
    compiler.add_include_dirs(["./../..", "."])

def buttons_driver_instance(project):
    compiler = project.get_compiler()
    compiler.define_macro("BB_CONFIG_OS_H", '"button_driver_config.h"')
    project.set_name("button_driver_instance")
    setup_common_instance(project)
    for filename in ("./../../bb/os/drivers/gpio/button.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/shmem.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/sio.c",
                     "button_driver.c"):
        project.add_source(os.path.join(module.get_dir(), filename))

def ui_instance(project):
    compiler = project.get_compiler()
    compiler.define_macro("BB_CONFIG_OS_H", '"ui_config.h"')
    project.set_name("ui_instance")
    setup_common_instance(project)
    for filename in ("ui.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/shmem.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/sio.c",
                     ):
        project.add_source(os.path.join(module.get_dir(), filename))

cogid_to_addr_mapping = dict()
cogid_to_filename_mapping = dict()
start_addr = 0
cogid_to_instance_mapping = {
    7: ui_instance,
    4: buttons_driver_instance,
}

for image_id, handler in cogid_to_instance_mapping.items():
    image = create_propgcc_project()
    handler(image)
    script_fname = "%s_script.ld" % image.get_name()
    gen_ld_script.generate(script_fname,
                           dict(HUB_START_ADDRESS=start_addr))
    compiler = image.get_compiler()
    compiler.define_macro("__linux__")
    compiler.define_macro("BB_HAS_STDINT_H")
    compiler.set_extra_preopts(["-Os", "-mlmm", "-Wall",
                                "-Wl,-T" + script_fname
                                ])

    image.build(verbose=True)
    cogid_to_addr_mapping[image_id] = start_addr
    start_addr += propler.get_image_file_size(image.get_output_filename())
    cogid_to_filename_mapping[image_id] = image.get_output_filename()

print "+-------------------------------------------------------------------+"
print "| %-65s |" % "Report"
print "+--------+--------------------------------+---------------+---------+"
print "| %6s | %30s | %13s | %7s |" \
    % ("COG ID", "IMAGE", "START ADDRESS", "SIZE")
print "+--------+--------------------------------+---------------+---------+"
total_size = 0
for i in cogid_to_instance_mapping.keys():
    sz = propler.get_image_file_size(cogid_to_filename_mapping[i])
    print "| %6d | %30s | %13d | %7d |" \
        % (i, cogid_to_filename_mapping[i], cogid_to_addr_mapping[i], sz)
    total_size += sz
print "+--------+--------------------------------+---------------+---------+"
print "  %55s | %7d |" % (" ", total_size)
print "                                                          +---------+"

#filename = cogid_to_filename_mapping[2]
#propler.dump_header(filename)

from bb.tools.propler.config import QuickStartBoardConfig, DemoBoardConfig
config = DemoBoardConfig() #QuickStartBoardConfig()

print "Uploading bootloader"
uploader = propler.upload_bootloader('/dev/ttyUSB0', config)

# Very important! Let bootloader to settle!
time.sleep(7)

print "Uploading images"
propler.multicog_spi_upload(cogid_to_filename_mapping,
                            '/dev/ttyUSB0')#uploader.serial.port)
propler.terminal_mode()
