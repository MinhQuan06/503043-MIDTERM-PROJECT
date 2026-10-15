import unittest
from pathlib import Path

from core.problem import SokobanProblem
from core.search import solve


ROOT = Path(__file__).resolve().parents[1]


class SokobanSearchTests(unittest.TestCase):
    def test_ucs_and_astar_find_same_optimal_solution_cost(self):
        problem = SokobanProblem.from_file(ROOT / "maps" / "example_map.txt")
        ucs_actions, ucs_cost, _ = solve(problem, "ucs")
        astar_actions, astar_cost, _ = solve(problem, "astar")

        self.assertIsNotNone(ucs_actions)
        self.assertIsNotNone(astar_actions)
        self.assertEqual(ucs_cost, astar_cost)
        self.assertEqual(ucs_cost, 34)

    def test_astar_solution_reaches_goal(self):
        problem = SokobanProblem.from_file(ROOT / "maps" / "example_map.txt")
        actions, _, _ = solve(problem, "astar")
        state = problem.initial

        for action in actions:
            successors = {name: next_state for name, next_state, _ in problem.successors(state)}
            self.assertIn(action, successors)
            state = successors[action]

        self.assertTrue(problem.is_goal(state))


if __name__ == "__main__":
    unittest.main()
