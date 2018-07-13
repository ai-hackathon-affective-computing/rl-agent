from tensorforce.agents.dqn_agent import DQNAgent

class DQNAgent(object):

    def __init__(
            self,
            n_features,
            n_actions,
    ):
        self.agent = DQNAgent(
            states=n_features,
            actions=n_actions,
            network=None
        ).initialize_model()

    def load(self):
        self.agent.restore_model()

    def save(self):
        self.agent.save()

    def act(self, features, reward, done):
        self.agent.act(states=features, reward=reward, done=done)
