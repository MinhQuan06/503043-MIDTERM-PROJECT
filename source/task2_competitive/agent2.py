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


class Agent2:
    def __init__(self):
        self.agent_id = 2

    def heuristic(self, boxes, goals):
        """
        Estimate the total Manhattan distance
        from boxes to their nearest goals.
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

    def is_free(self, state, position):
        x, y = position

        return (
            0 <= x < state.width
            and 0 <= y < state.height
            and position not in state.walls
        )

    def get_successors(self, state, player, boxes):
        """
        Generate valid successor states.
        Agent 1 is treated as a static obstacle.
        """
        successors = []
        opponent = state.agents[1]

        for action, (dx, dy) in MOVES.items():
            target = (
                player[0] + dx,
                player[1] + dy
            )

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

                if box_target in boxes:
                    continue

                if box_target == opponent:
                    continue

                new_boxes.remove(target)
                new_boxes.add(box_target)

            successors.append((
                action,
                target,
                frozenset(new_boxes)
            ))

        return successors

    def choose_action(
        self,
        state: CompetitiveState,
        time_limit=0.9
    ):
        """
        Greedy Best-First Search.

        Returns the first action of the selected plan.
        """
        start_time = time.perf_counter()

        start_player = state.agents[2]
        start_boxes = frozenset(state.boxes.keys())

        start = (start_player, start_boxes)

        counter = itertools.count()

        frontier = []

        initial_h = self.heuristic(
            start_boxes,
            state.goals
        )

        heapq.heappush(
            frontier,
            (
                initial_h,
                next(counter),
                start,
                None
            )
        )

        visited = set()
        discovered = {start}

        best_action = "WAIT"
        best_heuristic = initial_h

        while frontier:
            if time.perf_counter() - start_time >= time_limit:
                break

            h, _, current, first_action = (
                heapq.heappop(frontier)
            )

            if current in visited:
                continue

            visited.add(current)

            player, boxes = current

            if h < best_heuristic:
                best_heuristic = h
                best_action = first_action or "WAIT"

            if all(box in state.goals for box in boxes):
                return first_action or "WAIT"

            successors = self.get_successors(
                state,
                player,
                boxes
            )

            for action, new_player, new_boxes in successors:
                new_state = (
                    new_player,
                    new_boxes
                )

                if new_state in discovered:
                    continue

                discovered.add(new_state)

                new_h = self.heuristic(
                    new_boxes,
                    state.goals
                )

                first = first_action or action

                heapq.heappush(
                    frontier,
                    (
                        new_h,
                        next(counter),
                        new_state,
                        first
                    )
                )

        return best_action