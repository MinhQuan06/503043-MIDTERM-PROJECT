from dataclasses import dataclass


@dataclass(frozen=True)
class SearchMetrics:
    expanded: int
    generated: int
    frontier_peak: int
