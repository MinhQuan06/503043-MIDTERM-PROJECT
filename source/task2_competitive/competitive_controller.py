import time

from .competitive_state import CompetitiveState
from .competitive_engine import CompetitiveEngine
from .agent1 import Agent1
from .agent2 import Agent2


class CompetitiveController:
    def __init__(self, map_path, max_turns):
        self.initial_state = CompetitiveState.from_file(map_path)
        self.max_turns = max_turns

        self.agent1 = Agent1()
        self.agent2 = Agent2()

        self.reset()

    def reset(self):
        self.engine = CompetitiveEngine(
            self.initial_state.clone(),
            self.max_turns
        )

        self.history = []
        self.states = [self.state.clone()]

    def previous_step(self):
        if self.state.turn == 0:
            return False
        self.engine.state = self.states[self.state.turn - 1].clone()
        self.engine.finished = False
        return True

    @property
    def state(self):
        return self.engine.state

    @property
    def finished(self):
        return self.engine.finished

    def _get_action(self, agent, snapshot):
        start = time.perf_counter()

        try:
            action = agent.choose_action(
                snapshot,
                time_limit=0.9
            )
        except Exception as error:
            print(
                f"Agent {agent.agent_id} error: {error}"
            )
            action = "WAIT"

        elapsed_ms = (
            time.perf_counter() - start
        ) * 1000

        if elapsed_ms > 1000:
            print(
                f"Agent {agent.agent_id} exceeded "
                f"time limit: {elapsed_ms:.2f} ms"
            )
            action = "WAIT"

        return action, elapsed_ms

    def step(self):
        if self.finished:
            raise RuntimeError(
                "The competitive game has finished."
            )

        # Replay recorded turns without asking the agents to decide again.
        if self.state.turn < len(self.history):
            report = self.history[self.state.turn]
            self.engine.state = self.states[self.state.turn + 1].clone()
            self.engine.finished = report["finished"]
            return report

        # Both agents receive the same initial state.
        snapshot = self.state.clone()

        action1, time1 = self._get_action(
            self.agent1,
            snapshot.clone()
        )

        action2, time2 = self._get_action(
            self.agent2,
            snapshot.clone()
        )

        # Apply both actions in one simultaneous turn.
        report = self.engine.step({
            1: action1,
            2: action2
        })

        report["decision_times_ms"] = {
            1: time1,
            2: time2
        }

        self.history.append(report)
        self.states.append(self.state.clone())

        return report
