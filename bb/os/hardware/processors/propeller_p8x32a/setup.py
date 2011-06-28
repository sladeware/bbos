
from bb.builder.project import Wrapper
from bb.builder.compilers import CCompiler
from bb.apps.utils.dir import script_relpath, script_dir
from bb.os.hardware.processors.propeller_p8x32a import PropellerP8X32A

@Wrapper.bind("on_add", PropellerP8X32A)
def _add_propeller_p8x32a(processor, project):
    for filename in ('delay.c',):
        project.add_source(script_relpath(filename))

@Wrapper.bind("on_build", PropellerP8X32A)
def _build_propeller_p8x32a(processor, project):
    if isinstance(project.get_compiler(), CCompiler):
        f = open(project.env['BBOS_H'], 'a')
        f.write("#define BBOS_PROCESSOR propeller_p8x32a\n\n")
        f.close()
