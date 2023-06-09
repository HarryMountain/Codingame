import ast
import json
import math
from copy import deepcopy

import numpy as np


class Neuron:
    def __init__(self, weights, bias, activation):
        self.weights = weights
        self.bias = bias
        self.activation = activation
        self.num_inputs = len(weights)
        self.inputs = np.zeros(self.num_inputs)
        self.Z = 0
        self.A = 0

    @staticmethod
    def sigmoid(x):
        # print(x)
        if x > 100:
            return 1
        if x < -100:
            return 0
        return 1 / (1 + math.exp(-x))

    def evaluate(self, inputs):
        self.inputs = inputs
        self.Z = np.dot(self.weights, inputs) + self.bias
        match self.activation:
            case 'sigmoid':
                self.A = self.sigmoid(self.Z)
            case 'relu':
                self.A = max(0, self.Z)
            case _:
                self.A = self.Z
        return self.A


class NeuralNetwork:
    def __init__(self, num_inputs, num_outputs, weights, biases, activations):
        self.num_inputs = num_inputs
        self.num_layers = len(weights)
        self.num_outputs = num_outputs
        self.neurons = []
        self.input_sizes = [num_inputs]
        for layer in range(self.num_layers):
            number_of_neurons = len(weights[layer][0])
            neuron_weights = [[weights[layer][j][i] for j in range(self.input_sizes[-1])] for i in range(number_of_neurons)]
            self.neurons.append([Neuron(neuron_weights[i], biases[layer][i], activations[layer]) for i in range(number_of_neurons)])
            self.input_sizes.append(number_of_neurons)

    def evaluate(self, inputs):
        network_data = [deepcopy(inputs)]
        for layer in range(self.num_layers):
            layer_outputs = []
            for neuron_idx in range(len(self.neurons[layer])):
                layer_outputs.append(self.neurons[layer][neuron_idx].evaluate(network_data[layer]))
            network_data.append(layer_outputs)
        return network_data[-1]

    def print_neuron_config(self):
        for layer in range(len(self.neurons)):
            print('\nLayer ' + str(layer) + ' weights:')
            for neuron in self.neurons[layer]:
                print(neuron.weights)
            print('\nLayer ' + str(layer) + ' biases:')
            print([neuron.bias for neuron in self.neurons[layer]])


# shape is [hidden_layer_1_size, ..., hidden_layer_N_size]
def create_nn_from_json(file_name):
    f = open(file_name)
    data = json.load(f)
    weights = []
    biases = []
    activations = []
    final_layer = max([int(key.split(' ')[1]) for key in data.keys() if 'Layer' in key])
    num_inputs = data['Layer 0']['batch_input_shape'][1]
    num_outputs = data['Layer ' + str(final_layer)]['units']
    for layer in range(final_layer + 1):
        layer_weights = ast.literal_eval(data['Weights ' + str(layer) + ':0'])
        layer_biases = ast.literal_eval(data['Weights ' + str(layer) + ':1'])
        weights.append(layer_weights)
        biases.append(layer_biases)
        activations.append(data['Layer ' + str(layer)]['activation'])

    nn = NeuralNetwork(num_inputs, num_outputs, weights, biases, activations)

    f.close()

    return nn
