from __future__ import print_function
from flask import Flask

server = Flask(__name__)

@server.route('/observe')
def obvserve():
  return "OK"

@server.route('/reset')
def reset():
  return "OK"
