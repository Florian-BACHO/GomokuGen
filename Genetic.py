from NeuralNetwork import *
from ArgmaxActionSelector import *
import random

class Genetic:
    def __init__(self, environment, population_size, neurons_descriptor, \
                 init_min=-1., init_max=1., elit_rate=0.15, nb_cross_points=3, \
                 mutation_rate=0.01):
        self.env = environment
        self.init_min = init_min
        self.init_max = init_max
        self.elit_rate = elit_rate
        self.nb_cross_points = nb_cross_points
        self.mutation_rate = mutation_rate

        self.actionSelector = ArgmaxActionSelector()

        self.generation = 0
        self.population = [NeuralNetwork(neurons_descriptor, init_min, init_max) \
                           for _ in range(population_size)]
        self.scores = []

    def _resetScores(self):
        self.scores = [0. for _ in range(len(self.population))]

    def _evaluatePopulation(self):
        self._resetScores()

        for i in range(len(self.population)):
            self._evaluateIndiv(i)

    def _evaluateIndiv(self, indiv_idx):
        print("Evaluate", str(indiv_idx))
        for it in range(indiv_idx + 1, len(self.population)):
            score = self._match(indiv_idx, it)

            self.scores[indiv_idx] += 1. if score > 0. else 0.
            self.scores[it] += 1. if score < 0. else 0.
        print(self.scores)

    def _match(self, player1, player2):
        print("MATCH", str(player1), "vs" + str(player2))
        player1 = self.population[player1]
        player2 = self.population[player2]

        player1Char = random.choice(['O', 'X'])

        current = 'O'
        obs = self.env.reset()
        done = False

        while not done:
            if player1Char == current:
                out = player1.activate(obs)
            else:
                out = player2.activate(obs)
            action = self.actionSelector(out)
            obs, reward, done = self.env.step(current, action)
            self.env.render()
            if not done:
                current = 'X' if current == 'O' else 'O'

        return reward if current == player1Char else -reward
