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

# http://peak.telecommunity.com/DevCenter/EasyInstall
from bootstrap import use_setuptools

import setuptools.sandbox
import argparse
import os
import sys

HOME_DIR = os.path.dirname(os.path.realpath(__file__))

def _gen_default_user_config():
  try:
    import bb.config
  except ImportError:
    print("Please install bb first", file=sys.stderr)
    sys.exit(0)
  bb.config.gen_default_user_config()
  bb.config.user_settings.set("bbos", "homedir", HOME_DIR)
  bb.config.user_settings.write()

def setup_py(args):
  setuptools.setup(
    name="bb",
    description="BB Framework",
    author="Bionic Bunny Team",
    author_email="info@bionicbunny.org",
    url="http://www.bionicbunny.org/",
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
    test_suite="test.make_testsuite",
    # Pass setup arguments manually
    script_args = args,
  )

def build_doc():
  setup_py(['build_sphinx', '--source-dir=src/doc/python', '--build-dir=doc/build', '-a'])

def run_tests():
  setup_py(['test'])

def main():
  parser = argparse.ArgumentParser(description='BB setup.')
  subparsers = parser.add_subparsers()
  parser_doc = subparsers.add_parser('doc', help='Generate documentation')
  parser_doc.set_defaults(command='doc')
  parser_test = subparsers.add_parser('test', help='Run tests')
  parser_test.set_defaults(command='test')
  args = parser.parse_args()
  use_setuptools()
  if args.command == 'doc':
    build_doc()
    return
  elif args.command == 'test':
    run_tests()
    return
  setup_py(['develop'])
  #setup(
  #  scripts = ["bin/b3"],
  #  author_email = "info@bionicbunny.org",
  #  url = "http://www.bionicbunny.org/",
  #)
  _gen_default_user_config()

if __name__ == '__main__':
  main()
