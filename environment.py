from __future__ import print_function


class Environment(object):
  """State of environment"""

  def __init__(self, female, age, sunglasses, playsMusic):
    self.female = female          # bool
    self.age = age                # int
    self.sunglasses = sunglasses  # bool
    self.playsMusic = playsMusic  # bool
