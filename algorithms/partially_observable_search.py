import time
import heapq
import random
from collections import defaultdict
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

# tìm đường đi từ niềm tin ban đầu đến trạng thái mục tiêu trong điều kiện môi trường không hoàn toàn quan sát được
# sử dụng A* để điều hướng theo heuristic
# khi quan sát một trạng thái, có thể bị nhiễu và nhận sai trạng thái thực sự
# từ tập niềm tin ban đầu agent thực hiện hành đồng sau đó được trả về một môi trường quan sát
# sau đó cập nhật lại niềm tin, tức là xác suất phân phối mới của các trạng thái mà agent có thể đang ở, dựa vào quan sát được
# chỉ cần trạng thái có xác suất cao nhất ở trong tập goal

class POMDPBeliefStateSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_pq_size = 0
        self.max_visited_size = 0
        self.observation_noise = 0.2  # hệ số nhiễu quan sát
        self.gamma = 0.9  # hệ số chiết khấu

    def _state_to_string(self, state_2d):
        """Chuyển đổi trạng thái 2D thành chuỗi."""
        flat = [str(num) for row in state_2d for num in row]
        return ''.join(flat)

    def _string_to_2d(self, state_str):
        """Chuyển đổi chuỗi trạng thái thành trạng thái 2D."""
        nums = [int(c) for c in state_str]
        return [nums[i:i+3] for i in range(0, 9, 3)]

    def get_possible_actions(self, belief):
        """Lấy tất cả hành động hợp lệ từ các trạng thái trong belief."""
        actions = set()
        for state in belief:
            idx = state.index("0")
            i, j = divmod(idx, 3)
            moves = [(-1, 0, "0"), (1, 0, "1"), (0, -1, "2"), (0, 1, "3")]
            for di, dj, action in moves:
                ni, nj = i + di, j + dj
                if 0 <= ni < 3 and 0 <= nj < 3:
                    actions.add(action)
        return list(actions)

    def transition(self, state, action):
        """Áp dụng hành động cho một trạng thái."""
        idx = state.index("0")
        i, j = divmod(idx, 3)
        di, dj = {"0": (-1, 0), "1": (1, 0), "2": (0, -1), "3": (0, 1)}[action]
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_index = ni * 3 + nj
            new_state = list(state)
            new_state[idx], new_state[new_index] = new_state[new_index], new_state[idx]
            return ''.join(new_state)
        return state

    def reward(self, state):
        """Phần thưởng: 100 nếu đạt mục tiêu, -1 nếu không."""
        return 100 if state in self.goal_belief else -1

    def observation(self, state):
        """mô phỏng việc quan sát trạng thái sau khi thực hiện hành động và có thể trả sai trạng thái thực tế với xác suất là 0,2"""
        if random.random() < self.observation_noise:
            return random.choice(list(self.all_states))
        return state

    def update_belief(self, belief, action, observation):
        """Cập nhật niềm tin bằng công thức Bayes."""
        # nếu quan sát đúng thì xác suất bước hiện tại tăng cao
        # nếu quan sát sai thì chia đều xác suất cho cả 3
        new_belief = defaultdict(float)
        for state in belief:
            next_state = self.transition(state, action)
            prob = belief[state] * (
                (1 - self.observation_noise) if next_state == observation 
                else self.observation_noise / (len(self.all_states) - 1)
            )
            new_belief[next_state] += prob
        total = sum(new_belief.values())
        if total > 0:
            for state in new_belief:
                new_belief[state] /= total
        return dict(new_belief)

    def heuristic(self, belief):
        """Heuristic: Trung bình khoảng cách Manhattan theo xác suất."""
        total_distance = 0
        for state, prob in belief.items():
            min_distance = manhattanDistance(int(state))
            total_distance += prob * min_distance
        return total_distance

    def POMDPBeliefStateSearch(self, initial_belief_states, goal_belief_states, max_iterations=1000, time_limit=10):
        start_time = time.perf_counter()
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.max_pq_size = 0
        self.max_visited_size = 0

        initial_belief = {self._state_to_string(state): 1.0 / len(initial_belief_states) for state in initial_belief_states}
        self.goal_belief = {self._state_to_string(state) for state in goal_belief_states}
        self.all_states = initial_belief_states + goal_belief_states

        def goal_test_belief(belief):
            max_state = max(belief, key=belief.get)
            return max_state in self.goal_belief

        if goal_test_belief(initial_belief):
            path = [[self._string_to_2d(state) for state in initial_belief]]
            self.time_taken = time.perf_counter() - start_time
            total_space = len(initial_belief)
            return path, 0, 0, 0, self.time_taken, total_space

        pq = []
        visited = set()
        counter = 0
        h_score = self.heuristic(initial_belief)
        heapq.heappush(pq, (h_score, counter, initial_belief, []))
        counter += 1

        while pq and time.perf_counter() - start_time < time_limit and counter < max_iterations:
            self.counter += 1
            if len(pq) > self.max_pq_size:
                self.max_pq_size = len(pq)
            if len(visited) > self.max_visited_size:
                self.max_visited_size = len(visited)

            f_score, _, belief, actions = heapq.heappop(pq)
            belief_tuple = tuple(sorted(belief.items()))
            if belief_tuple in visited:
                continue
            visited.add(belief_tuple)

            if goal_test_belief(belief):
                self.path = []
                current_belief = initial_belief
                self.path.append([self._string_to_2d(state) for state in current_belief])
                for action in actions:
                    sample_state = max(current_belief, key=current_belief.get)
                    next_state = self.transition(sample_state, action)
                    observation = self.observation(next_state)
                    current_belief = self.update_belief(current_belief, action, observation)
                    self.path.append([self._string_to_2d(next_state)])
                self.cost = len(actions)
                self.depth = len(actions)
                self.time_taken = time.perf_counter() - start_time
                total_space = self.max_pq_size + self.max_visited_size
                # print(self.path)
                return self.path, self.cost, self.counter, self.depth, self.time_taken, total_space

            for action in self.get_possible_actions(belief):
                sample_state = max(belief, key=belief.get)
                next_state = self.transition(sample_state, action)
                observation = self.observation(next_state)
                next_belief = self.update_belief(belief, action, observation)
                next_tuple = tuple(sorted(next_belief.items()))
                if next_tuple not in visited:
                    new_actions = actions + [action]
                    g_score = len(new_actions)
                    h_score = self.heuristic(next_belief)
                    heapq.heappush(pq, (g_score + h_score, counter, next_belief, new_actions))
                    counter += 1

        self.time_taken = time.perf_counter() - start_time
        total_space = self.max_pq_size + self.max_visited_size
        return [], 0, self.counter, self.depth, self.time_taken, total_space
    


