from johannes_agent import JohannesAgent
from environment import Environment

import random

feature_def = {
    'gender': {'min': 0, 'max': 1},
    'age': {'min': 18, 'max': 99},
    'music_on': {'min': 0, 'max': 1},
    'has_sunglasses': {'min': 0, 'max': 1},
}

action_def = {
    0: 'music_A',
    1: 'music_B',
    2: 'route_A',
    3: 'route_B'
}


def random_features_generator(force_dict, seed=None):
    force_dict = {} if force_dict is None else force_dict
    env = {}

    if seed:
        random.seed(seed)

    for key in feature_def.keys():
        if key in force_dict.keys():
            env['key'] = force_dict[key]
        else:
            env[key] = random.randint(feature_def[key]['min'], feature_def[key]['max'])
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
