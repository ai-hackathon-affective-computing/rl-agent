from __future__ import print_function


def needs_music(persona, env, action):
  """The persona is unhappy if there is no music"""
  is_music_on = (env['music_on'] == 1) or 'music' in action
  return 0 if is_music_on else -0.5

def prefers_genre(genre):
  """The persona prefers a specific genre"""
  def fn(persona, env, action):
    if action.startswith('music_'):
      return 0.3 if action.endswith(genre) else -0.2
    else:
      return 0
  return fn

def prefers_route(route):
  """The persona prefers a specific route"""
  def fn(persona, env, action):
    if action.startswith('route_'):
      return 0.5 if action.endswith(route) else -0.4
    else:
      return 0
  return fn
