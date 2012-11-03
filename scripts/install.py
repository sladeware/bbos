#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import os
import os.path
import shutil
import stat
import sys

def absjoin(*args):
  return os.path.abspath(os.path.join(*args))

BB_HOME_DIR = absjoin(os.path.dirname(os.path.realpath(__file__)), "..")
BB_PKG_DIR = absjoin(BB_HOME_DIR, "bb")
# Force python to use our package. We will need a few modules.
sys.path.append(BB_HOME_DIR)

import bb
import bb.host_os
import bb.install.requirements
from bb.tools.compilers import Python

def banner():
  return "\n".join([" ____  ____    ___           _        _ _ ",
                    "| __ )| __ )  |_ _|_ __  ___| |_ __ _| | |",
                    "|  _ \|  _ \   | || '_ \/ __| __/ _` | | |",
                    "| |_) | |_) |  | || | | \__ \  ||(_| | | |",
                    "|____/|____/  |___|_| |_|___/\__\__,_|_|_|",
                   ])

def _install_package():
  if not bb.host_os.path.exists(BB_PKG_DIR):
    print "Can not find bb package '%s'" % BB_PKG_DIR
    sys.exit(1)
  print "Creating a link to BB package..."
  # NOTE: on this moment we will only create a links
  libdest = Python.config["LIBDEST"]
  link_path = bb.host_os.path.join(libdest, "bb")
  if bb.host_os.path.exists(link_path) or bb.host_os.path.lexists(link_path):
    print "*", "remove old link `%s'" % link_path
    try:
      bb.host_os.unlink(link_path)
    except OSError, e:
      print "Please run as root. Not enough permissions."
      exit(1)
  print "*", "link `%s' -> `%s'" % (BB_PKG_DIR, link_path)
  os.symlink(BB_PKG_DIR, link_path)

def _install_scripts():
  # Create link to the BB script
  bindir = Python.config["BINDIR"]
  bb_script_path = "./scripts/bb.sh"
  bb_script_link_path = os.path.join(bindir, 'bb')
  print "Creating a link to BB script..."
  if bb.host_os.path.exists(bb_script_link_path) or \
        bb.host_os.path.lexists(bb_script_link_path):
    print "*", "remove old link `%s'" % bb_script_link_path
    os.unlink(bb_script_link_path)
  print "*", "copy `%s' to `%s'" % (bb_script_path, bb_script_link_path)
  shutil.copyfile(bb_script_path, bb_script_link_path)
  # Set mode
  os.chmod(bb_script_link_path, stat.S_IRGRP | stat.S_IROTH | \
             stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

def main():
  print banner()
  print
  print "Python version:", Python.get_version()
  print "OS:", bb.host_os.env['OS_NAME']
  bb.install.requirements.check_all()
  _install_package()
  _install_scripts()
  return 0

if __name__ == "__main__":
  sys.exit(main())
