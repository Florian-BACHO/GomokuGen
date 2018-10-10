from Genetic import *
from GomokuEnv import *
from NeuralNetwork import *
import sys
import resource

BOARD_SIZE = 20

POPULATION_SIZE = 50
NN_DESCRIPTOR = [BOARD_SIZE * BOARD_SIZE, 500, BOARD_SIZE * BOARD_SIZE]

if __name__ == "__main__":
    filename = None

    #nn = NeuralNetwork(NN_DESCRIPTOR, -1., 1.)
    while True:
        pass
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    env = GomokuEnv(BOARD_SIZE)
    learner = Genetic(env, POPULATION_SIZE, NN_DESCRIPTOR, filename=filename)

    while True:
        learner()
        if filename is not None:
            learner.save(filename)
        learner.showBestMatch()
