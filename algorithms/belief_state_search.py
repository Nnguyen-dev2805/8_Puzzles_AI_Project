# algorithms/belief_state_search.py
import time
from collections import deque
from algorithms.common import goalTest, getChildren, getStringRepresentation

class BeliefStateSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.actions = []  # Lưu chuỗi hành động

    def apply_action(self, belief_state, action):
        """Áp dụng một hành động cho tất cả trạng thái trong belief state"""
        new_belief_state = set()
        action_map = {
            "up": lambda state: self.move(state, -3),
            "down": lambda state: self.move(state, 3),
            "left": lambda state: self.move(state, -1),
            "right": lambda state: self.move(state, 1)
        }
        move_func = action_map[action]

        for state in belief_state:
            new_state = move_func(state)
            if new_state is not None:
                new_belief_state.add(new_state)
        return new_belief_state

    def move(self, state, offset):
        """Thực hiện di chuyển ô trống"""
        state_str = getStringRepresentation(state)
        zero_idx = state_str.index('0')
        new_idx = zero_idx + offset

        # Kiểm tra tính hợp lệ của di chuyển
        if offset == -3 and zero_idx >= 3:  # Up
            new_state = list(state_str)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            return int(''.join(new_state))
        elif offset == 3 and zero_idx <= 5:  # Down
            new_state = list(state_str)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            return int(''.join(new_state))
        elif offset == -1 and zero_idx % 3 > 0:  # Left
            new_state = list(state_str)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            return int(''.join(new_state))
        elif offset == 1 and zero_idx % 3 < 2:  # Right
            new_state = list(state_str)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            return int(''.join(new_state))
        return None  # Di chuyển không hợp lệ

    def BeliefStateSearch(self, inputState):
        """Thuật toán Belief State Search cho bài toán 8-puzzle"""
        start_time = time.time()
        initial_state = int(inputState)
        # Belief state ban đầu: Chỉ chứa trạng thái ban đầu
        belief_state = {initial_state}
        # Hàng đợi lưu (belief_state, actions) để tìm kiếm
        queue = deque([(belief_state, [])])
        visited = set()  # Theo dõi các belief states đã duyệt qua
        state_to_path = {initial_state: [initial_state]}  # Lưu đường đi cho trạng thái ban đầu

        while queue:
            self.counter += 1
            current_belief_state, actions = queue.popleft()

            # Chuyển belief state thành tuple để có thể thêm vào visited (set)
            belief_state_tuple = tuple(sorted(current_belief_state))
            if belief_state_tuple in visited:
                continue
            visited.add(belief_state_tuple)

            # Kiểm tra xem tất cả trạng thái trong belief state có phải là mục tiêu không
            all_goal = all(goalTest(state) for state in current_belief_state)
            if all_goal:
                # Tái tạo đường đi từ trạng thái ban đầu
                state = initial_state
                self.path = [state]
                for action in actions:
                    new_state = self.apply_action({state}, action)
                    state = next(iter(new_state))  # Lấy trạng thái duy nhất từ belief state
                    self.path.append(state)
                self.actions = actions
                self.cost = len(self.path) - 1
                self.depth = self.cost
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken

            # Thử tất cả các hành động có thể
            for action in ["up", "down", "left", "right"]:
                new_belief_state = self.apply_action(current_belief_state, action)
                if new_belief_state:  # Chỉ tiếp tục nếu có trạng thái mới
                    queue.append((new_belief_state, actions + [action]))

        # Nếu không tìm thấy giải pháp
        self.path = []
        self.actions = []       
        self.cost = 0
        self.depth = 0
        self.time_taken = float(time.time() - start_time)
        return self.path, self.cost, self.counter, self.depth, self.time_taken