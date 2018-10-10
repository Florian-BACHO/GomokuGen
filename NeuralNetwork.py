import random

class NeuralNetwork:
    def __init__(self, layerDescriptor, init_min=-1., init_max=1., code=None, file=None):
        self.layerDescriptor = layerDescriptor
        if code is None and file is None:
            self._initNN(init_min, init_max)
        elif file is not None:
            self._load(file)
        else:
            self._setGeneticCode(code)

    # To handle sorting conflicts
    def __lt__(self, other):
        return self

    def _initNN(self, init_min, init_max):
        self.layers = []
        for currentLayer in range(len(self.layerDescriptor) - 1):
            layer = []
            nbWeights = self.layerDescriptor[currentLayer] + 1 # + 1 for the bias
            for neuron in range(self.layerDescriptor[currentLayer + 1]):
                layer.append([random.uniform(init_min, init_max) for i in \
                              range(nbWeights)])
            self.layers.append(layer)

    def save(self, file):
        for layer in self.layers:
            for neuron in layer:
                for weight in neuron:
                    file.write(str(weight) + "\n")

    def _load(self, file):
        self.layers = []
        for currentLayer in range(len(self.layerDescriptor) - 1):
            layer = []
            nbWeights = self.layerDescriptor[currentLayer] + 1 # + 1 for the bias
            for neuron in range(self.layerDescriptor[currentLayer + 1]):
                layer.append([float(file.readline()) for i in range(nbWeights)])
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

    def getGeneticCode(self):
        out = []
        for layer in self.layers:
            for neuron in layer:
                out.extend(neuron)
        return out

    def _setGeneticCode(self, code):
        idx = 0
        self.layers = []

        for currentLayer in range(len(self.layerDescriptor) - 1):
            layer = []
            nbWeights = self.layerDescriptor[currentLayer] + 1 # + 1 for the bias
            for neuron in range(self.layerDescriptor[currentLayer + 1]):
                layer.append(code[idx:idx + nbWeights])
                idx += nbWeights
            self.layers.append(layer)

    def leakyRelu(self, x):
        return (x) if (x > 0) else (0.01 * x)
