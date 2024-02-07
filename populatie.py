import config
import player
import math
import specii
import operator

class Population:
    def __init__(self, size):
        self.players = []
        self.generatia = 1
        self.specii = []
        self.size = size
        for i in range(0, self.size):
            self.players.append(player.Player())

    def update_live_players(self):
        for player in self.players:
            if player.alive:
                player.look()
                player.think()
                player.draw(config.window)
                player.update(config.ground)

    def selectie_naturala(self):
        print ("Generatia " + str (self.generatia) + ":")
        print ("Selectia naturala a inceput")
        self.specia()
        self.calculate_fitness()
        self.omara_speciile_disparute()
        self.omoara_speciile_vechi()
        self.sort_species_by_fitness()
        self.next_gen()
        print ("Selectia naturala s-a terminat")

    def specia(self):
        for s in self.specii:
            s.players = []

        for player in self.players:
            add_to_species = False
            for s in self.specii:
                if s.similaritate(player.brain):
                    s.add_to_species(player)
                    add_to_species = True
                    break
            if not add_to_species:
                self.specii.append(specii.Species(player))

    def calculate_fitness(self):
        for player in self.players:
            player.calculate_fitness()
        for s in self.specii:
            s.calculate_average_fitness()

    def omara_speciile_disparute(self):
        species_bin = []
        for s in self.specii:
            if len(s.players) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.specii.remove(s)

    def omoara_speciile_vechi(self):
        player_bin = []
        species_bin = []
        for s in self.specii:
            if s.staleness >= 8:
                if len(self.specii) > len(species_bin) + 1:
                    species_bin.append(s)
                    for player in s.players:
                        player_bin.append(player)
                else:
                    s.staleness = 0
        for p in player_bin:
            self.players.remove(p)
        for s in species_bin:
            self.specii.remove(s)

    def sort_species_by_fitness(self):
        for s in self.specii:
            s.sort_players_by_fitness()

        self.specii.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        children = []

        # clona campionului este introdusa in fiecare specie
        for s in self.specii:
            children.append(s.campion.cloneaza())
            children[-1].generatia = self.generatia

        # umple spatiile goale din fiecare specie cu copii
        children_per_species = math.floor((self.size - len(self.specii)) / len(self.specii))
        for s in self.specii:
            for i in range(0, children_per_species):
                child = s.offspring()
                child.generatia = self.generatia
                children.append(child)

        while len(children) < self.size:
            child = self.specii[0].offspring()
            child.generatia = self.generatia
            children.append(child)

        self.players = []
        for child in children:
            self.players.append(child)
        self.generatia += 1

    # true daca toti playerii au murit
    def extinct(self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct