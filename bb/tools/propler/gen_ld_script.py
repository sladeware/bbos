#!/usr/bin/env python

"""Generate proper script for GNU linker (ld)."""

from string import Template

TEMPLATE_FNAME = "template_ld_script.ld"

DEFAULT_VARS = {
    "HUB_START_ADDRESS": 0,
    "HUB_LEN": 32 * 1024,
}

def gen_ld_script(output_fname, required_vars=dict()):
    fh = open(TEMPLATE_FNAME)
    template = Template(fh.read())
    fh.close()
    target_vars = DEFAULT_VARS
    target_vars.update(required_vars)
    output_fh = open(output_fname, "w")
    output_fh.write(template.safe_substitute(target_vars))
    output_fh.close()

if __name__ == "__main__":
    gen_ld_script("script.ld", dict(HUB_START_ADDRESS=1024))
