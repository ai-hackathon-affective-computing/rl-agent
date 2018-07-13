from __future__ import print_function
from sys import maxint


# PERSONAS

class Persona:

  def __init__(self, female, age, sunglasses):
    self.female = female
    self.age = age
    self.sunglasses = sunglasses

  def distance_to_environment(self, env):
    return 10   * float(abs(env['female'] - self.female)) \
      +    0.2 * float(abs(env['age'] - self.age)) \
      +    1    * float(abs(env['sunglasses'] - self.sunglasses))

  def calculate_reward(self, env, action):
    return 0.0

  def __str__(self):
    return str.format("female: {}, age: {}, sunglasses: {}", self.female, self.age, self.sunglasses)


personas = [
  Persona(1, 30, 1),
  Persona(1, 55, 0)
]

def simulate_reward(env, action):
  persona = sorted(personas, key=lambda persona: persona.distance_to_environment(env))[0]
  print(persona)
  return persona.calculate_reward(env, action)


simulate_reward({
  'female': 1,
  'age': 35,
  'sunglasses': 0
}, 'MUSIC')
