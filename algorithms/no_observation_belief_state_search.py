import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class NoObservationBeliefStateSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_pq_size = 0  
        self.max_visited_size = 0  

    def _state_to_string(self, state_2d):
        """chuyển đổi trạng thái 2D thành chuỗi dạng"""
        flat = [str(num) for row in state_2d for num in row]
        return ''.join(flat)

    def _string_to_2d(self, state_str):
        """chuyển đổi chuỗi trạng thái thành trạng thái 2D."""
        nums = [int(c) for c in state_str]
        return [nums[i:i+3] for i in range(0, 9, 3)]
    
    def get_possible_actions(self, belief):
        """lấy tất cả hành động hợp lệ từ các trạng thái trong belief."""
        actions = set()
        for state in belief:
            idx = state.index("0")
            i, j = divmod(idx, 3)
            moves = [(-1, 0, "0"), (1, 0, "1"), (0, -1, "2"), (0, 1, "3")]
            for di, dj, action in moves:
                ni, nj = i + di, j + dj
                if 0 <= ni < 3 and 0 <= nj < 3:  # kiểm tra hợp lệ
                    actions.add(action)
        return list(actions)

    def transition(self, belief, action):
        """Áp dụng hành động cho tất cả trạng thái trong belief."""
        next_belief = set()
        for state in belief:
            children = getChildren(state)  # Danh sách trạng thái con
            idx = state.index("0")
            i, j = divmod(idx, 3)
            di, dj = {"0": (-1, 0), "1": (1, 0), "2": (0, -1), "3": (0, 1)}[action]
            ni, nj = i + di, j + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_index = ni * 3 + nj
                for child in children:
                    if child[new_index] == "0" and child[idx] == state[new_index]:
                        next_belief.add(child)
                        break
                else:
                    next_belief.add(state)
            else:
                next_belief.add(state)
        return next_belief

    def NoObsBeliefStateSearch(self, initial_belief_states, goal_belief_states, max_iterations=1000, time_limit=10):
        """
        initial_belief_states : Không gian niềm tin
        goal_belief_states : Không gian đích
        """
        
        start_time = time.perf_counter()

        initial_belief = {self._state_to_string(state) for state in initial_belief_states}
        goal_belief = {self._state_to_string(state) for state in goal_belief_states}

        def goal_test_belief(belief):
            """kiểm tra xem belief state có chứa toàn bộ và chỉ các trạng thái mục tiêu"""
            return set(belief) == set(goal_belief)
    

        # def transition(belief, action):
        #     """áp dụng hành động cho tất cả trạng thái trong belief"""
        #     next_belief = set()
        #     for state in belief:
        #         children = getChildren(state)  # danh sách các trạng thái con
        #         for child in children:
        #             next_belief.add(child)
        #     return next_belief

        def heuristic(belief):
            """Heuristic: trung bình khoảng cách Manhattan nhỏ nhất đến mục tiêu."""
            total = 0
            for state in belief:
                min_dist = manhattanDistance(int(state))  # manhattanDistance nhận int
                total += min_dist
            return total / len(belief) if belief else float('inf')

        # kiểm tra nếu belief ban đầu đã là mục tiêu
        if goal_test_belief(initial_belief):
            path = [[self._string_to_2d(state) for state in initial_belief]]
            self.time_taken = time.perf_counter() - start_time
            total_space = len(initial_belief)
            return path, 0, 0, 0, self.time_taken, total_space

        # Tìm kiếm A* trên không gian belief state
        pq = []  # (f_score, counter, belief, actions)
        visited = set()
        counter = 0
        h_score = heuristic(initial_belief)
        heapq.heappush(pq, (h_score, counter, initial_belief, []))
        counter += 1

        # while pq and time.perf_counter() - start_time < time_limit and counter < max_iterations:
        while pq :
            self.counter += 1

            if len(pq) > self.max_pq_size:
                self.max_pq_size = len(pq)

            if len(visited) > self.max_visited_size:
                self.max_visited_size = len(visited)

            f_score, _, belief, actions = heapq.heappop(pq)

            # print(f"DEBUG: belief={belief}, actions={actions}")
            belief_tuple = tuple(sorted(belief))
            if belief_tuple in visited:
                continue
            visited.add(belief_tuple)

            if goal_test_belief(belief):
                # Tái tạo đường đi belief state
                self.path = []
                current_belief = initial_belief
                self.path.append([self._string_to_2d(state) for state in current_belief])
                for action in actions:
                    current_belief = self.transition(current_belief, action)
                    self.path.append([self._string_to_2d(state) for state in current_belief])
                self.cost = len(actions)
                self.depth = len(actions)
                self.time_taken = time.perf_counter() - start_time
                total_space = self.max_pq_size + self.max_visited_size
                return self.path, self.cost, self.counter, self.depth, self.time_taken, total_space

            for action in self.get_possible_actions(belief):
                next_belief = self.transition(belief, action)
                next_tuple = tuple(sorted(next_belief))
                if next_tuple not in visited:
                    new_actions = actions + [action]
                    g_score = len(new_actions)
                    h_score = heuristic(next_belief)
                    heapq.heappush(pq, (g_score + h_score, counter, next_belief, new_actions))
                    counter += 1

        self.time_taken = time.perf_counter() - start_time
        total_space = self.max_pq_size + self.max_visited_size
        return [], 0, self.counter, self.depth, self.time_taken, total_space