import time
import tracemalloc

from core.problem import SokobanProblem
from core.search import solve


class GameController:
    def __init__(self, map_path, algorithm):
        self.problem = SokobanProblem.from_file(map_path)
        self.algorithm = self._normalize_algorithm(algorithm)

        self.actions = []
        self.states = [self.problem.initial]
        self.current_step = 0

        self.cost = None
        self.metrics = None
        self.solved = False
        self.execution_time = None
        self.peak_memory_mb = None

    @staticmethod
    def _normalize_algorithm(algorithm):
        name = algorithm.strip().lower()

        if name == "a*":
            return "astar"

        if name == "ucs":
            return "ucs"

        raise ValueError(f"Unsupported algorithm: {algorithm}")

    def solve(self):
        tracemalloc.start()
        start_time = time.perf_counter()

        try:
            actions, cost, metrics = solve(
                self.problem,
                self.algorithm
            )
        finally:
            self.execution_time = (
                time.perf_counter() - start_time
            )

            _, peak_memory = tracemalloc.get_traced_memory()
            self.peak_memory_mb = peak_memory / (1024 * 1024)

            tracemalloc.stop()

        self.cost = cost
        self.metrics = metrics
        self.current_step = 0
        self.states = [self.problem.initial]
        self.actions = []
        self.solved = actions is not None

        if not self.solved:
            return False

        self.actions = actions
        current_state = self.problem.initial

        for action in actions:
            successors = self.problem.successors(current_state)

            for next_action, next_state, _ in successors:
                if next_action == action:
                    current_state = next_state
                    self.states.append(current_state)
                    break
            else:
                raise ValueError(
                    f"Invalid solution action: {action}"
                )

        return True

    @property
    def total_actions(self):
        return len(self.actions)

    @property
    def current_state(self):
        return self.states[self.current_step]

    def next_step(self):
        if self.current_step < self.total_actions:
            self.current_step += 1
            return True
        return False

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            return True
        return False

    def reset(self):
        self.current_step = 0
