from johannes_agent import JohannesAgent
from environment import Environment

from random import randint

feature_def = {
    'gender': {'min': 0, 'max': 1},
    'age': {'min': 18, 'max': 99},
    'music_on': {'min': 0, 'max': 1},
    'has_sunglasses': {'min': 0, 'max': 1},
}

action_def = {
    
}


def random_features_generator(seed=None):
    env = {}
    for key in feature_def.keys():
        env['key'] = randint(feature_def[key]['min'], feature_def[key]['max'])
    return env


if __name__ == '__main__':

    n_repetitions = 100

    agent = JohannesAgent(n_features=4, n_actions=4)
    environment = Environment()

    last_action = 0
    last_feature = None
    reward = 0

    for repetition in range(n_repetitions):
        features = random_features_generator()
        action = agent.act(features=features, reward=reward)

        reward = environment.simulate(features, action)
