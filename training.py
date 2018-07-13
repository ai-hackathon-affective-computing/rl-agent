from johannes_agent import JohannesAgent
from reward_simulator.reward_simulator import simulate_reward
from copy import deepcopy
import random

feature_def = {
    'female': {'min': 0, 'max': 1},
    'age': {'min': 18, 'max': 99},
    'has_sunglasses': {'min': 0, 'max': 1},
    'music': {'min': 0, 'max': 3},
    'step': {'min': 0, 'max': 4},
    'route': {'min': 0, 'max': 3}
    # This can be exchanged with time later
}

action_def = {
    0: 'no_music',
    1: 'music_A',
    2: 'music_B',
    3: 'no_route',
    4: 'route_A',
    5: 'route_B'
}

n_steps = 5             # 0, 1 (15min), 2 (30min), 3 (45min), 4 (END)


def random_features_generator(force_dict, seed=None):
    force_dict = {} if force_dict is None else force_dict
    env = {}

    if seed:
        random.seed(seed)

    for key in feature_def.keys():
        if key in force_dict.keys():
            env[key] = force_dict[key]
        else:
            env[key] = random.randint(feature_def[key]['min'], feature_def[key]['max'])
    return env


def update_features(features, action):
    features['step'] = features['step'] + 1
    if (action >= 0 and action < 3):
        features['music'] = action

    if (action >= 3 and action < 6):
        features['route'] = action - 3

    return features


def explore(agent, n_episodes):
    agent.set_epsilon(1.0)

    for repetition in range(n_episodes):

        ### RESET ###
        music = 0
        route = 0
        step = 0
        features = random_features_generator({'music': music, 'route': route, 'step': step})

        ### STEP ###
        for step in range(n_steps):
            action = agent.act(features=features.values())
            reward = simulate_reward(features,  action_def[action])

            ### TODO fix update_features
            next_features = update_features(features, action)

            agent.remember((features.values(), action, reward, next_features.values(), (step == n_steps-1)))

            features = deepcopy(next_features)




        agent.learn()
        print('Episode {}'. format(repetition))
        reward = 0


def train(agent, n_episodes):
    reward_per_episodes = []

    for repetition in range(n_episodes):
        agent.set_epsilon(1.0 - (repetition/n_episodes))

        ### RESET ###
        music = 0
        route = 0
        step = 0
        features = random_features_generator({'music': music, 'route': route, 'step': step})
        reward_per_steps = []

        ### STEP ###
        for step in range(n_steps):
            action = agent.act(features=features.values())
            reward = simulate_reward(features,  action_def[action])
            last_features = features
            features = update_features(features, action)

            agent.remember((last_features.values(), action, reward, features.values(), (step == n_steps-1)))
            reward_per_steps.append(reward)



        #agent.learn()
        reward_per_episodes.append(reward_per_steps)
        print('Episode {} reached summed reward of {}'.format(repetition, sum(reward_per_steps)))

    return reward_per_episodes


def evaluate(agent, n_episodes):
    reward_per_episodes = []
    agent.set_epsilon(0.0)

    for repetition in range(n_episodes):

        ### RESET ###
        music = 0
        route = 0
        step = 0
        features = random_features_generator({'music': music, 'route': route, 'step': step})
        reward_per_steps = []

        ### STEP ###
        for step in range(n_steps):
            action = agent.act(features=features.values())
            reward = simulate_reward(features, action_def[action])
            features = update_features(features, action)

            reward_per_steps.append(reward)

        reward_per_episodes.append(reward_per_steps)
        print('Episode {} reached summed reward of {}'. format(repetition, sum(reward_per_steps)))

    return reward_per_episodes

import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

    agent = JohannesAgent(n_features=len(feature_def), n_actions=len(action_def))

    # Set epsilon to 1
    explore(agent, 1000)
    agent.learn()

    # Set epsilon to 1.0 to 0.0
    reward_per_episodes = train(agent, 1000)
    agent.save()

    series = pd.Series([sum(e) for e in reward_per_episodes])
    series.plot()
    plt.show()

    # Set epsilon to 0
    reward_per_episodes = evaluate(agent, 100)

    series = pd.Series([sum(e) for e in reward_per_episodes])
    series.plot()
    plt.show()


