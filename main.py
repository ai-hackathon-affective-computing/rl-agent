from __future__ import print_function
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
step = 0
should_reward_last_action = False

@app.route('/')
def hello():
  return "Hello world!"

@app.route('/next_action')
def next_action():
  if (step >= 4):
    abort(400, "End of simulation, please call /reset")
  if params.get('gender') is None: abort(400, "gender missing")
  if params.get('age') is None: abort(400, "age missing")
  if params.get('music_on') is None: abort(400, "music_on missing")
  if params.get('has_sunglasses') is None: abort(400, "has_sunglasses missing")
  env = {
    'gender': params.get('gender', type=int),
    'age': params.get('gender', type=int),
    'music_on': params.get('gender', type=int),
    'has_sunglasses': params.get('has_sunglasses', type=int),
    'step': step
  }
  action = 'MUSIC_A' # TODO: Get action
  should_reward_last_action = True
  step = += 1
  return jsonify({
    'action': action,
    'env': env
  })

@app.route('/observe')
def reward():
  if params.get('happiness') is None: abort(400, "happiness missing")
  happiness = params.get('happiness', type=float)
  if not should_reward_last_action:
    # TODO: Reward
    should_reward_last_action = true
  return "OK"

@app.route('/reset')
def reset():
  step = 0
  return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
