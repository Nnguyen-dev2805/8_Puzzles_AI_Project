# # import numpy as np
# # from collections import defaultdict
# # import random
# # import time
# # from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation

# # class QLearning:
# #     def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
# #         self.Q_table = defaultdict(lambda: [0.0] * 4) 
# #         self.alpha = alpha  # tốc độ học
# #         self.gamma = gamma  # hệ số chiết khấu
# #         self.epsilon = epsilon  # tỷ lệ khám phá
# #         self.counter = 0  
# #         self.path = []  
# #         self.cost = 0  
# #         self.depth = 0 
# #         self.time_taken = 0 

# #     def choose_action(self, state, valid_moves):
# #         if random.random() < self.epsilon:
# #             return random.choice(valid_moves) 
# #         else:
# #             q_values = self.Q_table[state]
# #             return max(range(4), key=lambda i: q_values[i] if i in valid_moves else -float('inf'))

# #     def train(self, inputState, episodes=1000, max_steps=100):
# #         start_time = time.time()
# #         integer_state = int(inputState)
# #         visited = set()
# #         best_path = None # đường đi tốt nhất tìm thấy
# #         best_path_length = float('inf')
# #         for ep in range(episodes):
# #             state = getStringRepresentation(inputState)   
# #             path = [state]
# #             parent = {}
# #             visited.add(state)
# #             total_reward = 0
            
# #             for step in range (max_steps):
                
# import numpy as np
# from collections import defaultdict
# import random
# import time
# from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation

# # Hàm tính khoảng cách Manhattan
# def manhattan_distance(state, goal_state):
#     distance = 0
#     state = np.array(state).reshape(3, 3)
#     goal_state = np.array(goal_state).reshape(3, 3)
#     for i in range(3):
#         for j in range(3):
#             if state[i][j] != 0:  # Bỏ qua ô trống
#                 value = state[i][j]
#                 gi, gj = np.where(goal_state == value)
#                 distance += abs(i - gi[0]) + abs(j - gj[0])
#     return distance

# class QLearning:
#     def __init__(self, alpha=0.1, gamma=0.95, epsilon_start=1.0, epsilon_end=0.01):
#         self.Q_table = defaultdict(lambda: defaultdict(float))  # Q-table với giá trị mặc định
#         self.alpha = alpha  # Tốc độ học
#         self.gamma = gamma  # Hệ số chiết khấu
#         self.epsilon = epsilon_start  # Tỷ lệ khám phá ban đầu
#         self.epsilon_end = epsilon_end
#         self.counter = 0  # Số trạng thái đã thăm
#         self.path = []  # Đường đi
#         self.cost = 0  # Chi phí (số bước)
#         self.depth = 0  # Độ sâu
#         self.time_taken = 0  # Thời gian thực hiện
#         self.visited = set()  # Tập hợp các trạng thái đã thăm
#         self.best_path = None  # Đường đi tốt nhất
#         self.best_path_length = float('inf')
#         self.distance_cache = {}  # Cache cho khoảng cách Manhattan

#     def choose_action(self, state, valid_moves):
#         if random.random() < self.epsilon:
#             return random.choice(valid_moves)  # Khám phá
#         q_vals = [self.Q_table[state][a] for a in valid_moves]
#         return valid_moves[q_vals.index(max(q_vals))]  # Khai thác

#     def train(self, inputState, episodes=5000, max_steps=50):
#         start_time = time.time()
#         epsilon_decay = (self.epsilon - self.epsilon_end) / episodes
#         goal_state_str = getStringRepresentation(goalState)

#         for ep in range(episodes):
#             state = getStringRepresentation(inputState)
#             self.visited.add(state)
#             episode_path = [state]
#             parent = {}
#             total_reward = 0

#             for step in range(max_steps):
#                 self.counter += 1
#                 valid_moves = [str(i) for i in range(4) if str(i) in getChildren(state)]
#                 if not valid_moves:
#                     break

#                 action = self.choose_action(state, valid_moves)
#                 next_state = getChildren(state).get(action, state)

#                 self.visited.add(next_state)
#                 episode_path.append(next_state)
#                 parent[next_state] = (state, action)

#                 # Tính khoảng cách Manhattan sử dụng cache
#                 if state not in self.distance_cache:
#                     state_array = np.array([int(c) for c in state.split(',')])
#                     self.distance_cache[state] = manhattan_distance(state_array, goalState)
#                 if next_state not in self.distance_cache:
#                     next_state_array = np.array([int(c) for c in next_state.split(',')])
#                     self.distance_cache[next_state] = manhattan_distance(next_state_array, goalState)

#                 current_distance = self.distance_cache[state]
#                 next_distance = self.distance_cache[next_state]

#                 # Tính phần thưởng
#                 reward = 100 if goalTest(next_state, goal_state_str) else (current_distance - next_distance) * 10

#                 # Cập nhật Q-table
#                 next_valid_moves = [str(i) for i in range(4) if str(i) in getChildren(next_state)]
#                 max_q_next = max([self.Q_table[next_state][a] for a in next_valid_moves], default=0)
#                 self.Q_table[state][action] += self.alpha * (reward + self.gamma * max_q_next - self.Q_table[state][action])

#                 total_reward += reward

#                 if goalTest(next_state, goal_state_str):
#                     if len(episode_path) < self.best_path_length:
#                         self.best_path = episode_path
#                         self.best_path_length = len(episode_path)
#                     self.path = episode_path
#                     self.cost = len(episode_path) - 1
#                     self.depth = len(episode_path) - 1
#                     print(f"Episode {ep + 1}: Solved in {len(episode_path) - 1} steps")
#                     break

#                 state = next_state

#             if ep % 100 == 0:
#                 print(f"Episode {ep + 1}/{episodes}, Epsilon: {self.epsilon:.3f}")

#             self.epsilon = max(self.epsilon_end, self.epsilon - epsilon_decay)

#             if self.best_path and len(self.best_path) <= 31:
#                 break

#         # Nếu không tìm thấy đường đi, thử xây dựng từ Q-table
#         if not self.best_path:
#             state = getStringRepresentation(inputState)
#             path = [state]
#             for _ in range(max_steps):
#                 if goalTest(state, goal_state_str):
#                     break
#                 valid_moves = [str(i) for i in range(4) if str(i) in getChildren(state)]
#                 if not valid_moves:
#                     break
#                 action = self.choose_action(state, valid_moves)
#                 state = getChildren(state).get(action, state)
#                 path.append(state)
#             self.best_path = path
#             self.path = path
#             self.cost = len(path) - 1
#             self.depth = len(path) - 1

#         self.time_taken = time.time() - start_time
#         return self.best_path, self.cost, self.counter, self.depth, self.time_taken

# import numpy as np
# from collections import defaultdict
# import random
# import time
# from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

# class QLearning:
#     def __init__(self, alpha=0.1, gamma=0.95, epsilon_start=1.0, epsilon_end=0.01):
#         self.Q_table = defaultdict(lambda: defaultdict(float))  # Q-table với giá trị mặc định
#         self.alpha = alpha  # Tốc độ học
#         self.gamma = gamma  # Hệ số chiết khấu
#         self.epsilon = epsilon_start  # Tỷ lệ khám phá ban đầu
#         self.epsilon_end = epsilon_end
#         self.counter = 0  # Số trạng thái đã thăm
#         self.path = []  # Đường đi
#         self.cost = 0  # Chi phí (số bước)
#         self.depth = 0  # Độ sâu
#         self.time_taken = 0  # Thời gian thực hiện
#         self.visited = set()  # Tập hợp các trạng thái đã thăm
#         self.best_path = None  # Đường đi tốt nhất
#         self.best_path_length = float('inf')
#         self.distance_cache = {}  # Cache cho khoảng cách Manhattan

#     def choose_action(self, state, valid_moves):
#         if random.random() < self.epsilon:
#             return random.choice(valid_moves)  # Khám phá
#         q_vals = [self.Q_table[state][a] for a in valid_moves]
#         return valid_moves[q_vals.index(max(q_vals))]  # Khai thác

#     def train(self, inputState, episodes=5000, max_steps=50):
#         start_time = time.time()
#         epsilon_decay = (self.epsilon - self.epsilon_end) / episodes

#         for ep in range(episodes):
#             state = getStringRepresentation(inputState)
#             self.visited.add(state)
#             episode_path = [state]
#             parent = {}
#             total_reward = 0

#             for step in range(max_steps):
#                 self.counter += 1
#                 valid_moves = [str(i) for i in range(4) if str(i) in getChildren(state)]
#                 if not valid_moves:
#                     break

#                 action = self.choose_action(state, valid_moves)
#                 next_state = getChildren(state).get(action, state)

#                 self.visited.add(next_state)
#                 episode_path.append(next_state)
#                 parent[next_state] = (state, action)

#                 # Tính khoảng cách Manhattan sử dụng cache
#                 if state not in self.distance_cache:
#                     self.distance_cache[state] = manhattanDistance(state)
#                 if next_state not in self.distance_cache:
#                     self.distance_cache[next_state] = manhattanDistance(next_state)

#                 current_distance = self.distance_cache[state]
#                 next_distance = self.distance_cache[next_state]

#                 # Tính phần thưởng
#                 reward = 100 if goalTest(next_state) else (current_distance - next_distance) * 10

#                 # Cập nhật Q-table
#                 next_valid_moves = [str(i) for i in range(4) if str(i) in getChildren(next_state)]
#                 max_q_next = max([self.Q_table[next_state][a] for a in next_valid_moves], default=0)
#                 self.Q_table[state][action] += self.alpha * (reward + self.gamma * max_q_next - self.Q_table[state][action])

#                 total_reward += reward

#                 if goalTest(next_state):
#                     if len(episode_path) < self.best_path_length:
#                         self.best_path = episode_path
#                         self.best_path_length = len(episode_path)
#                     self.path = episode_path
#                     self.cost = len(episode_path) - 1
#                     self.depth = len(episode_path) - 1
#                     print(f"Episode {ep + 1}: Solved in {len(episode_path) - 1} steps")
#                     break

#                 state = next_state

#             if ep % 100 == 0:
#                 print(f"Episode {ep + 1}/{episodes}, Epsilon: {self.epsilon:.3f}")

#             self.epsilon = max(self.epsilon_end, self.epsilon - epsilon_decay)

#             if self.best_path and len(self.best_path) <= 31:
#                 break

#         # Nếu không tìm thấy đường đi, thử xây dựng từ Q-table
#         if not self.best_path:
#             state = getStringRepresentation(inputState)
#             path = [state]
#             for _ in range(max_steps):
#                 if goalTest(state):
#                     break
#                 valid_moves = [str(i) for i in range(4) if str(i) in getChildren(state)]
#                 if not valid_moves:
#                     break
#                 action = self.choose_action(state, valid_moves)
#                 state = getChildren(state).get(action, state)
#                 path.append(state)
#             self.best_path = path
#             self.path = path
#             self.cost = len(path) - 1
#             self.depth = len(path) - 1

#         self.time_taken = time.time() - start_time
#         memory_size = len(self.Q_table) * 4  # Ước tính kích thước bộ nhớ
#         return self.best_path, self.cost, self.counter, self.depth, self.time_taken, memory_size


import numpy as np
from collections import defaultdict
import random
import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class QLearning:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon_start=1.0, epsilon_end=0.01):
        self.Q_table = defaultdict(lambda: defaultdict(float))  # Q-table với giá trị mặc định
        self.alpha = alpha  # Tốc độ học
        self.gamma = gamma  # Hệ số chiết khấu
        self.epsilon = epsilon_start  # Tỷ lệ khám phá ban đầu
        self.epsilon_end = epsilon_end
        self.counter = 0  # Số trạng thái đã thăm
        self.path = []  # Đường đi
        self.cost = 0  # Chi phí (số bước)
        self.depth = 0  # Độ sâu
        self.time_taken = 0  # Thời gian thực hiện
        self.visited = set()  # Tập hợp các trạng thái đã thăm
        self.best_path = None  # Đường đi tốt nhất
        self.best_path_length = float('inf')
        self.distance_cache = {}  # Cache cho khoảng cách Manhattan

    def _string_to_2d(self, state_str):
        """Chuyển đổi chuỗi trạng thái thành trạng thái 2D."""
        nums = [int(c) for c in state_str]
        return [nums[i:i+3] for i in range(0, 9, 3)]

    def choose_action(self, state, valid_moves):
        """Chọn hành động dựa trên epsilon-greedy."""
        if random.random() < self.epsilon:
            return random.choice(valid_moves)  # Khám phá
        q_vals = [self.Q_table[state][a] for a in valid_moves]
        return valid_moves[q_vals.index(max(q_vals))]  # Khai thác

    def train(self, inputState, goalState, episodes=5000, max_steps=50):
        start_time = time.perf_counter()
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.visited = set()
        self.best_path = None
        self.best_path_length = float('inf')
        self.distance_cache = {}

        state_2d = inputState
        goal_state_str = getStringRepresentation(goalState)
        epsilon_decay = (self.epsilon - self.epsilon_end) / episodes

        for ep in range(episodes):
            state = getStringRepresentation(state_2d)
            self.visited.add(state)
            episode_path = [state]
            total_reward = 0

            for step in range(max_steps):
                self.counter += 1
                valid_moves = [str(i) for i in range(4) if str(i) in getChildren(state)]
                if not valid_moves:
                    break

                action = self.choose_action(state, valid_moves)
                next_state = getChildren(state).get(action, state)

                self.visited.add(next_state)
                episode_path.append(next_state)

                # Tính khoảng cách Manhattan sử dụng cache
                if state not in self.distance_cache:
                    self.distance_cache[state] = manhattanDistance(int(state))
                if next_state not in self.distance_cache:
                    self.distance_cache[next_state] = manhattanDistance(int(next_state))

                current_distance = self.distance_cache[state]
                next_distance = self.distance_cache[next_state]

                # Tính phần thưởng
                reward = 100 if next_state == goal_state_str else (current_distance - next_distance) * 10

                # Cập nhật Q-table
                next_valid_moves = [str(i) for i in range(4) if str(i) in getChildren(next_state)]
                max_q_next = max([self.Q_table[next_state][a] for a in next_valid_moves], default=0)
                self.Q_table[state][action] += self.alpha * (reward + self.gamma * max_q_next - self.Q_table[state][action])

                total_reward += reward

                if next_state == goal_state_str:
                    if len(episode_path) < self.best_path_length:
                        self.best_path = episode_path
                        self.best_path_length = len(episode_path)
                    self.path = episode_path
                    self.cost = len(episode_path) - 1
                    self.depth = len(episode_path) - 1
                    break

                state = next_state

            # Giảm epsilon
            self.epsilon = max(self.epsilon_end, self.epsilon - epsilon_decay)

            # Thoát sớm nếu tìm thấy đường đi tối ưu
            if self.best_path and len(self.best_path) <= 31:  # Độ dài tối ưu cho 8-puzzle
                break

        # Nếu không tìm thấy đường đi, xây dựng từ Q-table
        if not self.best_path:
            state = getStringRepresentation(state_2d)
            path = [state]
            for _ in range(max_steps):
                if state == goal_state_str:
                    break
                valid_moves = [str(i) for i in range(4) if str(i) in getChildren(state)]
                if not valid_moves:
                    break
                action = self.choose_action(state, valid_moves)
                state = getChildren(state).get(action, state)
                path.append(state)
            self.best_path = path
            self.path = path
            self.cost = len(path) - 1
            self.depth = len(path) - 1

        # Chuyển đổi path thành định dạng 2D
        path_2d = [self._string_to_2d(state) for state in self.best_path]
        self.time_taken = time.perf_counter() - start_time
        memory_size = len(self.Q_table) * 4  # Ước tính kích thước bộ nhớ (bytes)

        return path_2d, self.cost, self.counter, self.depth, self.time_taken, memory_size