from qpole import QCartPoleSolver

class Agent(object):

  def __init__(self):

    self.agent = QCartPoleSolver()
    self.agent.load()
    self.last_action = None

  def revive(self):
    self.agent.load()

  def next_action(self, env):
    state = self.agent.discretize(env)
    self.last_action = self.agent.choose_action(state, 0.0)
    return self.last_action

  def rewardLastAction(self, reward):
    return 0
    # self.last_action
