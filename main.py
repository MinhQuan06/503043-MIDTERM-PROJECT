import argparse
from pathlib import Path
from time import perf_counter

from core.problem import SokobanProblem
from core.search import solve


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve a Sokoban map with UCS or A*.")
    parser.add_argument("map", nargs="?", type=Path, default=Path("maps/example_map.txt"))
    parser.add_argument("--algorithm", "-a", choices=("ucs", "astar"), default="astar")
    parser.add_argument("--gui", action="store_true", help="launch the Pygame application")
    args = parser.parse_args()

    if args.gui:
        from gui.app import App

        App().run()
        return

    problem = SokobanProblem.from_file(args.map)
    started = perf_counter()
    actions, cost, metrics = solve(problem, args.algorithm)
    elapsed = perf_counter() - started

    print(f"Algorithm: {args.algorithm.upper()}")
    if actions is None:
        print("No solution found")
    else:
        print("Actions:", actions)
        print("Total cost:", cost)
    print(f"Expanded: {metrics.expanded}")
    print(f"Generated: {metrics.generated}")
    print(f"Frontier peak: {metrics.frontier_peak}")
    print(f"Time: {elapsed:.3f}s")

if __name__ == "__main__":
    main()
