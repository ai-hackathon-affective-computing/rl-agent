from johannes_agent import JohannesAgent
from reward_simulator import simulate_reward

import random

feature_def = {
    'gender': {'min': 0, 'max': 1},
    'age': {'min': 18, 'max': 99},
    'has_sunglasses': {'min': 0, 'max': 1},
    'music_on': {'min': 0, 'max': 1},
    'step': {'min': 0, 'max': 1},               # This can be exchanged with time later
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


def update_features(features, step, is_music):
    features['step'] = step
    features['music_on'] = int(is_music)
    return features


if __name__ == '__main__':

    n_repetitions = 100
    n_steps = 5             # 0, 1 (15min), 2 (30min), 3 (45min), 4 (END)

    agent = JohannesAgent(n_features=len(feature_def), n_actions=4)
    reward_per_episodes = []

    for repetition in range(n_repetitions):

        ### RESET ###
        last_features = None
        reward = 0
        is_music = False
        features = random_features_generator({'music_on': int(is_music)})
        reward_per_steps = []

        ### STEP ###
        for step in range(n_steps):
            action = agent.act(features=features.values())
            last_features = features
            features = update_features(features, step, is_music)
            reward = simulate_reward(features, action)

            agent.remember((last_features.values(), action, reward, features.values(), (step == n_steps-1)))
            reward_per_steps.append(reward)

            if 'music' in action_def[action]:
                is_music = True

        agent.learn()
        reward_per_episodes.append(reward_per_steps)
        print('Episode {} reached summed reward of {}'. format(repetition, sum(reward_per_steps)))

    agent.save()
