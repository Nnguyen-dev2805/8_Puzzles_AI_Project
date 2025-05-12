import numpy as np
from collections import defaultdict
import random
import time

# Lớp 8-Puzzle
class EightPuzzle:
    def __init__(self, difficulty=10):
        self.n = 3  # Kích thước 3x3
        self.goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])  # Trạng thái mục tiêu
        self.board = self._generate_puzzle(difficulty)
        self.actions = [0, 1, 2, 3]  # 0: right, 1: up, 2: left, 3: down

    def _generate_puzzle(self, difficulty):
        # Bắt đầu từ trạng thái mục tiêu và tráo ngẫu nhiên
        board = self.goal.copy()
        for _ in range(difficulty):
            valid_moves = self._get_valid_moves(board)
            action = random.choice(valid_moves)
            board = self._move(board, action)
        return board

    def _get_blank_position(self):
        return np.where(self.board == 0)

    def _get_valid_moves(self, board):
        i, j = self._get_blank_position()
        valid = []
        if i > 0: valid.append(1)  # up
        if i < self.n - 1: valid.append(3)  # down
        if j > 0: valid.append(2)  # left
        if j < self.n - 1: valid.append(0)  # right
        return valid

    def _move(self, board, action):
        i, j = self._get_blank_position()
        new_board = board.copy()
        if action == 0 and j < self.n - 1:  # right
            new_board[i, j], new_board[i, j + 1] = new_board[i, j + 1], new_board[i, j]
        elif action == 1 and i > 0:  # up
            new_board[i, j], new_board[i - 1, j] = new_board[i - 1, j], new_board[i, j]
        elif action == 2 and j > 0:  # left
            new_board[i, j], new_board[i, j - 1] = new_board[i, j - 1], new_board[i, j]
        elif action == 3 and i < self.n - 1:  # down
            new_board[i, j], new_board[i + 1, j] = new_board[i + 1, j], new_board[i, j]
        return new_board

    def move(self, action):
        valid_moves = self._get_valid_moves(self.board)
        if action not in valid_moves:
            return -1000  # Phạt nặng nếu di chuyển không hợp lệ
        self.board = self._move(self.board, action)
        return 100 if np.array_equal(self.board, self.goal) else -1  # Phần thưởng: 100 nếu thắng, -1 nếu không

    def get_state(self):
        return tuple(self.board.flatten())  # Chuyển trạng thái thành tuple để làm khóa

    def is_goal(self):
        return np.array_equal(self.board, self.goal)

# Lớp Q-Learning với Q-table
class QLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.Q_table = defaultdict(lambda: [0.0] * 4)  # Q-table với giá trị mặc định [0, 0, 0, 0]
        self.alpha = alpha  # Tốc độ học
        self.gamma = gamma  # Hệ số chiết khấu
        self.epsilon = epsilon  # Tỷ lệ khám phá
        self.counter = 0  # Số trạng thái đã thăm
        self.path = []  # Đường đi
        self.cost = 0  # Chi phí (số bước)
        self.depth = 0  # Độ sâu
        self.time_taken = 0  # Thời gian thực hiện

    def choose_action(self, state, valid_moves):
        if random.random() < self.epsilon:
            return random.choice(valid_moves)  # Khám phá: chọn ngẫu nhiên
        else:
            q_values = self.Q_table[state]
            return max(range(4), key=lambda i: q_values[i] if i in valid_moves else -float('inf'))  # Khai thác

    def train(self, episodes=1000, max_steps=100):
        start_time = time.time()
        for episode in range(episodes):
            puzzle = EightPuzzle(difficulty=10)
            state = puzzle.get_state()
            steps = 0
            done = False

            while not done and steps < max_steps:
                self.counter += 1
                valid_moves = puzzle._get_valid_moves(puzzle.board)
                action = self.choose_action(state, valid_moves)

                # Thực hiện hành động
                reward = puzzle.move(action)
                next_state = puzzle.get_state()
                done = puzzle.is_goal()

                # Cập nhật Q-table
                old_value = self.Q_table[state][action]
                next_max = max(self.Q_table[next_state]) if not done else 0
                new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
                self.Q_table[state][action] = new_value

                state = next_state
                steps += 1

                if done:
                    self.path = self._reconstruct_path(state)  # Xây dựng đường đi
                    self.cost = steps
                    self.depth = steps
                    print(f"Episode {episode + 1}: Solved in {steps} steps")

            if episode % 100 == 0:
                print(f"Episode {episode + 1}/{episodes}, Epsilon: {self.epsilon}")

            # Giảm epsilon dần
            if self.epsilon > 0.01:
                self.epsilon *= 0.995

        self.time_taken = time.time() - start_time
        return self.path, self.cost, self.counter, self.depth, self.time_taken

    def _reconstruct_path(self, final_state):
        # (Giả định đơn giản: chỉ in đường đi từ trạng thái ban đầu đến cuối)
        # Trong thực tế, cần lưu lịch sử trạng thái và hành động
        return [tuple(self.goal.flatten()), final_state]  # Cần cải tiến để theo dõi đường đi thực tế

    def test(self):
        puzzle = EightPuzzle(difficulty=10)
        state = puzzle.get_state()
        steps = 0
        done = False

        print("Initial State:")
        self._print_board(puzzle.board)
        while not done and steps < 50:
            valid_moves = puzzle._get_valid_moves(puzzle.board)
            action = self.choose_action(state, valid_moves)
            reward = puzzle.move(action)
            next_state = puzzle.get_state()
            done = puzzle.is_goal()

            print(f"Step {steps + 1}, Action: {action}")
            self._print_board(puzzle.board)
            if done:
                print(f"Solved in {steps + 1} steps with reward {reward}")
            elif reward == -1000:
                print("Invalid move, stopping.")
                break

            state = next_state
            steps += 1

        if not done:
            print("Failed to solve within 50 steps.")

    def _print_board(self, board):
        for row in board:
            print(" ".join(map(str, row)))
        print()

# Chạy thử
if __name__ == "__main__":
    ql = QLearning(alpha=0.7, gamma=0.9, epsilon=0.1)
    path, cost, counter, depth, time_taken = ql.train(episodes=1000, max_steps=200)
    print(f"Training completed. Path: {path}")
    print(f"Cost: {cost}, Counter: {counter}, Depth: {depth}, Time taken: {time_taken:.2f} seconds")
    ql.test()