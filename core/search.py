import heapq
from itertools import count
from math import inf
from typing import Callable

from core.metrics import SearchMetrics
from core.problem import Action, SokobanProblem, State

Heuristic = Callable[[State], float]


def solve(problem: SokobanProblem, algorithm: str = "astar", heuristic: Heuristic | None = None):
    name = algorithm.lower()
    if name not in {"ucs", "astar"}:
        raise ValueError("algorithm must be 'ucs' or 'astar'")
    if name == "astar" and heuristic is None:
        from core.heuristic import make_heuristic

        heuristic = make_heuristic(problem)

    start = problem.initial
    tie_breaker = count()
    initial_h = heuristic(start) if name == "astar" else 0
    frontier = [(initial_h, 0, next(tie_breaker), start)]
    best_cost = {start: 0}
    parent: dict[State, tuple[State, Action] | None] = {start: None}
    expanded = generated = 0
    frontier_peak = 1

    while frontier:
        _, cost, _, state = heapq.heappop(frontier)
        if cost != best_cost.get(state):
            continue
        if problem.is_goal(state):
            actions: list[Action] = []
            cursor = state
            while parent[cursor] is not None:
                previous, action = parent[cursor]
                actions.append(action)
                cursor = previous
            actions.reverse()
            return actions, cost, SearchMetrics(expanded, generated, frontier_peak)

        expanded += 1
        for action, next_state, step_cost in problem.successors(state):
            generated += 1
            new_cost = cost + step_cost
            if new_cost >= best_cost.get(next_state, inf):
                continue
            estimate = heuristic(next_state) if name == "astar" else 0
            if estimate == inf:
                continue
            best_cost[next_state] = new_cost
            parent[next_state] = (state, action)
            heapq.heappush(frontier, (new_cost + estimate, new_cost, next(tie_breaker), next_state))
        frontier_peak = max(frontier_peak, len(frontier))

    return None, inf, SearchMetrics(expanded, generated, frontier_peak)


def ucs(problem: SokobanProblem):
    return solve(problem, "ucs")


def astar(problem: SokobanProblem, heuristic: Heuristic | None = None):
    return solve(problem, "astar", heuristic)
