from NeuralNetwork import *
from ArgmaxActionSelector import *
import random
import os

class Genetic:
    def __init__(self, environment, population_size, neurons_descriptor, \
                 init_min=-1., init_max=1., elit_rate=0.15, nb_cross_points=3, \
                 mutation_rate=0.01, filename=None):
        self.env = environment
        self.neurons_descriptor = neurons_descriptor
        self.init_min = init_min
        self.init_max = init_max
        self.elit_nb = int(population_size * elit_rate)
        self.nb_cross_points = nb_cross_points
        self.mutation_rate = mutation_rate

        self.actionSelector = ArgmaxActionSelector()

        if filename is not None and os.path.isfile(filename):
            self._load(filename, population_size)
        else:
            self.generation = 0
            self.population = [NeuralNetwork(neurons_descriptor, init_min, init_max) \
                               for _ in range(population_size)]

        self.scores = []

    def __call__(self):
        print("Generation %d:" % (self.generation))
        self._evaluatePopulation()
        self.population = self._generateNewPopulation()
        self.generation += 1

    def showBestMatch(self):
        self._match(0, 1, True)

    def save(self, filename):
        file = open(filename, "w")

        file.write(str(self.generation) + "\n")

        for it in self.population:
            it.save(file)

        file.close()

    def _load(self, filename, population_size):
        file = open(filename, "r")

        self.generation = float(file.readline())
        self.population = [NeuralNetwork(self.neurons_descriptor, self.init_min, self.init_max, \
                                         file=file) for _ in range(population_size)]

        file.close()

    def _resetScores(self):
        self.scores = [0. for _ in range(len(self.population))]

    def _evaluatePopulation(self):
        self._resetScores()

        for i in range(len(self.population)):
            print("Evaluating indiv %d" % (i))
            self._evaluateIndiv(i)

        for i, it in enumerate(self.scores):
            print("Indiv %d: %d" % (i, it))
        print()

    def _evaluateIndiv(self, indiv_idx):
        for it in range(indiv_idx, len(self.population)):
            scoreIndiv, scoreIt = self._match(indiv_idx, it)

            self.scores[indiv_idx] += scoreIndiv
            self.scores[it] += scoreIt

    def _match(self, player1, player2, dump=False):
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
            obs, rewardCurrent, rewardAdvers, done = self.env.step(current, \
                                                                   'X' if current == 'O' else 'O', \
                                                                   action)
            if dump:
                self.env.render()
            if not done:
                current = 'X' if current == 'O' else 'O'

        return (rewardCurrent, rewardAdvers) if current == player1Char else \
            (rewardAdvers, rewardCurrent)

    def _generateNewPopulation(self):
        sortedPop = [it for _, it in sorted(list(zip(self.scores, self.population)), \
                                            reverse=True, key=lambda variable: variable[0])]
        total = sum(self.scores)
        sortedScores = [x / total for x in sorted(self.scores, reverse=True)]

        newPop = sortedPop[:self.elit_nb + 1]
        while len(newPop) < len(self.population):
            indiv1, indiv2 = self._generateIndiv(sortedPop, sortedScores)

            newPop.append(indiv1)
            if len(newPop) < len(self.population):
                newPop.append(indiv2)

        return newPop

    def _generateIndiv(self, sortedPop, sortedScores):
        indiv1 = self._selectIndiv(sortedPop, sortedScores)
        indiv2 = self._selectIndiv(sortedPop, sortedScores)

        indiv1Code = indiv1.getGeneticCode()
        indiv2Code = indiv2.getGeneticCode()

        for _ in range(self.nb_cross_points):
            indiv1Code, indiv2Code = self._crossingOver(indiv1Code, indiv2Code)
        indiv1Code = self._mutate(indiv1Code)
        indiv2Code = self._mutate(indiv2Code)

        return NeuralNetwork(self.neurons_descriptor, code = indiv1Code), \
            NeuralNetwork(self.neurons_descriptor, code = indiv2Code)

    def _selectIndiv(self, sortedPop, sortedScores):
        value = random.uniform(0., 1.)
        idx = 0
        total = sortedScores[0]

        while total < value:
            idx += 1
            total += sortedScores[idx]

        return sortedPop[idx]

    def _crossingOver(self, code1, code2):
        crossPoint = random.randint(0, len(code1) - 1)

        code11 = code1[:crossPoint]
        code12 = code1[crossPoint:len(code1) + 1]
        code21 = code2[:crossPoint]
        code22 = code2[crossPoint:len(code2) + 1]

        return code11 + code22, code21 + code12

    def _mutate(self, code):
        return [(random.uniform(self.init_min, self.init_max) \
                if random.uniform(0., 1.) < self.mutation_rate else it) \
                for it in code]
