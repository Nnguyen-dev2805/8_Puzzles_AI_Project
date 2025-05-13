# import random
# import time

# class Backtracking8Puzzle:
#     def __init__(self, update_callback=None):
#         self.board = [None] * 9  # Bảng 8-puzzle (9 ô, ban đầu là None)
#         self.used_values = set()  # Tập hợp các giá trị đã được sử dụng
#         self.steps = 0  # Đếm số bước thực hiện
#         self.update_callback = update_callback  # Hàm callback để cập nhật giao diện

#     def is_valid(self, value):
#         """Kiểm tra ràng buộc: Giá trị chưa được sử dụng."""
#         return value not in self.used_values

#     def backtrack(self, position=0):
#         """Thuật toán Backtracking để gán giá trị cho từng ô."""
#         if position == 9:  # Nếu đã gán giá trị cho tất cả các ô
#             if self.update_callback:
#                 self.update_callback(self.board, "success")
#             return True

#         values = list(range(9))
#         random.shuffle(values)

#         for value in values:
#             if self.is_valid(value):
#                 # Gán giá trị cho ô hiện tại
#                 self.board[position] = value
#                 self.used_values.add(value)
#                 self.steps += 1

#                 # Cập nhật giao diện
#                 if self.update_callback:
#                     self.update_callback(self.board, "assign")
#                 time.sleep(0.5)  # Delay để quan sát

#                 # Tiếp tục gán giá trị cho ô tiếp theo
#                 if self.backtrack(position + 1):
#                     return True

#                 # Backtrack: Hủy gán giá trị và thử giá trị khác
#                 self.board[position] = None
#                 self.used_values.remove(value)

#                 # Cập nhật giao diện khi backtrack
#                 if self.update_callback:
#                     self.update_callback(self.board, "backtrack")
#                 time.sleep(0.5)  # Delay để quan sát

#         return False

#     def solve(self):
#         """Giải bài toán 8-puzzle bằng Backtracking."""
#         if self.update_callback:
#             self.update_callback(self.board, "start")
#         if self.backtrack():
#             print("Thuật toán hoàn tất.")
#         else:
#             print("Không tìm thấy giải pháp.")

import random

def backtracking_with_steps(initial_state, goal_state):
    """
    Hàm Backtracking để giải bài toán 8-Puzzle.
    Args:
        initial_state: Trạng thái ban đầu (danh sách 3x3).
        goal_state: Trạng thái mục tiêu (danh sách 3x3).
    Returns:
        (steps, visited_count): Các bước giải (danh sách các trạng thái), số trạng thái đã thăm.
    """
    def flatten_state(state):
        if isinstance(state, (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state):
            return [state[i][j] for i in range(3) for j in range(3)]
        elif isinstance(state, (list, tuple)) and len(state) == 9:
            return list(state)
        else:
            raise ValueError("State must be a 3x3 grid or a flat list/tuple with 9 elements")

    def is_continuous_sequence(board, pos):
        if pos == 0:
            return True
        max_num = -1
        for i in range(pos):
            row, col = divmod(i, 3)
            if board[row][col] is not None:
                max_num = max(max_num, board[row][col])
        if max_num == 8:
            return board[pos // 3][pos % 3] == 0
        return board[pos // 3][pos % 3] == max_num + 1

    goal_flat = flatten_state(goal_state)
    if set(goal_flat) != set(range(9)):
        raise ValueError("Goal state must contain exactly the numbers 0 to 8")

    goal = [[goal_flat[i * 3 + j] for j in range(3)] for i in range(3)]
    board = [[None for _ in range(3)] for _ in range(3)]
    steps = []
    visited_count = 0

    def backtrack(pos, remaining_numbers):
        nonlocal visited_count
        i, j = divmod(pos, 3)
        
        if pos == 9:
            if all(board[i][j] == goal[i][j] for i in range(3) for j in range(3)):
                steps.append([row[:] for row in board])
                return True
            return False
        
        for idx, num in enumerate(remaining_numbers):
            board[i][j] = num
            if not is_continuous_sequence(board, pos):
                board[i][j] = None
                continue
            steps.append([row[:] for row in board])
            visited_count += 1
            next_numbers = remaining_numbers[:idx] + remaining_numbers[idx+1:]
            if backtrack(pos + 1, next_numbers):
                return True
            board[i][j] = None
            steps.append([row[:] for row in board])
        
        return False

    numbers = list(range(9))
    random.shuffle(numbers)
    success = backtrack(0, numbers)
    
    if not success:
        return [], visited_count
    
    return steps, visited_count