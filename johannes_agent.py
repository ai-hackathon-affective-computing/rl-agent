class JohannesAgent(object):
    def __init__(
            self,
            n_features=10,
            n_actions=4,
    ):
        self.n_features = n_features
        self.n_actions = n_actions

    def act(self, features, reward, done):
        raise NotImplementedError

    def learn(self, list_obs_reward_tuples):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError
