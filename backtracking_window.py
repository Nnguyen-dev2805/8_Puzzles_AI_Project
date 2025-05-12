# import tkinter as tk
# from tkinter import ttk, messagebox
# import random

# class BacktrackingWindow:
#     def __init__(self, master):
#         # Tạo cửa sổ mới cho backtracking
#         self.backtracking_window = tk.Toplevel(master)
#         self.backtracking_window.title("Backtracking 8-Puzzle")
#         self.backtracking_window.geometry("600x700")
        
#         # Khởi tạo trạng thái mục tiêu
#         self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
#         self.goal_flat = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        
#         # Tạo bảng 3x3
#         self.create_backtracking_board()
        
#         # Nút điều khiển
#         control_frame = ttk.Frame(self.backtracking_window)
#         control_frame.pack(pady=10)
        
#         self.start_button = ttk.Button(control_frame, text="Bắt đầu", 
#                                     command=self.start_backtracking)
#         self.start_button.pack(side=tk.LEFT, padx=5)
        
#         self.step_button = ttk.Button(control_frame, text="Từng bước", 
#                                     command=self.next_backtracking_step, state=tk.DISABLED)
#         self.step_button.pack(side=tk.LEFT, padx=5)
        
#         self.auto_button = ttk.Button(control_frame, text="Tự động", 
#                                     command=self.auto_backtracking, state=tk.DISABLED)
#         self.auto_button.pack(side=tk.LEFT, padx=5)
        
#         # Thêm nhãn để hiển thị thông tin từng bước
#         self.step_info_label = tk.Label(
#             self.backtracking_window,
#             text="Nhấn 'Bắt đầu' để chạy Backtracking",
#             font=("Arial", 12),
#             wraplength=500
#         )
#         self.step_info_label.pack(pady=10)
        
#         # Khởi tạo biến cho backtracking
#         self.backtracking_steps = []
#         self.step_info = []  # Lưu thông tin từng bước
#         self.current_step = 0
#         self.backtracking_running = False

#     def create_backtracking_board(self):
#         # Tạo frame chính cho bảng
#         board_frame = ttk.Frame(self.backtracking_window)
#         board_frame.pack(pady=20)
        
#         # Tạo frame riêng cho bảng 3x3
#         grid_frame = ttk.Frame(board_frame)
#         grid_frame.pack()
        
#         self.backtracking_tiles = []
#         for i in range(3):
#             row = []
#             for j in range(3):
#                 tile = tk.Label(
#                     grid_frame,
#                     text="",
#                     font=("Arial", 24, "bold"),
#                     width=4,
#                     height=2,
#                     relief="raised",
#                     bg="white"
#                 )
#                 tile.grid(row=i, column=j, padx=2, pady=2)
#                 row.append(tile)
#             self.backtracking_tiles.append(row)
        
#         # Tạo frame riêng cho mục tiêu
#         goal_frame = ttk.Frame(self.backtracking_window)
#         goal_frame.pack(pady=10)
        
#         tk.Label(goal_frame, text="Mục tiêu:", font=("Arial", 12)).pack()
        
#         # Tạo frame riêng cho bảng mục tiêu
#         goal_grid_frame = ttk.Frame(goal_frame)
#         goal_grid_frame.pack()
        
#         for i in range(3):
#             for j in range(3):
#                 idx = i * 3 + j
#                 val = self.goal_flat[idx] if self.goal_flat[idx] != 0 else ""
#                 tk.Label(
#                     goal_grid_frame,
#                     text=str(val),
#                     font=("Arial", 16),
#                     width=4,
#                     height=2,
#                     relief="sunken"
#                 ).grid(row=i, column=j, padx=2, pady=2)

#     def start_backtracking(self):
#         # Khởi tạo trạng thái ban đầu (bảng trống)
#         initial_state = [[None for _ in range(3)] for _ in range(3)]
#         self.backtracking_steps = []
#         self.step_info = []  # Reset thông tin bước
#         self.current_step = 0
#         self.step_info_label.config(text="Đang tìm giải pháp...")

#         # Tìm giải pháp
#         result = self.solve(initial_state)
#         if result['solution']:
#             self.backtracking_steps = result['path']
#             self.update_backtracking_board(self.backtracking_steps[0], 0)
#             self.step_button.config(state=tk.NORMAL)
#             self.auto_button.config(state=tk.NORMAL)
#         else:
#             self.step_info_label.config(text="Không tìm thấy giải pháp!")
#             messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")

#     def create_constraints(self):
#         constraints = []

#         # Ràng buộc không trùng lặp (một số chỉ được sử dụng một lần trong assignment)
#         constraints.append((lambda assignment: len(set(assignment.values())) == len(assignment) if assignment else True))

#         return constraints

#     def is_consistent(self, var, value, assignment, csp):
#         if value in assignment.values() and len(assignment) > 0:
#             return False

#         temp_assignment = assignment.copy()
#         temp_assignment[var] = value

#         for constraint in csp['constraints']:
#             if callable(constraint):
#                 if not constraint(temp_assignment):
#                     return False

#         return True

#     def solve(self, initial_state):
#         nodes_expanded = [0]
#         max_depth = [0]
#         path = []
#         step_info = []  # Lưu thông tin từng bước

#         # Sử dụng None để biểu thị ô trống
#         flat_state = [num if num is not None else 0 for row in initial_state for num in row]
#         variables = [f"X{i+1}" for i in range(9)]
#         value_order = list(range(9))  # Chỉ thử từ 0 đến 8
#         domains = {var: value_order.copy() for var in variables}
#         constraints = self.create_constraints()

#         csp = {
#             'variables': variables,
#             'domains': domains,
#             'constraints': constraints,
#             'initial_assignment': {}
#         }

#         result = self.backtrack({}, 0, csp, nodes_expanded, max_depth, path, step_info)

#         if result:
#             solution_grid = [[0 for _ in range(3)] for _ in range(3)]
#             for var, value in result.items():
#                 idx = int(var[1:]) - 1
#                 row, col = idx // 3, idx % 3
#                 solution_grid[row][col] = value
#             self.step_info = step_info  # Lưu thông tin bước
#             return {
#                 'path': path,
#                 'nodes_expanded': nodes_expanded[0],
#                 'max_depth': max_depth[0],
#                 'solution': solution_grid
#             }
#         else:
#             self.step_info = step_info
#             return {
#                 'path': [],
#                 'nodes_expanded': nodes_expanded[0],
#                 'max_depth': max_depth[0],
#                 'solution': None
#             }

#     def backtrack(self, assignment, index, csp, nodes_expanded, max_depth, path, step_info):
#         nodes_expanded[0] += 1
#         max_depth[0] = max(max_depth[0], len(assignment))

#         def capture_grid(current_assignment):
#             grid = [[None for _ in range(3)] for _ in range(3)]
#             for var, value in current_assignment.items():
#                 idx = int(var[1:]) - 1
#                 row, col = idx // 3, idx % 3
#                 grid[row][col] = value
#             return [row[:] for row in grid]  # Bản sao

#         if assignment:
#             path.append(capture_grid(assignment))  # Lưu trạng thái hiện tại

#         if index == len(csp['variables']):
#             # Kiểm tra xem trạng thái cuối cùng có khớp với goal_state không
#             grid = [[0 for _ in range(3)] for _ in range(3)]
#             for var, value in assignment.items():
#                 idx = int(var[1:]) - 1
#                 row, col = idx // 3, idx % 3
#                 grid[row][col] = value
#             if grid == self.goal_state:
#                 return assignment
#             return None

#         var = csp['variables'][index]

#         # Xáo trộn giá trị để thử ngẫu nhiên
#         values = csp['domains'][var][:]
#         random.shuffle(values)

#         for value in values:
#             if self.is_consistent(var, value, assignment, csp):
#                 assignment[var] = value
#                 step_info.append(f"Thử {value} tại {var}")
#                 path.append(capture_grid(assignment))  # Trạng thái sau khi gán mới
#                 result = self.backtrack(assignment, index + 1, csp, nodes_expanded, max_depth, path, step_info)
#                 if result:
#                     return result
#                 del assignment[var]
#                 step_info.append(f"Backtrack: Xóa {value} tại {var}")
#                 path.append(capture_grid(assignment))  # Trạng thái sau khi xóa để quay lui

#         return None

#     def update_backtracking_board(self, state, step_idx):
#         for i in range(3):
#             for j in range(3):
#                 value = state[i][j] if state[i][j] is not None else ""
#                 self.backtracking_tiles[i][j].config(text=str(value), bg="white")

#         # Highlight ô đang được xử lý
#         flat_state = [state[i][j] if state[i][j] is not None else 0 for i in range(3) for j in range(3)]
#         for idx in range(9):
#             i, j = divmod(idx, 3)
#             if flat_state[idx] == 0 or (idx < 8 and flat_state[idx] != self.goal_flat[idx]):
#                 self.backtracking_tiles[i][j].config(bg="lightyellow")
#                 break

#         # Cập nhật nhãn thông tin bước
#         if step_idx < len(self.step_info):
#             self.step_info_label.config(text=self.step_info[step_idx])
#         else:
#             self.step_info_label.config(text="Hoàn thành!")

#     def next_backtracking_step(self):
#         if self.current_step < len(self.backtracking_steps):
#             self.update_backtracking_board(self.backtracking_steps[self.current_step], self.current_step)
#             self.current_step += 1
#             if self.current_step == len(self.backtracking_steps):
#                 self.step_button.config(state=tk.DISABLED)
#                 flat_last_state = [self.backtracking_steps[-1][i][j] for i in range(3) for j in range(3) if self.backtracking_steps[-1][i][j] is not None]
#                 flat_last_state = [0 if x is None else x for x in flat_last_state] + [0] * (9 - len(flat_last_state))
#                 if flat_last_state == self.goal_flat:
#                     self.step_info_label.config(text="Đã đạt mục tiêu 123456780!")
#                     messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
#                 else:
#                     self.step_info_label.config(text="Không tìm thấy giải pháp!")
#                     messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
#         else:
#             self.step_button.config(state=tk.DISABLED)
#             flat_last_state = [self.backtracking_steps[-1][i][j] for i in range(3) for j in range(3) if self.backtracking_steps[-1][i][j] is not None]
#             flat_last_state = [0 if x is None else x for x in flat_last_state] + [0] * (9 - len(flat_last_state))
#             if flat_last_state == self.goal_flat:
#                 self.step_info_label.config(text="Đã đạt mục tiêu 123456780!")
#                 messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
#             else:
#                 self.step_info_label.config(text="Không tìm thấy giải pháp!")
#                 messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")

#     def auto_backtracking(self):
#         if not self.backtracking_running:
#             self.backtracking_running = True
#             self.auto_button.config(text="Dừng lại")
#             self.animate_backtracking()
#         else:
#             self.backtracking_running = False
#             self.auto_button.config(text="Tự động")

#     def animate_backtracking(self):
#         if self.current_step < len(self.backtracking_steps) and self.backtracking_running:
#             self.update_backtracking_board(self.backtracking_steps[self.current_step], self.current_step)
#             self.current_step += 1
#             self.backtracking_window.after(500, self.animate_backtracking)  # Cập nhật mỗi 0.5 giây
#         elif self.backtracking_running:
#             self.backtracking_running = False
#             self.auto_button.config(text="Tự động")
#             flat_last_state = [self.backtracking_steps[-1][i][j] for i in range(3) for j in range(3) if self.backtracking_steps[-1][i][j] is not None]
#             flat_last_state = [0 if x is None else x for x in flat_last_state] + [0] * (9 - len(flat_last_state))
#             if flat_last_state == self.goal_flat:
#                 self.step_info_label.config(text="Đã đạt mục tiêu 123456780!")
#                 messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
#             else:
#                 self.step_info_label.config(text="Không tìm thấy giải pháp!")
#                 messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")

import tkinter as tk
from tkinter import ttk, messagebox
import random

class BacktrackingWindow:
    def __init__(self, master):
        # Tạo cửa sổ mới cho backtracking
        self.backtracking_window = tk.Toplevel(master)
        self.backtracking_window.title("Backtracking 8-Puzzle")
        self.backtracking_window.geometry("600x700")
        
        # Khởi tạo trạng thái mục tiêu
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.goal_flat = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        
        # Tạo bảng 3x3
        self.create_backtracking_board()
        
        # Nút điều khiển
        control_frame = ttk.Frame(self.backtracking_window)
        control_frame.pack(pady=10)
        
        self.start_button = ttk.Button(control_frame, text="Bắt đầu", 
                                    command=self.start_backtracking)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.step_button = ttk.Button(control_frame, text="Từng bước", 
                                    command=self.next_backtracking_step, state=tk.DISABLED)
        self.step_button.pack(side=tk.LEFT, padx=5)
        
        self.auto_button = ttk.Button(control_frame, text="Tự động", 
                                    command=self.auto_backtracking, state=tk.DISABLED)
        self.auto_button.pack(side=tk.LEFT, padx=5)
        
        # Thêm nhãn để hiển thị thông tin từng bước
        self.step_info_label = tk.Label(
            self.backtracking_window,
            text="Nhấn 'Bắt đầu' để chạy Backtracking",
            font=("Arial", 12),
            wraplength=500
        )
        self.step_info_label.pack(pady=10)
        
        # Khởi tạo biến cho backtracking
        self.backtracking_steps = []
        self.step_info = []  # Lưu thông tin từng bước
        self.current_step = 0
        self.backtracking_running = False

    def create_backtracking_board(self):
        # Tạo frame chính cho bảng
        board_frame = ttk.Frame(self.backtracking_window)
        board_frame.pack(pady=20)
        
        # Tạo frame riêng cho bảng 3x3
        grid_frame = ttk.Frame(board_frame)
        grid_frame.pack()
        
        self.backtracking_tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                tile = tk.Label(
                    grid_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2,
                    relief="raised",
                    bg="white"
                )
                tile.grid(row=i, column=j, padx=2, pady=2)
                row.append(tile)
            self.backtracking_tiles.append(row)
        
        # Tạo frame riêng cho mục tiêu
        goal_frame = ttk.Frame(self.backtracking_window)
        goal_frame.pack(pady=10)
        
        tk.Label(goal_frame, text="Mục tiêu:", font=("Arial", 12)).pack()
        
        # Tạo frame riêng cho bảng mục tiêu
        goal_grid_frame = ttk.Frame(goal_frame)
        goal_grid_frame.pack()
        
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                val = self.goal_flat[idx] if self.goal_flat[idx] != 0 else ""
                tk.Label(
                    goal_grid_frame,
                    text=str(val),
                    font=("Arial", 16),
                    width=4,
                    height=2,
                    relief="sunken"
                ).grid(row=i, column=j, padx=2, pady=2)

    def start_backtracking(self):
        # Khởi tạo trạng thái ban đầu (bảng trống)
        initial_state = [[None for _ in range(3)] for _ in range(3)]
        self.backtracking_steps = []
        self.step_info = []  # Reset thông tin bước
        self.current_step = 0
        self.step_info_label.config(text="Đang tìm giải pháp...")

        # Tìm giải pháp
        result = self.solve(initial_state)
        if result['solution']:
            self.backtracking_steps = result['path']
            self.update_backtracking_board(self.backtracking_steps[0], 0)
            self.step_button.config(state=tk.NORMAL)
            self.auto_button.config(state=tk.NORMAL)
        else:
            self.step_info_label.config(text="Không tìm thấy giải pháp!")
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")

    def count_inversions(self, assignment):
        # Chuyển assignment thành dãy phẳng
        flat = [0] * 9  # Khởi tạo dãy phẳng với 9 phần tử
        for var, value in assignment.items():
            idx = int(var[1:]) - 1  # X1 -> index 0, X2 -> index 1, ...
            flat[idx] = value
        
        # Lấy các số không phải 0
        numbers = [num for num in flat if num != 0]
        
        # Đếm số hoán vị
        inversions = 0
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] > numbers[j]:
                    inversions += 1
        return inversions

    def create_constraints(self):
        constraints = []

        # Ràng buộc không trùng lặp
        constraints.append((lambda assignment: len(set(assignment.values())) == len(assignment) if assignment else True))

        # Ràng buộc cố định: X1 phải là 1
        constraints.append(('X1', lambda x: x == 1))

        # Ràng buộc cố định: X9 phải là 0
        constraints.append(('X9', lambda x: x == 0))

        return constraints

    def is_consistent(self, var, value, assignment, csp):
        # Kiểm tra không trùng lặp
        if value in assignment.values() and len(assignment) > 0:
            return False

        temp_assignment = assignment.copy()
        temp_assignment[var] = value

        # Kiểm tra các ràng buộc khác
        for constraint in csp['constraints']:
            if callable(constraint):
                if not constraint(temp_assignment):
                    return False
            elif len(constraint) == 2:
                name, constraint_func = constraint
                if name in temp_assignment:
                    if not constraint_func(temp_assignment[name]):
                        return False

        return True

    def solve(self, initial_state):
        nodes_expanded = [0]
        max_depth = [0]
        path = []
        step_info = []  # Lưu thông tin từng bước

        # Sử dụng None để biểu thị ô trống
        flat_state = [num if num is not None else 0 for row in initial_state for num in row]
        variables = [f"X{i+1}" for i in range(9)]
        value_order = list(range(9))  # Chỉ thử từ 0 đến 8
        domains = {var: value_order.copy() for var in variables}
        constraints = self.create_constraints()

        csp = {
            'variables': variables,
            'domains': domains,
            'constraints': constraints,
            'initial_assignment': {}
        }

        # Bắt đầu backtracking
        result = self.backtrack({}, 0, csp, nodes_expanded, max_depth, path, step_info)

        if result:
            solution_grid = [[0 for _ in range(3)] for _ in range(3)]
            for var, value in result.items():
                idx = int(var[1:]) - 1
                row, col = idx // 3, idx % 3
                solution_grid[row][col] = value
            self.step_info = step_info  # Lưu thông tin bước
            return {
                'path': path,
                'nodes_expanded': nodes_expanded[0],
                'max_depth': max_depth[0],
                'solution': solution_grid
            }
        else:
            self.step_info = step_info
            return {
                'path': path,
                'nodes_expanded': nodes_expanded[0],
                'max_depth': max_depth[0],
                'solution': None
            }

    def backtrack(self, assignment, index, csp, nodes_expanded, max_depth, path, step_info):
        nodes_expanded[0] += 1
        max_depth[0] = max(max_depth[0], len(assignment))

        def capture_grid(current_assignment):
            grid = [[None for _ in range(3)] for _ in range(3)]
            for var, value in current_assignment.items():
                idx = int(var[1:]) - 1
                row, col = idx // 3, idx % 3
                grid[row][col] = value
            return [row[:] for row in grid]  # Bản sao

        # Lưu trạng thái hiện tại
        if assignment:
            path.append(capture_grid(assignment))

        # Nếu đã gán hết các biến, kiểm tra trạng thái mục tiêu và số hoán vị
        if index == len(csp['variables']):
            grid = [[0 for _ in range(3)] for _ in range(3)]
            for var, value in assignment.items():
                idx = int(var[1:]) - 1
                row, col = idx // 3, idx % 3
                grid[row][col] = value
            # Kiểm tra số hoán vị chẵn
            inversions = self.count_inversions(assignment)
            if inversions % 2 == 0 and grid == self.goal_state:
                return assignment
            return None

        var = csp['variables'][index]
        values = csp['domains'][var][:]

        # Ưu tiên giá trị hợp lệ nhưng vẫn thử các giá trị không hợp lệ
        if var == 'X1':
            values = [1] + [v for v in values if v != 1]  # Ưu tiên 1
        elif var == 'X9':
            values = [0] + [v for v in values if v != 0]  # Ưu tiên 0
        else:
            random.shuffle(values)  # Thử ngẫu nhiên cho các ô khác

        for value in values:
            # Thử gán giá trị
            assignment[var] = value
            step_info.append(f"Thử {value} tại {var}")
            path.append(capture_grid(assignment))

            # Kiểm tra ràng buộc sau khi gán
            if self.is_consistent(var, value, assignment, csp):
                result = self.backtrack(assignment, index + 1, csp, nodes_expanded, max_depth, path, step_info)
                if result is not None:
                    return result

            # Backtrack nếu không hợp lệ
            del assignment[var]
            step_info.append(f"Backtrack: Xóa {value} tại {var}")
            path.append(capture_grid(assignment))

        return None

    def update_backtracking_board(self, state, step_idx):
        for i in range(3):
            for j in range(3):
                value = state[i][j] if state[i][j] is not None else ""
                self.backtracking_tiles[i][j].config(text=str(value), bg="white")

        # Highlight ô đang được xử lý
        flat_state = [state[i][j] if state[i][j] is not None else 0 for i in range(3) for j in range(3)]
        for idx in range(9):
            i, j = divmod(idx, 3)
            if flat_state[idx] == 0 or (idx < 8 and flat_state[idx] != self.goal_flat[idx]):
                self.backtracking_tiles[i][j].config(bg="lightyellow")
                break

        # Cập nhật nhãn thông tin bước
        if step_idx < len(self.step_info):
            self.step_info_label.config(text=self.step_info[step_idx])
        else:
            self.step_info_label.config(text="Hoàn thành!")

    def next_backtracking_step(self):
        if self.current_step < len(self.backtracking_steps):
            self.update_backtracking_board(self.backtracking_steps[self.current_step], self.current_step)
            self.current_step += 1
            if self.current_step == len(self.backtracking_steps):
                self.step_button.config(state=tk.DISABLED)
                flat_last_state = [self.backtracking_steps[-1][i][j] for i in range(3) for j in range(3) if self.backtracking_steps[-1][i][j] is not None]
                flat_last_state = [0 if x is None else x for x in flat_last_state] + [0] * (9 - len(flat_last_state))
                if flat_last_state == self.goal_flat:
                    self.step_info_label.config(text="Đã đạt mục tiêu 123456780!")
                    messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
                else:
                    self.step_info_label.config(text="Không tìm thấy giải pháp!")
                    messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")
        else:
            self.step_button.config(state=tk.DISABLED)
            flat_last_state = [self.backtracking_steps[-1][i][j] for i in range(3) for j in range(3) if self.backtracking_steps[-1][i][j] is not None]
            flat_last_state = [0 if x is None else x for x in flat_last_state] + [0] * (9 - len(flat_last_state))
            if flat_last_state == self.goal_flat:
                self.step_info_label.config(text="Đã đạt mục tiêu 123456780!")
                messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
            else:
                self.step_info_label.config(text="Không tìm thấy giải pháp!")
                messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")

    def auto_backtracking(self):
        if not self.backtracking_running:
            self.backtracking_running = True
            self.auto_button.config(text="Dừng lại")
            self.animate_backtracking()
        else:
            self.backtracking_running = False
            self.auto_button.config(text="Tự động")

    def animate_backtracking(self):
        if self.current_step < len(self.backtracking_steps) and self.backtracking_running:
            self.update_backtracking_board(self.backtracking_steps[self.current_step], self.current_step)
            self.current_step += 1
            self.backtracking_window.after(500, self.animate_backtracking)  # Cập nhật mỗi 0.5 giây
        elif self.backtracking_running:
            self.backtracking_running = False
            self.auto_button.config(text="Tự động")
            flat_last_state = [self.backtracking_steps[-1][i][j] for i in range(3) for j in range(3) if self.backtracking_steps[-1][i][j] is not None]
            flat_last_state = [0 if x is None else x for x in flat_last_state] + [0] * (9 - len(flat_last_state))
            if flat_last_state == self.goal_flat:
                self.step_info_label.config(text="Đã đạt mục tiêu 123456780!")
                messagebox.showinfo("Thông báo", "Đã đạt mục tiêu 123456780!")
            else:
                self.step_info_label.config(text="Không tìm thấy giải pháp!")
                messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")