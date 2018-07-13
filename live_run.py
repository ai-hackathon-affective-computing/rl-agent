from __future__ import print_function
from flask import Flask, request, abort, jsonify

server = Flask(__name__)


def get_env_from_params(params):
  if params.get('gender') is None: abort(400, "gender missing")
  if params.get('age') is None: abort(400, "age missing")
  if params.get('music_on') is None: abort(400, "music_on missing")
  if params.get('has_sunglasses') is None: abort(400, "has_sunglasses missing")
  return {
    'gender': params.get('gender', type=int),
    'age': params.get('gender', type=int),
    'music_on': params.get('gender', type=int),
    'has_sunglasses': params.get('has_sunglasses', type=int)
  }


@server.route('/observe')
def obvserve():
  env = get_env_from_params(request.args)
  return jsonify(env)

@server.route('/reset')
def reset():
  return "OK"
