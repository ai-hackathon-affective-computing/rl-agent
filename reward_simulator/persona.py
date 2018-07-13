from __future__ import print_function
import math

try:
  from functools import reduce
except:
  pass

class Persona:
  """Wrapper class for a persona"""

  def __init__(self, name, female, age, has_sunglasses, traits):
    self.name = name
    self.female = female
    self.age = age
    self.has_sunglasses = has_sunglasses
    self.traits = traits

  def distance_to_environment(self, env):
    return 10   * float(abs(env['female'] - self.female)) \
      +    0.2 * float(abs(env['age'] - self.age)) \
      +    1    * float(abs(env['has_sunglasses'] - self.has_sunglasses))

  def calculate_reward(self, env, action):
    # reward = reduce(lambda result, trait: result + trait(self, env, action), self.traits, 0.5)
    if action == self.simplified(self.name)[env['step']]:
      return 1
    else:
      return 0
    # return min(max(reward, 0), 1)

  def __str__(self):
    return str.format("Persona {}", self.name)

  def simplified(self, name):
    if name == 'Hanna':
      return {0: 'music_A', 1: 'route_A', 2: 'route_B', 3: 'route_A', 4: 'no_music'}
    elif name == 'Verena':
      return {0: 'music_B', 1: 'route_A', 2: 'route_B', 3: 'route_A', 4: 'no_music'}
    elif name == 'Gerd':
      return {0: 'route_A', 1: 'route_B', 2: 'route_A', 3: 'route_B', 4: 'no_music'}
    else:
      return {0: 'music_A', 1: 'route_B', 2: 'route_A', 3: 'route_B', 4: 'no_music'}
