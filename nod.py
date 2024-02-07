import math

class Node:
    def __init__(self, id_number):
        self.id = id_number
        self.layer = 0
        self.input_value = 0
        self.output_value = 0
        self.connections = []

    def activate(self): # functia de activare
        def sigmoid(x):
            return 1 / (1 + math.exp (-x))

        if self.layer == 1:
            self.output_value = sigmoid(self.input_value)

        for i in range (0, len (self.connections)):
            self.connections[i].to_node.input_value += \
                self.connections[i].weight * self.output_value

    def clone(self):
        clona = Node(self.id)
        clona.id = self.id
        clona.layer = self.layer
        return clona