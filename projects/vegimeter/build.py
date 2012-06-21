#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"

import os
import time

from bb.utils import module
from bb.tools import propler
from bb import builder
from bb.builder.projects import CProject
from bb.builder.compilers import PropGCCCompiler

def create_image():
    image = CProject("image")
    compiler = PropGCCCompiler()
    image.set_compiler(compiler)
    # At some point propgcc doesn't provide platform macro so we need to
    # define it manually
    compiler.define_macro("__linux__")
    compiler.define_macro("BB_HAS_STDINT_H")
    compiler.define_macro("printf", "__simple_printf")
    compiler.set_memory_model("LMM") # case insensetive
    compiler.set_extra_preopts(["-Os", "-Wall"])

    for filename in ("./../../bb/os.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/delay.c",
                     "./../../bb/os/kernel.c",
                     #"./../../bb/os/kernel/schedulers/fcfsscheduler.c"
                     ):
        image.add_source(filename)
    compiler = image.get_compiler()
    compiler.add_include_dirs(["./../..", "."])
    return image

def buttons_driver_image(image):
    compiler = image.get_compiler()
    compiler.define_macro("BB_CONFIG_OS_H", '"button_driver_config.h"')
    image.set_name("button_driver_image")
    for filename in ("./../../bb/os/drivers/gpio/button.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/shmem.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/sio.c",
                     "button_driver.c"):
        image.add_source(os.path.join(module.get_dir(), filename))

def ui_image(image):
    compiler = image.get_compiler()
    compiler.define_macro("BB_CONFIG_OS_H", '"ui_config.h"')
    image.set_name("ui_image")
    for filename in ("ui.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/shmem.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/sio.c",
                     ):
        image.add_source(os.path.join(module.get_dir(), filename))

cogid_to_addr_mapping = dict()
cogid_to_filename_mapping = dict()
start_addr = 0
cogid_to_instance_mapping = {
    6: ui_image,
    4: buttons_driver_image,
}

if __name__ == "__main__":
    builder.get_config().parse_command_line()

    for image_id, handler in cogid_to_instance_mapping.items():
        image = create_image()
        handler(image)
        script_fname = "%s_script.ld" % image.get_name()
        propler.gen_ld_script.generate(script_fname,
                                       dict(HUB_START_ADDRESS=start_addr))
        compiler = image.get_compiler()
        compiler.define_macro("__linux__")
        compiler.define_macro("BB_HAS_STDINT_H")
        compiler.set_extra_preopts(["-Os"]) # -Wall?
        linker = compiler.get_linker()
        linker.add_opts(["-Wl,-T" + script_fname])

        image.build(verbose=True)
        cogid_to_addr_mapping[image_id] = start_addr
        start_addr += propler.Image.get_file_size(image.get_output_filename())
        cogid_to_filename_mapping[image_id] = image.get_output_filename()

    board_config = propler.QuickStartBoardConfig()

    upload_bootloader = False

    if upload_bootloader:
        print "Uploading bootloader"
        uploader = propler.upload_bootloader("/dev/ttyUSB0", board_config)
        if not uploader:
            exit(0)
        # Very important! Let bootloader to settle!
        time.sleep(7)

    print "Uploading images"
    # We can also use uploader.serial.port instead of direct selection
    if propler.multicog_spi_upload(cogid_to_filename_mapping,
                                   "/dev/ttyUSB0", force=False): #uploader.serial.port
        propler.terminal_mode()
