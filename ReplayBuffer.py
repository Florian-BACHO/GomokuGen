from collections import deque
import numpy as np

class ReplayBuffer(deque):
    # maxsize = 0 is infinite replay buffer
    def __init__(self, maxsize=10000):
        super(ReplayBuffer, self).__init__(maxlen=maxsize)

    def __call__(self, sample_size):
        size = len(self)
        indices = np.random.choice(size, sample_size, replace=False)

        return [self[i] for i in indices]
