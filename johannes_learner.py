from johannes_agent import JohannesAgent
from reward_simulator import reward_simulator

class Learner:

    def __init__(self, simulation):
        self.simulation = simulation
        self.agent = JohannesAgent()



    def train(self):
        self.agent.fill_experience_buffer()
        self.reward_over_episode = []
        for e in self.agent.hyperparameters["EPISODES"]:
            state = self.simulation.reset()
            while True:
                action = self.agent.act(state)
                next_state, reward, done = self.simulation.step()

                self.reward_over_episode

