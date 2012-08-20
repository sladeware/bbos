#!/usr/bin/env python

class Application(object):

  def __init__(self):
    self._images = []

  def add_image(self, image):
    self._images.append(image)

  def get_images(self):
    return self._images
