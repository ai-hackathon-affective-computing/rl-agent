from bmw_agent import bmwAgent

class Agent(object):

  def __init__(self):


    self.agent = bmwAgent()
    self.agent.load_q_table('q_savings/q_table-11.08.09.246167-.npy')
    self.last_action = None

  def revive(self):
    self.agent.load_q_table('q_savings/q_table-11.08.09.246167-.npy')

  def next_action(self, env):
    state = self.agent.discretize(env)
    self.last_action = self.agent.choose_action(state, 0.0)
    return self.last_action

  def rewardLastAction(self, reward):
    # self.last_action
    pass
