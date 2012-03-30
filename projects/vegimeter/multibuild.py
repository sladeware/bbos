#!/usr/bin/env python

import os
import time

from bb.utils import module
from bb.tools import propler
from bb.builder.projects import CProject
from bb.builder.compilers import PropGCCCompiler

#propler.Image.dump_file_header("/home/d2rk/Workspace/bionicbunny/trunk/bb/tools/propler/tests/special.binary")
#exit(0)

def create_propgcc_project():
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
    6: ui_instance,
    4: buttons_driver_instance,
}

for image_id, handler in cogid_to_instance_mapping.items():
    image = create_propgcc_project()
    handler(image)
    script_fname = "%s_script.ld" % image.get_name()
    propler.gen_ld_script.generate(script_fname,
                           dict(HUB_START_ADDRESS=start_addr))
    compiler = image.get_compiler()
    compiler.define_macro("__linux__")
    compiler.define_macro("BB_HAS_STDINT_H")
    compiler.set_extra_preopts(["-Os", "-Wall"])
    linker = compiler.get_linker()
    linker.add_opts(["-Wl,-T" + script_fname])

    image.build(verbose=True)
    cogid_to_addr_mapping[image_id] = start_addr
    start_addr += propler.Image.get_file_size(image.get_output_filename())
    cogid_to_filename_mapping[image_id] = image.get_output_filename()

    #raw_input()

config = propler.DemoBoardConfig() #QuickStartBoardConfig()

#print "Uploading bootloader"
#uploader = propler.upload_bootloader('/dev/ttyUSB0', config)
# Very important! Let bootloader to settle!
#time.sleep(7)

print "Uploading images"
propler.multicog_spi_upload(cogid_to_filename_mapping,
                            '/dev/ttyUSB0')#uploader.serial.port)
propler.terminal_mode()
