from keras.models import *
from keras.layers.core import Dense, Activation
from random import sample as rsample
import numpy as np
import random as rn
from copy import deepcopy
import datetime


class JohannesAgent(object):
    def __init__(self, n_features=10, n_actions=4, load_network=False, file=None):
        self.experience_buffer = []
        self.n_actions = n_actions
        self.hyperparameters = self.read_in_configuration_file()[0]["hyperparameters"]
        self.epsilon = self.hyperparameters["EPSILON"]
        self.n_features = n_features
        self.n_actions = n_actions
        if not load_network:
            self.value_model = self.build_network(n_features, n_actions)
            self.target_model = self.build_network(n_features, n_actions)
        else:
            self.value_model = self.load(file)
            self.target_model = self.load(file)
        self.counter = 0

    def act(self, features):
        if np.random.rand() <= self.epsilon:
            return rn.randint(0, self.n_actions - 1)
        else:
            act_values = self.target_model.predict(self.reshape_state(features))
            return np.argmax(act_values[0])

    def learn(self):
        if self.counter % 10 == 0:
            self.target_model.set_weights(self.value_model.get_weights())
            batch = self.create_batch()
            if batch is None:
                return
            for state, action, reward, next_state, done in batch:
                target = self.target_model.predict(self.reshape_state(state))
                if done:
                    target[0][action] = reward
                else:
                    a = self.value_model.predict(self.reshape_state(next_state))[0]
                    t = self.target_model.predict(self.reshape_state(next_state))[0]
                    target[0][action] = reward + self.hyperparameters["GAMMA"] * t[np.argmax(a)]
                self.value_model.fit(self.reshape_state(state), target, epochs=1, verbose=0)
                if self.epsilon > self.hyperparameters["EPSILON_MIN"]:
                    self.epsilon = max(self.hyperparameters["EPSILON_MIN"], self.epsilon * self.hyperparameters["EPSILON_DECAY"])
                self.counter += 1



    def build_network(self, n_features, n_actions):
        model = Sequential([
            Dense(16, input_dim=n_features),
            Activation("relu"),
            Dense(32),
            Activation("relu"),
            Dense(n_actions),
            Activation("linear")
        ])
        model.compile(loss='mean_squared_error', optimizer=optimizers.Adam(lr=self.hyperparameters["LEARNING_RATE"]))
        return model


    def create_batch(self):
        if len(self.experience_buffer) >= self.hyperparameters["EXP_BUFFER_SIZE"]:
            experiences = rsample(self.experience_buffer, self.hyperparameters["BATCH_SIZE"])
            return experiences
        return None


    def fill_experience_buffer(self):
        for i in range(self.hyperparameters["EXP_BUFFER_SIZE"]):
            state = self.simulation.reset()
            while True:
                action = self.act(state)
                next_state, reward, done, _ = self.simulation.step(action)
                self.remember(state, action, reward, next_state, done)
                state = deepcopy(next_state)
                if done:
                    break


    def remember(self, tuple):
        if len(self.experience_buffer) >= self.hyperparameters["EXP_BUFFER_SIZE"]:
            self.experience_buffer.pop(0)
        self.experience_buffer.append(tuple)

    def load(self, file):
        return load_model(file)

    def save(self):
        self.target_model.save('net_savings/net-' + str(datetime.datetime.now().time()).replace(':','.') + '-.h5')


    def reshape_state(self, features):
        return np.reshape(np.array(list(features)), (1,-1))


    def read_in_configuration_file(self):
        return yaml.load(open('parameters.yml'))

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon


if __name__ == "__main__":
    agent = JohannesAgent()
