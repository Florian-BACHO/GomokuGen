from Genetic import *
from GomokuEnv import *

BOARD_SIZE = 20

POPULATION_SIZE = 3
NN_DESCRIPTOR = [BOARD_SIZE * BOARD_SIZE, 256, 256, BOARD_SIZE]

if __name__ == "__main__":
    env = GomokuEnv(BOARD_SIZE)
    learner = Genetic(env, POPULATION_SIZE, NN_DESCRIPTOR)

    learner._evaluatePopulation()
