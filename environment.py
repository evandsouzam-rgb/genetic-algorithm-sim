from dataclasses import dataclass

from vector import Vector2D


@dataclass
class Obstacle:
    x: float
    y: float
    w: float
    h: float

    def hits(self, p, r=0):
        return self.x - r <= p.x <= self.x + self.w + r and self.y - r <= p.y <= self.y + self.h + r


@dataclass
class Goal:
    pos: Vector2D
    radius: float

    def reached_by(self, p):
        return self.pos.distance_to(p) <= self.radius


class Environment:
    def __init__(self, width, height, start, goal, obstacles):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.obstacles = obstacles

    def collides(self, p, r=0):
        if p.x - r < 0 or p.x + r > self.width or p.y - r < 0 or p.y + r > self.height:
            return True
        return any(o.hits(p, r) for o in self.obstacles)
