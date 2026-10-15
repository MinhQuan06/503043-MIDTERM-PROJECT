from dataclasses import dataclass

# TODO: Sokoban state representation (agent, boxes, walls, targets).
# Design spec: see docs/formulation.md
# QUYỀN SỞ HỮU: file này do A (Track A) phụ trách.
# B: chỉ ĐỌC (import) các hàm/class ở đây để dùng trong search.py, không sửa trực tiếp.
# Cần đổi gì (vd thêm hàm so sánh state) thì nhắn A hoặc mở Pull Request.

@dataclass(frozen=True)
class State:
    agent: tuple
    boxes: frozenset
target = set()
walls = set()

def load_map(file_map: str) -> State:
    global target, walls
    target.clear()
    walls.clear()
    agent = None
    boxes = set()

    with open(file_map, "r") as f:
        for row, line in enumerate(f):
            line = line.rstrip('\n')
            for column, char in enumerate(line):
                pos = (row, column)

                if char == '%':
                    walls.add(pos)
                elif char == 'A':
                    agent = pos
                elif char in ('B', 'C'):
                    boxes.add(pos)
                    if char == 'C':
                        target.add(pos)
                elif char == 'D':
                    target.add(pos)

    print(f"Walls ({len(walls)} blocks):", walls)
    print(f"Target ({len(target)} blocks):", target)
    print(f"Boxes ({len(boxes)}):", boxes)
    print(f"Agent position: {agent}", agent)

    initial_state = State(agent=agent, boxes=frozenset(boxes))
    return initial_state

def goal_check(state: State) -> bool:
    return state.boxes == frozenset(target)

ACTIONS = {
    'N': (-1, 0), # North
    'S': (1, 0),  # South
    'W': (0, -1), # West
    'E': (0, 1)   # East
}

def step(state: State, action: str):
    x, y = ACTIONS[action]
    agent_x, agent_y = state.agent
    next_agent_pos = (x + agent_x, y + agent_y)

    if next_agent_pos in walls:
        return None

    if next_agent_pos in state.boxes:
        next_box = (next_agent_pos[0] + x, next_agent_pos[1] + y) # kiểm tra ô kế tiếp của box cùng với hướng đi của agent

        # Nếu ô đằng sau box là tường hoặc đã có box khác thì tức là bị kẹt, không đẩy được, di chuyển được
        if next_box in walls or next_box in state.boxes:
            return None

        # Nếu ổ đằng sau box trống, thì ta tạo 1 tập box mới để đẩy box, và cập nhật nó
        new_boxes = set(state.boxes)
        new_boxes.remove(next_agent_pos)  # Bỏ hộp ở vị trí của agent mới
        new_boxes.add(next_box)  # Thêm hộp vào vị trí mới

        # Trả về State mới chứa vị trí Agent mới và Tập Hộp mới
        return State(agent=next_agent_pos, boxes=frozenset(new_boxes))
    
    # Nếu là ô trống thì di chuyển Agent bình thường, trả về state có vị trí agent mới và tập box cũ
    return State(agent=next_agent_pos, boxes=state.boxes)
        
# Hàm này sẽ kiểm tra step của agent với mỗi hướng đi, nó gọi hàm step để kiểm tra xem đi hướng nào thì không trả về None
def get_valid_actions(state: State):
    valid_actions = []
    for action in ['N', 'S', 'W', 'E']:
        next_state = step(state, action)
        
        #Nếu hàm step trả về một State mới, nghĩa là hướng đi đó không đụng tường, không bị kẹt hộp
        if next_state is not None: 
            valid_actions.append(action)
    return valid_actions


