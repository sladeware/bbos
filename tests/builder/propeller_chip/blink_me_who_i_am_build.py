#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import time

from bb.builder.projects import CProject
from bb.builder.compilers import PropGCCCompiler
from bb.tools import propler
from bb.tools.propler import gen_ld_script

target_cogs = [5, 7]

cogid_to_addr_mapping = dict()
cogid_to_filename_mapping = dict()
start_addr = 0

#propler.dump_header("blink_me_who_i_am5")
#propler.dump_header("blink_me_who_i_am7")
#img = propler.extract_image_from_file("blink_me_who_i_am5")
#propler.disasm_image(img)
#exit(0)

for image_id in target_cogs:
    script_fname = "script%d.ld" % image_id
    gen_ld_script.generate(script_fname,
                           dict(HUB_START_ADDRESS=start_addr,
                                HUB_LEN=(32*1024 + start_addr)))
    image = CProject("blink_me_who_i_am%d" % image_id)
    image.add_source("./../../../bb/os/drivers/processors/propeller_p8x32/sio.c")
    image.add_source("./../../../bb/os/drivers/processors/propeller_p8x32/delay.c")
    image.add_source("blink_me_who_i_am.c")

    # Setup compiler
    compiler = image.set_compiler(PropGCCCompiler())
    compiler.define_macro("__linux__")
    compiler.define_macro("BB_HAS_STDINT_H")
    compiler.add_include_dirs([".", "./../../../"])
    compiler.define_macro("printf", "__simple_printf")
    compiler.set_memory_model("lmm")
    compiler.set_extra_preopts(["-Os", "-Wall"])

    # Setup linker
    linker = compiler.get_linker()
    linker.add_opts(["-Wl,-T" + script_fname])

    # Build image
    image.build(verbose=False)
    cogid_to_addr_mapping[image_id] = start_addr
    start_addr += propler.Image.get_file_size(image.get_output_filename())
    cogid_to_filename_mapping[image_id] = image.get_output_filename()
    #propler.dump_header(image.get_output_filename())

#exit(0)

# Upload bootloader
from bb.tools.propler.config import QuickStartBoardConfig, DemoBoardConfig
config = QuickStartBoardConfig()
#propler.upload_bootloader('/dev/ttyUSB0', config)
#time.sleep(5)
propler.multicog_spi_upload(cogid_to_filename_mapping,
                            '/dev/ttyUSB0', force=True)#uploader.serial.port)

propler.terminal_mode()
