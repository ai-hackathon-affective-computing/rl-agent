from __future__ import print_function
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
should_reward = False

@app.route('/')
def hello():
  return "Hello world!"

@app.route('/next_action')
def next_action():
  if params.get('step') is None: abort(400, "step missing")
  if params.get('gender') is None: abort(400, "gender missing")
  if params.get('age') is None: abort(400, "age missing")
  if params.get('music_on') is None: abort(400, "music_on missing")
  if params.get('has_sunglasses') is None: abort(400, "has_sunglasses missing")
  env = {
    'gender': params.get('gender', type=int),
    'age': params.get('gender', type=int),
    'music_on': params.get('gender', type=int),
    'has_sunglasses': params.get('has_sunglasses', type=int),
    'step': params.get('step', type=int)
  }
  action = 'MUSIC_A' # TODO: Get action
  should_reward = True
  return jsonify({
    'action': action,
    'env': env
  })

@app.route('/observe')
def observe():
  if params.get('happiness') is None: abort(400, "happiness missing")
  happiness = params.get('happiness', type=float)
  if should_reward:
    # TODO: Reward
    should_reward = False
  return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
