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
  if request.args.get('gender') is None: abort(400, "gender missing")
  if request.args.get('age') is None: abort(400, "age missing")
  if request.args.get('music_on') is None: abort(400, "music_on missing")
  if request.args.get('has_sunglasses') is None: abort(400, "has_sunglasses missing")
  if request.args.get('step') is None: abort(400, "step missing")
  if request.args.get('happiness') is None: abort(400, "happiness missing")
  env = {
    'gender': request.args.get('gender', type=int),
    'age': request.args.get('gender', type=int),
    'music_on': request.args.get('gender', type=int),
    'has_sunglasses': request.args.get('has_sunglasses', type=int),
    'step': request.args.get('step', type=int),
    'happiness': request.args.get('happiness', type=float)
  }
  action = agent.next_action(env)
  return jsonify({
    'action': action,
    'env': env
  })

@app.route('/observe')
def observe():
  if request.args.get('happiness') is None: abort(400, "happiness missing")
  happiness = request.args.get('happiness', type=float)
  agent.rewardLastAction(happiness)
  return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
