import argparse
import csv

from environment import Environment, Goal, Obstacle
from population import Population
from vector import Vector2D
from visualizer import Visualizer


def make_env():
    start = Vector2D(400, 540)
    goal = Goal(Vector2D(400, 60), 24)
    walls = [
        Obstacle(200, 300, 400, 16),
        Obstacle(360, 180, 80, 16),
    ]
    return Environment(800, 600, start, goal, walls)


def run(generations, pop_size, lifespan, mutation_rate, headless, csv_output):
    env = make_env()
    pop = Population(pop_size, lifespan, env.start, mutation_rate)
    vis = Visualizer(env, headless)

    with open(csv_output, "w", newline="") as f:
        out = csv.writer(f)
        out.writerow(["generation", "avg_fitness", "peak_fitness", "successes", "success_rate"])

        avg, best, solved = 0, 0, 0
        try:
            for gen in range(generations):
                for tick in range(lifespan):
                    if not vis.handle_events():
                        return
                    pop.update(tick, env)
                    vis.draw(pop, tick, avg, best, solved)

                avg, best, solved = pop.evaluate(env)
                out.writerow([gen, f"{avg:.2f}", f"{best:.2f}", solved, f"{solved / pop_size:.4f}"])
                f.flush()
                pop.evolve()
        except KeyboardInterrupt:
            pass
        finally:
            vis.close()
            print(f"saved stats to {csv_output}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--generations", type=int, default=50)
    p.add_argument("--pop-size", type=int, default=100)
    p.add_argument("--lifespan", type=int, default=240)
    p.add_argument("--mutation-rate", type=float, default=0.015)
    p.add_argument("--headless", action="store_true", help="no window, just print progress")
    p.add_argument("--csv-output", default="ga_metrics.csv")
    run(**vars(p.parse_args()))
