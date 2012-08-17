#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

from vegimeter import vegimeter

import bb
from bb.application_build import Application

bb.Builder.rule(bb.application.get_mapping('Vegimeter').get_thread('UI'), {
    'PropellerToolchain' : {
      'srcs' : ('ui.c',)
      }
    })
bb.Builder.rule(bb.application.get_mapping('Vegimeter').get_thread('BUTTON_DRIVER'), {
    'PropellerToolchain' : {
      'srcs' : ('button_driver.c',)
      }
    })
bb.Builder.build(Application())

exit(0)

vegetable_plant_guard = appmanager.new_application([vegimeter])
#vegimeter.hardware.set_simulation_mode()
vegetable_plant_guard.add_device(vegimeter_device)

builder.get_config().parse_command_line()
builder.set_application(vegetable_plant_guard)
builder.build(toolchain_class=propgcc.PropGCCToolchain)

exit(0)

def create_image():
    image = CProject("image")
    compiler = PropGCCCompiler()
    image.set_compiler(compiler)

    for filename in ("./../../bb/os.c",
                     "./../../bb/os/drivers/processors/propeller_p8x32/delay.c",
                     "./../../bb/os/kernel.c",
                     #"./../../bb/os/kernel/schedulers/fcfsscheduler.c"
                     ):
        image.add_source(filename)
    compiler = image.get_compiler()
    compiler.add_include_dirs(["./../..", "."])
    return image

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
