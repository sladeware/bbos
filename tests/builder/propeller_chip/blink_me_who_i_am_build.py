#!/usr/bin/env python

from bb.builder.projects import CProject
from bb.builder.compilers import PropGCCCompiler
from bb.tools import propler
from bb.tools.propler import gen_ld_script

target_cogs = [2, 4, 6, 8]

cogid_to_addr_mapping = dict()
cogid_to_filename_mapping = dict()
start_addr = 0

for image_id in target_cogs:
    script_fname = "script%d.ld" % image_id
    gen_ld_script.generate(script_fname,
                           dict(HUB_START_ADDRESS=start_addr))
    image = CProject("blink_me_who_i_am%d" % image_id)
    compiler = image.set_compiler(PropGCCCompiler())
    compiler.define_macro("__linux__")
    compiler.define_macro("BB_HAS_STDINT_H")
    compiler.set_extra_preopts(["-Os", "-mlmm", "-Wall",
                                "-Wl,-T" + script_fname])
    image.add_source("blink_me_who_i_am.c")
    image.build(verbose=True)
    cogid_to_addr_mapping[image_id] = start_addr
    start_addr += propler.get_image_file_size(image.get_output_filename())
    cogid_to_filename_mapping[image_id] = image.get_output_filename()

print "Report"
print "======  ====================  =============  ======="
print "%6s  %20s  %13s  %7s" % ("COG ID", "IMAGE", "START ADDRESS", "SIZE")
print "======  ====================  =============  ======="
for i in target_cogs:
    print "%6d  %20s  %13d  %7d" \
        % (i, cogid_to_filename_mapping[i], cogid_to_addr_mapping[i],
           propler.get_image_file_size(cogid_to_filename_mapping[i]))

# Upload bootloader
propler.upload_bootloader()

propler.multicog_spi_upload(cogid_to_filename_mapping, "/dev/ttyUSB0")
