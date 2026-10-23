import sys

try:
    import pygame
except ImportError:
    pygame = None

BG = (18, 20, 24)
GOAL = (0, 230, 118)
WALL = (239, 83, 80)
ALIVE = (70, 160, 255)
DEAD = (70, 70, 80)
WON = (0, 255, 150)


class Visualizer:
    def __init__(self, env, headless=False):
        self.env = env
        self.headless = headless or pygame is None
        if self.headless:
            return

        pygame.init()
        pygame.display.set_caption("genetic algorithm")
        self.screen = pygame.display.set_mode((env.width, env.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 14)

    def handle_events(self):
        if self.headless:
            return True
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return False
        return True

    def draw(self, pop, tick, avg, best, solved):
        if self.headless:
            sys.stdout.write(f"\rgen {pop.generation:3d}  tick {tick:3d}  "
                             f"best {best:8.2f}  avg {avg:8.2f}  solved {solved}/{pop.size}")
            sys.stdout.flush()
            return

        self.screen.fill(BG)

        g = self.env.goal
        pygame.draw.circle(self.screen, GOAL, (int(g.pos.x), int(g.pos.y)), g.radius)

        for o in self.env.obstacles:
            pygame.draw.rect(self.screen, WALL, (o.x, o.y, o.w, o.h))

        for a in pop.agents:
            color = WON if a.done else DEAD if a.crashed else ALIVE
            pygame.draw.circle(self.screen, color, (int(a.pos.x), int(a.pos.y)), a.radius)

        lines = [
            f"generation {pop.generation}",
            f"tick {tick}/{pop.lifespan}",
            f"solved {solved}/{pop.size}",
            f"best {best:.2f}",
            f"avg {avg:.2f}",
        ]
        for i, line in enumerate(lines):
            self.screen.blit(self.font.render(line, True, (240, 240, 240)), (12, 12 + i * 18))

        pygame.display.flip()
        self.clock.tick(600)

    def close(self):
        if not self.headless:
            pygame.quit()
        print()
