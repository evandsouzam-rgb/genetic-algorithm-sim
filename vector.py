import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector2D:
    x: float
    y: float

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vector2D(self.x * k, self.y * k)

    def length(self):
        return math.hypot(self.x, self.y)

    def limit(self, max_len):
        n = self.length()
        if n > max_len:
            return self * (max_len / n)
        return self

    def distance_to(self, other):
        return (self - other).length()

    @staticmethod
    def random(max_len=1.0):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, max_len)
        return Vector2D(math.cos(angle) * r, math.sin(angle) * r)
