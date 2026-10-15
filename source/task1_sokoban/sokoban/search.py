from state import get_valid_actions, step, goal_check
# TODO: UCS + A* implementation (Requirement 2).
# docs/team-workflow.md mục 4.4: solve(initial_state, algorithm) -> list[str]
# algorithm chỉ nhận "UCS" hoặc "A*". Không có lời giải thì trả về [], không trả None, không để crash.

def solve(initial_state, algorithm):
    """
    Nhận state ban đầu và tên thuật toán, trả về danh sách action ('N','S','E','W')
    đi từ initial_state tới trạng thái đích (goal_check trả True).
    """
    if algorithm == "UCS":
        return ucs(initial_state)
    elif algorithm == "A*":
        return a_star(initial_state)
    return []

def ucs(initial_state):
    """
    TODO (Req 2): Uniform Cost Search.
    Trả về list action hoặc [] nếu không có lời giải.
    """
    return []  

def a_star(initial_state):
    """
    TODO (Req 2): A* dùng heuristic(state) từ heuristic.py.
    Trả về list action hoặc [] nếu không có lời giải.
    """
    return []