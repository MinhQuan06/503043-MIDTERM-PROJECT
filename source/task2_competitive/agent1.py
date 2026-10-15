import heapq
import itertools
import time

from .competitive_state import CompetitiveState


MOVES = {
    "North": (0, -1),
    "East": (1, 0),
    "South": (0, 1),
    "West": (-1, 0),
}


class Agent1:
    def __init__(self):
        self.agent_id = 1

    def heuristic(self, boxes, goals):
        """
        Estimate the distance from boxes to goals.
        """
        total = 0

        for bx, by in boxes:
            if (bx, by) in goals:
                continue

            distance = min(
                abs(bx - gx) + abs(by - gy)
                for gx, gy in goals
            )

            total += distance

        return total

    def get_successors(self, state, player, boxes):
        """
        Generate valid successor states.
        Agent 2 is treated as a static obstacle.
        """
        successors = []

        opponent = state.agents[2]

        for action, (dx, dy) in MOVES.items():
            target = (player[0] + dx, player[1] + dy)

            if not self.is_free(state, target):
                continue

            if target == opponent:
                continue

            new_boxes = set(boxes)

            if target in boxes:
                box_target = (
                    target[0] + dx,
                    target[1] + dy
                )

                if not self.is_free(state, box_target):
                    continue

                if box_target in boxes or box_target == opponent:
                    continue

                new_boxes.remove(target)
                new_boxes.add(box_target)

            successors.append((
                action,
                target,
                frozenset(new_boxes)
            ))

        return successors

    def is_free(self, state, position):
        x, y = position

        return (
            0 <= x < state.width
            and 0 <= y < state.height
            and position not in state.walls
        )

    def choose_action(self, state: CompetitiveState, time_limit=0.9):
        """
        Use A* to select the first action of a plan.
        Return WAIT if no suitable action is found.
        """
        start_time = time.perf_counter()

        start_player = state.agents[1]
        start_boxes = frozenset(state.boxes.keys())

        start = (start_player, start_boxes)

        counter = itertools.count()

        frontier = []

        heapq.heappush(
            frontier,
            (
                self.heuristic(start_boxes, state.goals),
                0,
                next(counter),
                start,
                None
            )
        )

        best_cost = {start: 0}

        best_action = "WAIT"
        best_heuristic = self.heuristic(
            start_boxes,
            state.goals
        )

        while frontier:
            if time.perf_counter() - start_time >= time_limit:
                break

            priority, cost, _, current, first_action = (
                heapq.heappop(frontier)
            )

            if cost != best_cost.get(current):
                continue

            player, boxes = current

            h = self.heuristic(boxes, state.goals)

            if h < best_heuristic:
                best_heuristic = h
                best_action = first_action or "WAIT"

            if all(box in state.goals for box in boxes):
                return first_action or "WAIT"

            for action, new_player, new_boxes in (
                self.get_successors(state, player, boxes)
            ):
                new_state = (new_player, new_boxes)
                new_cost = cost + 1

                if new_cost >= best_cost.get(
                    new_state, float("inf")
                ):
                    continue

                best_cost[new_state] = new_cost

                first = first_action or action

                new_priority = (
                    new_cost
                    + self.heuristic(new_boxes, state.goals)
                )

                heapq.heappush(
                    frontier,
                    (
                        new_priority,
                        new_cost,
                        next(counter),
                        new_state,
                        first
                    )
                )

        return best_action