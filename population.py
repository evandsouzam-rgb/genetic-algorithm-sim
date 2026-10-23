import random

from agent import Agent, DNA


class Population:
    def __init__(self, size, lifespan, start, mutation_rate=0.015, elite_frac=0.04, tournament=4):
        self.size = size
        self.lifespan = lifespan
        self.start = start
        self.mutation_rate = mutation_rate
        self.n_elite = max(1, int(size * elite_frac))
        self.tournament = tournament
        self.generation = 0
        self.agents = [Agent(start, DNA.new(lifespan)) for _ in range(size)]

    def update(self, tick, env):
        for a in self.agents:
            a.update(tick, env)

    def evaluate(self, env):
        scores = [a.score(env, self.lifespan) for a in self.agents]
        solved = sum(a.done for a in self.agents)
        return sum(scores) / self.size, max(scores), solved

    def pick_parent(self):
        return max(random.sample(self.agents, self.tournament), key=lambda a: a.fitness)

    def evolve(self):
        best = sorted(self.agents, key=lambda a: a.fitness, reverse=True)
        next_gen = [Agent(self.start, a.dna.copy()) for a in best[:self.n_elite]]

        while len(next_gen) < self.size:
            c1, c2 = self.pick_parent().dna.crossover(self.pick_parent().dna)
            c1.mutate(self.mutation_rate)
            c2.mutate(self.mutation_rate)
            next_gen.append(Agent(self.start, c1))
            if len(next_gen) < self.size:
                next_gen.append(Agent(self.start, c2))

        self.agents = next_gen
        self.generation += 1
