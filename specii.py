import operator
import random

class Species:
    def __init__(self, player):
        self.players = []
        self.average_fitness = 0
        self.threshold = 1.2
        self.players.append(player)
        self.benchmark_fitness = player.fitness
        self.benchmark_brain = player.brain.cloneaza()
        self.campion = player.cloneaza()
        self.staleness = 0

    def similaritate(self, brain):
        similaritate = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similaritate

    @staticmethod
    def weight_difference(brain_1, brain_2):
        total_weight_difference = 0
        for i in range(0, len(brain_1.conexiuni)):
            for j in range(0, len(brain_2.conexiuni)):
                if i == j:
                    total_weight_difference += abs(brain_1.conexiuni[i].weight -
                                                   brain_2.conexiuni[j].weight)
        return total_weight_difference

    def add_to_species(self, player):
        self.players.append(player)

    def sort_players_by_fitness(self):
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.players[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.players[0].fitness
            self.campion = self.players[0].cloneaza()
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        total_fitness = 0
        for p in self.players:
            total_fitness += p.fitness
        if self.players:
            self.average_fitness = int(total_fitness / len(self.players))
        else:
            self.average_fitness = 0

    def offspring(self):
        child = self.players[random.randint(1, len(self.players)) - 1].cloneaza()
        child.brain.muteaza()
        return child