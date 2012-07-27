#!/usr/bin/env python

__author__ = "Oleksandr Sviridenko"

from bb.cli.config import Config

class CommandLineInterface(object):
  config = None

  def __init__(self):
    pass

CLI = CommandLineInterface
CLI.config = Config()
