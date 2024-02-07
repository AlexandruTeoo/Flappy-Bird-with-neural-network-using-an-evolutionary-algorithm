import nod
import conn
import random

class Brain:
    def __init__(self, intrari, clona=False):
        self.conexiuni = []
        self.noduri = []
        self.intrari = intrari
        self.retea = []
        self.layers = 2

        if not clona:
            # crearea nodurilor de input i0, i1 si i3
            for i in range(0, self.intrari):
                self.noduri.append(nod.Node(i))
                self.noduri[i].layer = 0
            #crearea nodului bias
            self.noduri.append(nod.Node(3))
            self.noduri[3].layer = 0
            #crearea iesirii
            self.noduri.append(nod.Node(4))
            self.noduri[4].layer = 1

            #crearea conexiunilor
            for i in range(0, 4):
                self.conexiuni.append(conn.Connection(self.noduri[i], self.noduri[4], random.uniform(-1, 1)))

    def noduri_conectate(self):
        for i in range(0, len(self.noduri)):
            self.noduri[i].conexiuni = []

        for i in range(0, len(self.conexiuni)):
            self.conexiuni[i].from_node.connections.append(self.conexiuni[i])

    def genereaza_retea(self):
        self.noduri_conectate()
        self.retea = []
        for j in range(0, self.layers):
            for i in range(0, len(self.noduri)):
                if self.noduri[i].layer == j:
                    self.retea.append(self.noduri[i])

    def feed_forward(self, vision):
        for i in range(0, self.intrari):
            self.noduri[i].output_value = vision[i]

        self.noduri[3].output_value = 1

        for i in range(0, len(self.retea)):
            self.retea[i].activate()

        # nodul iesire
        output_value = self.noduri[4].output_value

        # resetez valoarea nodurilor de input
        for i in range(0, len(self.noduri)):
            self.noduri[i].input_value = 0

        return output_value

    def cloneaza(self):
        clona = Brain(self.intrari, True)

        # clonez toate nodurile
        for n in self.noduri:
            clona.noduri.append(n.clone())

        # clonez toate conexiunile
        for c in self.conexiuni:
            clona.conexiuni.append(c.clone(clona.getNode(c.from_node.id), clona.getNode(c.to_node.id)))

        clona.layers = self.layers
        clona.noduri_conectate()
        return clona

    def getNode(self, id):
        for n in self.noduri:
            if n.id == id:
                return n

    # sanse de 80% ca o gena sa se muteze
    def muteaza(self):
        if random.uniform(0, 1) < 0.8:
            for i in range(0, len(self.conexiuni)):
                self.conexiuni[i].mutate_weight()