import numpy as np
import random
import math
from collections import deque
from copy import deepcopy

class Environment():
    def __init__(self):
        pass

class State():
    def __init__(self):
        # This can be exchanged with time later
        self.init_state()

    def init_state(self):
        self.state = random_features_generator({
            "music" : 0,
            "route" : 0,
            "step" : 0,
        })
        return self.state

    def get_state_copy(self):
        return deepcopy(self.state)

    def update_state_with_action(self, action):
        self.state['step'] = self.state['step'] + 1
        if (action >= 0 and action < 3):
            self.state['music'] = action

        if (action >= 3 and action < 6):
            self.state['route'] = action - 3
        return self.get_state_copy()

    def compute_reward(self, actionid):
        action = action_def[actionid]
        profiles = [
            {0: 'music_A', 1: 'route_A', 2: 'route_B', 3: 'route_A', 4: 'no_music'},
            {0: 'music_B', 1: 'route_A', 2: 'route_B', 3: 'route_A', 4: 'no_music'},
            {0: 'route_A', 1: 'route_B', 2: 'route_A', 3: 'route_B', 4: 'no_music'},
            {0: 'music_A', 1: 'route_B', 2: 'route_A', 3: 'route_B', 4: 'no_music'},
        ]

        if self.state['female'] == 1:
            if self.state['age'] < 50:
                return int(action==profiles[0][self.state['step']])
            else:
                return int(action==profiles[1][self.state['step']])
        else:
            if self.state['age'] < 50:
                return int(action==profiles[2][self.state['step']])
            else:
                return int(action==profiles[3][self.state['step']])

action_def = {
    0: 'no_music',
    1: 'music_A',
    2: 'music_B',
    3: 'no_route',
    4: 'route_A',
    5: 'route_B'
}
feature_def = {
        'female': {'min': 0, 'max': 1},
        'age': {'min': 18, 'max': 99},
        'has_sunglasses': {'min': 0, 'max': 1},
        'music': {'min': 0, 'max': 2},
        'step': {'min': 0, 'max': 4},
        'route': {'min': 0, 'max': 2}
        }
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


class QCartPoleSolver():
    def __init__(self, buckets=(2, 2, 2, 3, 5, 3,), n_episodes=20000, n_win_ticks=195, min_alpha=0.1, min_epsilon=0.1, gamma=1.0, ada_divisor=25, max_env_steps=None, quiet=False, monitor=False):
        self.buckets = buckets # down-scaling feature space to discrete range
        self.n_episodes = n_episodes # training episodes 
        #self.n_win_ticks = n_win_ticks # average ticks over 100 episodes required for win
        self.min_alpha = min_alpha # learning rate
        self.min_epsilon = min_epsilon # exploration rate
        self.gamma = gamma # discount factor
        self.ada_divisor = ada_divisor # only for development purposes
        self.quiet = quiet

        #self.env = gym.make('CartPole-v0')
        self.state = State()
        #if max_env_steps is not None: self.env._max_episode_steps = max_env_steps
        #if monitor: self.env = gym.wrappers.Monitor(self.env, 'tmp/cartpole-1', force=True) # record results for upload

        self.Q = np.zeros(self.buckets + ( len(action_def),))
        print(self.Q.shape)

    def discretize(self, obs):
        # upper_bounds = [self.env.observation_space.high[0], 0.5, self.env.observation_space.high[2], math.radians(50)]
        # lower_bounds = [self.env.observation_space.low[0], -0.5, self.env.observation_space.low[2], -math.radians(50)]
        # ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(obs))]
        # new_obs = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
        # new_obs = [min(self.buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        nobs = (obs['female'], #2
        int(obs['age']<50), #2
        obs['has_sunglasses'], #2
        obs['music'], #3
        obs['step'], #5
        obs['route'], #3
        )

        return nobs

    def choose_action(self, state, epsilon):
        return random.randint(0, len(action_def)-1) if (np.random.random() <= epsilon) else np.argmax(self.Q[state])

    def update_q(self, state_old, action, reward, state_new, alpha):
        sc = alpha * (reward + self.gamma * np.max(self.Q[state_new]) - self.Q[state_old][action])
        self.Q[state_old][(action)] += sc

    def get_epsilon(self, t):
        return max(self.min_epsilon, min(1, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def get_alpha(self, t):
        return max(self.min_alpha, min(1.0, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def run(self):
        scores = deque(maxlen=100)
        self.mean_scores = []
        for e in range(self.n_episodes):
            current_state = self.discretize(self.state.init_state())

            alpha = self.get_alpha(e)
            epsilon = self.get_epsilon(e)
            done = False
            i = 0
            
            while not done:
                # self.env.render()
                action = self.choose_action(current_state, epsilon)
                reward = self.state.compute_reward(action)
                done = self.state.state["step"] == 3
                obs = self.state.update_state_with_action(action)
                
                #obs, reward, done, _ = self.env.step(action)
                new_state = self.discretize(obs)
                self.update_q(current_state, action, reward, new_state, alpha)
                current_state = new_state
                i += reward

            scores.append(i)
            mean_score = np.mean(scores)
            self.mean_scores.append(mean_score)
            # if mean_score >= self.n_win_ticks and e >= 100:
            #     if not self.quiet: print('Ran {} episodes. Solved after {} trials ✔'.format(e, e - 100))
            #     return e - 100
            if e % 100 == 0 and not self.quiet:
                print('[Episode {}] - Mean survival time over last 100 episodes was {} ticks.'.format(e, mean_score))

            print(mean_score)

        if not self.quiet: print('Did not solve after {} episodes 😞'.format(e))
        return e


import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    solver = QCartPoleSolver()
    solver.run()

    series = pd.Series(solver.mean_scores)
    #print(series.describe())
    series.plot()
    plt.show()
    # gym.upload('tmp/cartpole-1', api_key='')