from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

Position = tuple[int, int]
State = tuple[Position, frozenset[Position]]
Action = str

MOVES: dict[Action, Position] = {
    "North": (-1, 0),
    "East": (0, 1),
    "South": (1, 0),
    "West": (0, -1),
}


@dataclass(frozen=True)
class SokobanProblem:
    walls: frozenset[Position]
    goals: frozenset[Position]
    initial: State
    rows: int
    cols: int

    @classmethod
    def from_file(cls, path: str | Path) -> "SokobanProblem":
        map_path = Path(path)
        lines = [line.rstrip("\r\n") for line in map_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            raise ValueError(f"Map is empty: {map_path}")
        width = max(map(len, lines))
        lines = [line.ljust(width) for line in lines]
        walls: set[Position] = set()
        goals: set[Position] = set()
        boxes: set[Position] = set()
        agent: Position | None = None
        valid_symbols = {"%", "A", "B", "C", "D", " "}

        for row, line in enumerate(lines):
            for col, symbol in enumerate(line):
                position = (row, col)
                if symbol not in valid_symbols:
                    raise ValueError(f"Unknown map symbol {symbol!r} at {position}")
                if symbol == "%":
                    walls.add(position)
                elif symbol == "A":
                    if agent is not None:
                        raise ValueError("Map must contain exactly one agent")
                    agent = position
                elif symbol == "B":
                    boxes.add(position)
                elif symbol == "C":
                    boxes.add(position)
                    goals.add(position)
                elif symbol == "D":
                    goals.add(position)

        if agent is None:
            raise ValueError("Map does not contain an agent (A)")
        if not boxes or not goals:
            raise ValueError("Map must contain at least one box and one goal")
        if len(boxes) != len(goals):
            raise ValueError(f"Map has {len(boxes)} boxes but {len(goals)} goals")
        return cls(frozenset(walls), frozenset(goals), (agent, frozenset(boxes)), len(lines), width)

    def is_goal(self, state: State) -> bool:
        return state[1] == self.goals

    def successors(self, state: State) -> Iterator[tuple[Action, State, int]]:
        (row, col), boxes = state
        for action, (dr, dc) in MOVES.items():
            next_agent = (row + dr, col + dc)
            if not self._is_floor(next_agent):
                continue
            if next_agent in boxes:
                next_box = (next_agent[0] + dr, next_agent[1] + dc)
                if next_box in boxes or not self._is_floor(next_box):
                    continue
                next_boxes = frozenset((boxes - {next_agent}) | {next_box})
                yield action, (next_agent, next_boxes), 1
            else:
                yield action, (next_agent, boxes), 1

    def _is_floor(self, position: Position) -> bool:
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols and position not in self.walls
