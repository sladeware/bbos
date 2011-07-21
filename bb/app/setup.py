
from bb.builder.project import Wrapper

from bb.app import Application, Process

@Wrapper.bind("on_build", Application)
def _build_application(application, project):
    print 2

@Wrapper.bind("on_add", Process)
def _build_process(process, project):
    project.add_source(process.get_kernel())
    project.add_source(process.get_hardware())
    
