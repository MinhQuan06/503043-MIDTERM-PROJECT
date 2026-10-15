from collections import deque
from math import inf

from core.problem import MOVES, Position, SokobanProblem, State


def compute_push_distances(problem: SokobanProblem) -> dict[Position, int]:
    distances = {goal: 0 for goal in problem.goals}
    queue = deque(problem.goals)
    while queue:
        current = queue.popleft()
        for dr, dc in MOVES.values():
            previous_box = (current[0] - dr, current[1] - dc)
            agent_stand = (current[0] - 2 * dr, current[1] - 2 * dc)
            if previous_box in distances or not problem._is_floor(previous_box) or not problem._is_floor(agent_stand):
                continue
            distances[previous_box] = distances[current] + 1
            queue.append(previous_box)
    return distances


def make_heuristic(problem: SokobanProblem):
    push_distances = compute_push_distances(problem)

    def heuristic(state: State) -> float:
        total = 0
        for box in state[1]:
            distance = push_distances.get(box, inf)
            if distance == inf:
                return inf
            total += distance
        return total

    return heuristic
