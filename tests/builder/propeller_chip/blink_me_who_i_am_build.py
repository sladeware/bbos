#!/usr/bin/env python

from bb.builder.projects import CProject
from bb.builder.compilers import PropGCCCompiler
from bb.tools import propler
from bb.tools.propler import gen_ld_script

NR_IMAGES = 5

filenames = [None] * NR_IMAGES
addresses = [0] * NR_IMAGES
start_addr = 0

for i in range(NR_IMAGES):
    image_id = i + 1
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
    addresses[i] = start_addr
    start_addr += propler.get_image_size(image.get_output_filename())
    filenames[i] = image.get_output_filename()

print "Report"
print "==  ====================  =============  ======="
print "%2s  %20s  %13s  %7s" % ("ID", "IMAGE", "START ADDRESS", "SIZE")
print "==  ====================  =============  ======="
for i in range(NR_IMAGES):
    print "%2d  %20s  %13d  %7d" \
        % (i + 1, filenames[i], addresses[i],
           propler.get_image_size(filenames[i]))
