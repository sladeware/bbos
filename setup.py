#!/usr/bin/env python
#
# http://www.bionicbunny.org/
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

from __future__ import print_function

# See http://peak.telecommunity.com/DevCenter/EasyInstall for details.
from bootstrap import use_setuptools

import setuptools.sandbox
import argparse
import os
import sys
import logging

HOME_DIR = os.path.dirname(os.path.realpath(__file__))

EMAIL = "info@bionicbunny.org"
URL = "http://www.bionicbunny.org/"

class Command(object):

  def run(self):
    raise NotImplementedError()

class Install(object):
  # setup.py install

  def __init__(self, subparsers):
    parser_install = subparsers.add_parser('install', help='Run installation process')
    parser_install.set_defaults(command=self)

  def run(self):
    # TODO: record still doesn't work. We need to generate record logs to remove
    # installed scripts automatically what uninstall command is called.
    setup_py(['develop', '--record=install.logs'])
    self._gen_default_user_config()

  def _gen_default_user_config(self):
    try:
      import bb.config
    except ImportError:
      print("Please install bb first", file=sys.stderr)
      sys.exit(0)
    bb.config.gen_default_user_config()
    bb.config.user_settings.set('bbos', 'homedir', HOME_DIR)
    bb.config.user_settings.set('b3', 'builddir', os.path.join(HOME_DIR, 'tmp'))
    bb.config.user_settings.write()

class Uninstall(object):
  # setup.py uninstall

  def __init__(self, subparsers):
    parser_uninstall = subparsers.add_parser('uninstall', help='Uninstall bb framework')
    parser_uninstall.set_defaults(command=self)

  def run(self):
    setup_py(['develop', '--uninstall'])

class Doc(Command):
  # setup.py doc

  def __init__(self, subparsers):
    Command.__init__(self)
    parser_doc = subparsers.add_parser('doc', help='Generate documentation')
    parser_doc.set_defaults(command=self)

  def run(self):
    setup_py(['build_sphinx', '--source-dir=src/doc/python', '--build-dir=doc/build', '-a'])

class Test(object):
  # setup.py test

  def __init__(self, subparsers):
    parser_test = subparsers.add_parser('test', help='Run tests')
    parser_test.set_defaults(command=self)

  def run(self):
    setup_py(['test'])

def setup_py(args):
  print(' '.join(['setup.py'] + args))
  setuptools.setup(
    name="bb",
    description="BB Framework",
    author="Bionic Bunny Team",
    author_email=EMAIL,
    url=URL,
    license="Apache",
    classifiers=[
      "License :: OSI Approved :: Apache Software License",
      "Development Status :: 2 - Pre-Alpha",
      "Operating System :: BBOS"
    ],
    install_requires=[
      "django",
      "distribute>=0.6.24",
      "networkx",
      "pyserial"
    ],
    packages=setuptools.find_packages("src/main/python"),
    package_dir={'': 'src/main/python'},
    scripts=["bin/b3"],
    test_suite="test.make_testsuite",
    # Pass setup arguments manually
    script_args=args,
  )

def _build_argparser():
  parser = argparse.ArgumentParser(description='BB setup.')
  subparsers = parser.add_subparsers()
  for cmd_class in (Doc, Install, Test, Uninstall):
    cmd = cmd_class(subparsers)
  return parser

def main():
  parser = _build_argparser()
  args = parser.parse_args()
  use_setuptools()
  args.command.run()

if __name__ == '__main__':
  main()
