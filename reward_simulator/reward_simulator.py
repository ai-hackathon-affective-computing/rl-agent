from __future__ import print_function
from persona import Persona
import traits


personas = [
  Persona(
    'Hanna',
    1, 30, 1, [
      traits.needs_music,
      traits.prefers_genre('A'),
      traits.prefers_route('A')
    ]
  ),
  Persona(
    'Verena',
    1, 55, 0, [
      traits.needs_music,
      traits.prefers_genre('B'),
      traits.prefers_route('B')
    ]
  ),
  Persona(
    'Gerd',
    0, 60, 1, [
      traits.prefers_genre('B'),
      traits.prefers_route('A')
    ]
  ),
  Persona(
    'Fabian',
    0, 28, 0, [
      traits.needs_music,
      traits.prefers_genre('A'),
      traits.prefers_route('B')
    ]
  )
]


def simulate_reward(env, action):
  persona = sorted(personas, key=lambda persona: persona.distance_to_environment(env))[0]
  reward = persona.calculate_reward(env, action)
  print(str.format("{} rewards {} with {} in {}", persona.name, action, reward, env))
  return 0