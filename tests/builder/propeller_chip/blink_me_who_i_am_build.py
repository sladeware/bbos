#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import time

from bb import builder
from bb.builder.projects import CProject
from bb.builder.compilers import PropGCCCompiler
from bb.tools import propler
from bb.tools.propler.boards import QuickStartBoardConfig, DemoBoardConfig

# List of cog identifiers on which the program will be run
TEST_COGS = [4, 6]

cogid_to_addr_mapping = dict()
cogid_to_filename_mapping = dict()
start_addr = 0

if __name__ == "__main__":
    builder.get_config().parse_command_line()
    # Build demo image for each tested cog
    for cog_id in TEST_COGS:
        image = CProject("blink_me_who_i_am%d" % cog_id)
        for filename in ("./../../../bb/os/drivers/processors/propeller_p8x32/sio.c",
                         "./../../../bb/os/drivers/processors/propeller_p8x32/delay.c",
                         "blink_me_who_i_am.c"):
            image.add_source(filename)            
        # Setup compiler
        compiler = image.set_compiler(PropGCCCompiler())
        compiler.define_macro("BB_CONFIG_OS_H", '"blink_me_who_i_am_config.h"')
        compiler.define_macro("__linux__")
        compiler.define_macro("BB_HAS_STDINT_H")
        compiler.add_include_dirs([".", "./../../../"])
        #compiler.define_macro("printf", "__simple_printf")
        compiler.set_memory_model("LMM")
        compiler.set_extra_preopts(["-Os", "-Wall"])
        # Setup linker
        linker = compiler.get_linker()
        script_fname = "script%d.ld" % cog_id
        propler.gen_ld_script.generate(script_fname,
                               dict(HUB_START_ADDRESS=start_addr))
        linker.add_opts(["-Wl,-T" + script_fname])
        # Build image
        image.build()
        cogid_to_addr_mapping[cog_id] = start_addr
        start_addr += propler.Image.get_file_size(image.get_output_filename())
        cogid_to_filename_mapping[cog_id] = image.get_output_filename()
    # Upload bootloader
    config = QuickStartBoardConfig()
    #propler.upload_bootloader('/dev/ttyUSB0', config)
    #time.sleep(7)
    propler.multicog_spi_upload(cogid_to_filename_mapping,
                                '/dev/ttyUSB0')
    propler.terminal_mode()
