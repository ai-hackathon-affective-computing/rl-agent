from __future__ import print_function
from reward_simulator import simulate_reward

simulate_reward({
  'female': 1,
  'age': 35,
  'has_sunglasses': 0,
  'music_on': 1
}, 'music_A')

simulate_reward({
  'female': 0,
  'age': 60,
  'has_sunglasses': 0,
  'music_on': 1
}, 'route_B')
