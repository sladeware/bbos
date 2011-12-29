#!/usr/bin/env python

"""Projects:

  ================  =======================================
  Project           Class
  ================  =======================================
  Basic project     :class:`bb.builder.projects.project.Project`
  C project         :class:`bb.builder.projects.c.CProject`
  Catalina project  :class:`bb.builder.projects.catalina.CatalinaProject`
  ================  =======================================
"""

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.builder.projects.project import Project
from bb.builder.projects.c import CProject
from bb.builder.projects.catalina import CatalinaProject
