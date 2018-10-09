import random

class NeuralNetwork:
    def __init__(self, layerDescriptor):
        self.layerDescriptor = layerDescriptor
        self.layers = []

        for currentLayer in range(len(layerDescriptor) - 1):
            layer = []
            nbWeights = layerDescriptor[currentLayer] + 1 # + 1 for the bias
            for neuron in range(layerDescriptor[currentLayer + 1]):
                layer.append([random.uniform(-1, 1) for i in range(nbWeights)])
            self.layers.append(layer)

    def activate(self, entries):
        assert len(entries) == self.layerDescriptor[0]
        for layer in self.layers:
            out = [self.activateNeuron(neuron, entries) for neuron in layer]
            entries = out
        return out

    def activateNeuron(self, weights, entries):
        preActivation = weights[0]

        for i in range(1, len(weights)):
            preActivation += weights[i] * entries[i - 1]

        return self.leakyRelu(preActivation)

    def leakyRelu(self, x):
        return (x) if (x > 0) else (0.01 * x)
