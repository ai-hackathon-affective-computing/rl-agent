import numpy as np
import random
import math
from collections import deque
from copy import deepcopy
import yaml
import datetime

class Environment():
    def __init__(self):
        pass

# Class which represents a state at each abstract tick the environment has
# State is represented as feature vector
class State():
    def __init__(self):
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
                return int(action == profiles[0][self.state['step']])
            else:
                return int(action == profiles[1][self.state['step']])
        else:
            if self.state['age'] < 50:
                return int(action == profiles[2][self.state['step']])
            else:
                return int(action == profiles[3][self.state['step']])

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


# Class for the Reinforcement Learning Agent using TD-Updates and Q-Learning
class bmwAgent():
    def __init__(self, buckets=(2, 2, 2, 3, 6, 3,), ada_divisor=25, quiet=False, max_q = False):
        self.hyperparameters = self.read_in_configuration_file()[0]["hyperparameters"]
        self.buckets = buckets # down-scaling feature space to discrete range
        self.n_episodes = self.hyperparameters["EPISODES"] # training episodes
        if max_q:
            self.n_episodes = 1
        self.min_alpha = self.hyperparameters["LEARNING_RATE"] # learning rate
        self.min_epsilon = self.hyperparameters["EPSILON_MIN"] # exploration rate
        self.gamma = self.hyperparameters["GAMMA"] # discount factor
        self.ada_divisor = ada_divisor # only for development purposes
        self.quiet = quiet
        self.epsilon = self.hyperparameters["EPSILON"]
        self.max_q = max_q
        self.state = State()
        self.Q = np.zeros(self.buckets + ( len(action_def),))
        print(self.Q.shape)

    # method to discretize states for building up correct q-table
    def discretize(self, obs):
        nobs = (obs['female'], #2
        int(obs['age']<50), #2
        obs['has_sunglasses'], #2
        obs['music'], #3
        obs['step'], #5
        obs['route'], #3
        )

        return nobs

    # method to save q-table
    def save_q_table(self, q_table):
        np.save('q_savings/q_table-' + str(datetime.datetime.now().time()).replace(':','.') + '-.npy', q_table)

    # method to load q-table
    def load_q_table(self, file):
        self.Q = np.load(file)

    # helper method to read in configuration file
    def read_in_configuration_file(self):
        return yaml.load(open('parameters.yml'))

    # chooses action regarding exploration - exploitation
    def choose_action(self, state, epsilon):
        return random.randint(0, len(action_def)-1) if (np.random.random() <= epsilon) else np.argmax(self.Q[state])

    # chooses best policies for testing agent
    def choose_max_actions(self, state):
        return np.argmax(self.Q[state])

    # method to do temporal difference updates
    def update_q(self, state_old, action, reward, state_new, alpha):
        sc = alpha * (reward + self.gamma * np.max(self.Q[state_new]) - self.Q[state_old][action])
        self.Q[state_old][action] += sc

    def get_epsilon(self, t):
        return max(self.min_epsilon, min(1, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def get_alpha(self, t):
        return max(self.min_alpha, min(1.0, 1.0 - math.log10((t + 1) / self.ada_divisor)))


    # Main learning/Testing loop for agent
    # Used Temporal Difference updates with one-step look-ahead and Q-Learning
    def run(self):
        scores = deque(maxlen=100)
        self.mean_scores = []
        for e in range(self.n_episodes):
            current_state = self.discretize(self.state.init_state())

            alpha = self.get_alpha(e)
            epsilon = self.get_epsilon(e)
            i = 0
            
            while True:
                if self.max_q:
                    action = self.choose_max_actions(current_state)
                else:
                    action = self.choose_action(current_state, epsilon)

                reward = self.state.compute_reward(action)
                done = self.state.state["step"] == 4
                obs = self.state.update_state_with_action(action)

                new_state = self.discretize(obs)
                if not self.max_q:
                    self.update_q(current_state, action, reward, new_state, alpha)
                current_state = new_state
                i += reward

                if done:
                    break

            scores.append(i)
            mean_score = np.mean(scores)
            self.mean_scores.append(mean_score)
            if e % 100 == 0 and not self.quiet:
                print('[Episode {}] - Mean survival time over last 100 episodes was {} ticks.'.format(e, mean_score))

            print(mean_score)

        return e


import pandas as pd
import matplotlib.pyplot as plt


#
if __name__ == "__main__":
    solver = bmwAgent(max_q=False)

    # Only needed if agent wants to be tested for max policy with saved q-table
    #solver.load_q_table('q_savings/q_table-10.18.15.925081-.npy')

    solver.run()
    #Only needed if q-table output of learning run should be saved
    #solver.save_q_table(solver.Q)

    series = pd.Series(solver.mean_scores)
    #print(series.describe())
    series.plot()
    plt.show()