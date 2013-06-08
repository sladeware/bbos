#!/usr/bin/env python
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
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

import sys
# http://packages.python.org/distribute/setuptools.html
from setuptools import setup, find_packages

sys.path = ['/home/d2rk/workspace/bbos'] + sys.path

# Dynamically get the current version
#version = __import__("bb").__version__

def main():
  setup(
    name = "bb",
    description = "BB Framework",
    #version = version,
    author = "Bionic Bunny Team",
    author_email = "info@bionicbunny.org",
    url = "http://www.bionicbunny.org/",
    license = "Apache",
    classifiers = [
      "License :: OSI Approved :: Apache Software License",
      "Development Status :: 2 - Pre-Alpha",
      "Operating System :: BBOS"
    ],
    install_requires = [
      "django",
      "distribute>=0.6.24",
      "networkx",
      "pyserial"
    ],
    test_suite = "test.make_testsuite",
  )

if __name__ == "__main__":
  main()
