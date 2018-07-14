from __future__ import print_function
from flask import Flask, request, abort, jsonify
from agent import Agent

app = Flask(__name__)
agent = Agent()

agent.revive()

@app.route('/')
def hello():
  return "Hello world!"

@app.route('/next_action')
def next_action():
  if request.args.get('female') is None: abort(400, "female missing")
  if request.args.get('age') is None: abort(400, "age missing")
  if request.args.get('music') is None: abort(400, "music missing")
  if request.args.get('route') is None: abort(400, "route missing")
  if request.args.get('has_sunglasses') is None: abort(400, "has_sunglasses missing")
  if request.args.get('step') is None: abort(400, "step missing")
  if request.args.get('happiness') is None: abort(400, "happiness missing")
  env = {
    'female': request.args.get('female', type=int),
    'age': request.args.get('age', type=int),
    'music': request.args.get('music', type=int),
    'route': request.args.get('route', type=int),
    'has_sunglasses': request.args.get('has_sunglasses', type=int),
    'step': request.args.get('step', type=int),
    'happiness': request.args.get('happiness', type=float)
  }
  action = agent.next_action(env) if (env.step <= 4) else 9
  return jsonify({
    'action': action,
    'env': env
  })

@app.route('/reward')
def reward():
  if request.args.get('happiness') is None: abort(400, "happiness missing")
  happiness = request.args.get('happiness', type=float)
  agent.rewardLastAction(happiness)
  return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
