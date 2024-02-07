import math
import brain
import random
import pygame
import config

class Player:
    def __init__(self):
        # Bird
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 15) # pasarea ilustrata ca fiind un dreptunghi
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255) # varietatea de culori in care sa faca
                                                                                                # un player / o pasare, pentru a ne da seama ca sunt
                                                                                                # playeri diferiti se aleg 3 valori random care sa fie
                                                                                                # atribuite pasarii
        self.vel = 0 # viteza
        self.score = 0
        self.generatia = 0
        self.flap = False # bataie din aripi (miscare pe axa Oy) este falsa
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3 # cele 3 input-uri (distanta pana la pipe-ul de sus, pana la cel de jos (axa Oy) si ultimul pana la cele 2 pipe uri (axa Ox))
        self.brain = brain.Brain(self.inputs)
        self.brain.genereaza_retea()

    # functia de desenare in fereasta de joc
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        window.blit(score_text, (10, 10))

        highscore_text = font.render(f"Highscore: {config.highscore}", True, (0, 0, 0))
        window.blit(highscore_text, (10, 50))

        generation_text = font.render(f"Gen: {self.generatia}", True, (0, 0, 0))
        window.blit(generation_text, (10, 90))

    def urmatoarea_generatie(self):
        children = [] # urmatorea generatie care va fi supusa incercarii

        # clona campionului se adauga in fiecare generatie
        for s in self.species:
            children.append(s.campion.cloneaza())
            children[-1].generatia = self.generatia

        # spatiile libere pentru copii sunt umplute
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for i in range(0, children_per_species):
                child = s.offspring()
                child.generatia = self.generatia
                children.append(child)

        while len(children) < self.size:
            child = self.species[0].offspring()
            child.generatia = self.generatia
            children.append(child)

        self.players = []
        for child in children:
            self.players.append(child)
        self.generatia += 1

    def coliziune_pamant(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def coliziune_cer(self):
        return bool(self.rect.y < 30)

    def coliziune_conducte(self):
        for pipe in config.pipes:
            return pygame.Rect.colliderect(self.rect, pipe.top_rect) or \
                   pygame.Rect.colliderect(self.rect, pipe.bottom_rect)

    def update(self, ground):
        if not (self.coliziune_pamant(ground) or self.coliziune_conducte()):
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.coliziune_cer():
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def cea_mai_apropiata_conducta():
        for p in config.pipes:
            if not p.passed:
                return p

    def look(self):
        if config.pipes:

            # linie pana la pipe ul de sus
            self.vision[0] = max(0, self.rect.center[1] - self.cea_mai_apropiata_conducta().top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].top_rect.bottom))

            # linie pentru centrul dintre cele doua pipe uri
            self.vision[1] = max(0, self.cea_mai_apropiata_conducta().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (config.pipes[0].x, self.rect.center[1]))

            # linie pana la pipe ul de jos
            self.vision[2] = max(0, self.cea_mai_apropiata_conducta().bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].bottom_rect.top))


    def think(self):
        #self.decision = random.uniform(0, 1) # pasarile iau decizie random daca sa zboare sau nu
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def cloneaza(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.cloneaza()
        clone.brain.genereaza_retea()
        return clone