import random
from collections import deque

def generate_random_state(goal_state):
    """Tạo trạng thái ngẫu nhiên khả nghiệm bằng cách hoán đổi từ goal_state."""
    while True:
        # Bắt đầu từ goal_state
        state = [row[:] for row in goal_state]
        # Thực hiện 2-5 hoán đổi ngẫu nhiên
        num_swaps = random.randint(2, 5)
        for _ in range(num_swaps):
            # Chọn hai vị trí ngẫu nhiên
            i1, j1 = random.randint(0, 2), random.randint(0, 2)
            i2, j2 = random.randint(0, 2), random.randint(0, 2)
            # Hoán đổi
            state[i1][j1], state[i2][j2] = state[i2][j2], state[i1][j1]
        
        # Chuyển thành assignment để kiểm tra số hoán vị
        flat = [state[i][j] for i in range(3) for j in range(3)]
        assignment = {f'X{i+1}': flat[i] for i in range(9)}
        inversions = count_inversions(assignment)
        
        # Nếu số hoán vị chẵn, trả về trạng thái
        if inversions % 2 == 0:
            return state

def count_inversions(assignment):
    """Tính số hoán vị của trạng thái."""
    flat = [0] * 9
    for var, value in assignment.items():
        idx = int(var[1:]) - 1
        flat[idx] = value
    
    numbers = [num for num in flat if num != 0]
    inversions = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                inversions += 1
    return inversions

def is_violate_constrain(state, goal_state):
    """Kiểm tra xem trạng thái có vi phạm ràng buộc (khác goal_state) hay không."""
    return state != goal_state

def run_test_algorithm(goal_state):
    """Chạy kiểm tra với các trạng thái ngẫu nhiên khả nghiệm cho đến khi đạt mục tiêu."""
    visited = set()
    path = []
    step_info = []
    max_steps = 100

    while len(path) < max_steps:
        new_state = generate_random_state(goal_state)
        state_tuple = tuple(tuple(row) for row in new_state)
        if state_tuple in visited:
            continue
        
        visited.add(state_tuple)
        path.append(new_state)
        # Tính số hoán vị cho thông tin
        flat = [new_state[i][j] for i in range(3) for j in range(3)]
        assignment = {f'X{i+1}': flat[i] for i in range(9)}
        inversions = count_inversions(assignment)
        step_info.append(f"Thử trạng thái: {new_state}, Hoán vị: {inversions}")
        
        if not is_violate_constrain(new_state, goal_state):
            return path, step_info, len(path)
        
        if len(path) >= max_steps:
            return path, step_info, len(path)
    
    return path, step_info, len(path)