import random

from vector import Vector2D

MAX_FORCE = 0.4
MAX_SPEED = 5.0


class DNA:
    def __init__(self, genes):
        self.genes = genes

    @classmethod
    def new(cls, length):
        return cls([Vector2D.random(MAX_FORCE) for _ in range(length)])

    def copy(self):
        return DNA(list(self.genes))

    def crossover(self, other):
        a, b = [], []
        for g1, g2 in zip(self.genes, other.genes):
            if random.random() < 0.5:
                g1, g2 = g2, g1
            a.append(g1)
            b.append(g2)
        return DNA(a), DNA(b)

    def mutate(self, rate):
        for i in range(len(self.genes)):
            if random.random() < rate:
                self.genes[i] = Vector2D.random(MAX_FORCE)


class Agent:
    radius = 4

    def __init__(self, pos, dna):
        self.pos = pos
        self.vel = Vector2D(0, 0)
        self.dna = dna
        self.fitness = 0
        self.crashed = False
        self.done = False
        self.finish_tick = 0

    def update(self, tick, env):
        if self.crashed or self.done:
            return

        if env.goal.reached_by(self.pos):
            self.done = True
            self.finish_tick = tick
            return

        if tick < len(self.dna.genes):
            self.vel = (self.vel + self.dna.genes[tick]).limit(MAX_SPEED)
        self.pos = self.pos + self.vel

        if env.collides(self.pos, self.radius):
            self.crashed = True

    def score(self, env, lifespan):
        d = self.pos.distance_to(env.goal.pos)
        f = 1000 / (d + 1) ** 1.5
        if self.done:
            f += 2000 + 15 * (lifespan - self.finish_tick)
        elif self.crashed:
            f *= 0.1
        self.fitness = max(f, 0.0001)
        return self.fitness
