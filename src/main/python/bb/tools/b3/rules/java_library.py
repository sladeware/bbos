from bb.tools.b3.rules.library import Library

class JavaLibrary(Library):

  properties = (("programming_language", "java"),)

  def __init__(self, target=None, name=None, srcs=[], deps=[], copts=[]):
    Library.__init__(self, target=target, name=name, srcs=srcs, deps=deps)
