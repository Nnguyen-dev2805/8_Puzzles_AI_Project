import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import deque
from algorithms.test import run_test_algorithm, is_violate_constrain
from algorithms.backtracking_ac3 import backtracking_with_ac3
from algorithms.backtracking import backtracking_with_steps

class BacktrackingWindow:
    def __init__(self, master):
        self.backtracking_window = tk.Toplevel(master)
        self.backtracking_window.title("Backtracking 8-Puzzle")
        self.backtracking_window.geometry("600x700")
        
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.goal_flat = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        
        self.create_backtracking_board()
        
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
        
        self.ac3_button = ttk.Button(control_frame, text="AC-3", 
                                    command=self.run_ac3)
        self.ac3_button.pack(side=tk.LEFT, padx=5)
        
        self.csp_button = ttk.Button(control_frame, text="CSP", 
                                    command=self.show_csp)
        self.csp_button.pack(side=tk.LEFT, padx=5)

        # Thêm nút Backtrack
        self.backtrack_button = ttk.Button(control_frame, text="Backtrack", 
                                        command=self.run_backtrack)
        self.backtrack_button.pack(side=tk.LEFT, padx=5)
        
        self.test_button = ttk.Button(control_frame, text="TEST", 
                                     command=self.run_test)
        self.test_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = ttk.Button(control_frame, text="Quay lại", 
                                 command=self.prev_backtracking_step, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(control_frame, text="Reset", 
                                  command=self.reset_backtracking, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.step_info_label = tk.Label(
            self.backtracking_window,
            text="Nhấn 'Bắt đầu' để chạy Backtracking",
            font=("Arial", 12),
            wraplength=500
        )
        self.step_info_label.pack(pady=10)

        self.step_count_label = tk.Label(
            self.backtracking_window,
            text="Số bước: 0",
            font=("Arial", 12)
        )
        self.step_count_label.pack(pady=5)

        self.current_step_label = tk.Label(
            self.backtracking_window,
            text="Bước hiện tại: 0",
            font=("Arial", 12)
        )
        self.current_step_label.pack(pady=5)
        
        self.backtracking_steps = []
        self.step_info = []  # lưu thông tin từng bước
        self.current_step = 0
        self.backtracking_running = False
        self.csp = None  # Lưu CSP để tái sử dụng

    def create_backtracking_board(self):
        board_frame = ttk.Frame(self.backtracking_window)
        board_frame.pack(pady=20)
        
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
        
        goal_frame = ttk.Frame(self.backtracking_window)
        goal_frame.pack(pady=10)
        
        tk.Label(goal_frame, text="Mục tiêu:", font=("Arial", 12)).pack()
        
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
            self.reset_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.DISABLED)
            self.step_info_label.config(text=f"Đã tìm thấy giải pháp! Số node mở rộng: {result['nodes_expanded']}, Độ sâu tối đa: {result['max_depth']}")
        else:
            self.step_info_label.config(text="Không tìm thấy giải pháp!")
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp!")

    def count_inversions(self, assignment):
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

    def create_constraints(self):
        constraints = []

        # Ràng buộc không trùng lặp
        constraints.append((lambda assignment: len(set(assignment.values())) == len(assignment) if assignment else True))

        return constraints

    def is_consistent(self, var, value, assignment, csp):
        if value in assignment.values() and len(assignment) > 0:
            return False

        temp_assignment = assignment.copy()
        temp_assignment[var] = value

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

    def ac3(self, csp):
        """Thuật toán AC-3 để thực thi tính nhất quán cung."""
        queue = deque([(xi, xj) for xi in csp['variables'] for xj in csp['variables'] if xi != xj])
        domains = {var: values[:] for var, values in csp['domains'].items()}
        
        while queue:
            xi, xj = queue.popleft()
            if self.revise(csp, xi, xj, domains):
                if not domains[xi]:
                    return None  # Không có giải pháp
                for xk in [v for v in csp['variables'] if v != xi and v != xj]:
                    queue.append((xk, xi))
        
        return domains

    def revise(self, csp, xi, xj, domains):
        """Cập nhật miền của xi dựa trên ràng buộc với xj."""
        revised = False
        values_to_remove = []
        
        for x in domains[xi]:
            consistent = False
            for y in domains[xj]:
                temp_assignment = {xi: x, xj: y}
                consistent = all(
                    constraint(temp_assignment) if callable(constraint) else
                    (constraint[1](temp_assignment[constraint[0]]) if constraint[0] in temp_assignment else True)
                    for constraint in csp['constraints']
                )
                if consistent:
                    break
            if not consistent:
                values_to_remove.append(x)
                revised = True
        
        for x in values_to_remove:
            domains[xi].remove(x)
        
        return revised

    def run_ac3(self):
        """Chạy thuật toán Backtracking với AC-3."""
        self.backtracking_steps = []
        self.step_info = []
        self.current_step = 0
        self.step_info_label.config(text="Đang chạy Backtracking với AC-3...")
        self.step_count_label.config(text="Tổng số bước: 0")
        self.current_step_label.config(text="Bước hiện tại: 0")
        
        initial_state = [[None for _ in range(3)] for _ in range(3)]
        steps, visited_count, ac3_log = backtracking_with_ac3(initial_state, self.goal_state)
        
        self.step_info = ac3_log + [f"Trạng thái Backtracking: {step}" for step in steps]
        self.backtracking_steps = steps
        
        if steps:
            self.step_count_label.config(text=f"Tổng số bước: {len(steps)}")
            self.update_backtracking_board(self.backtracking_steps[0], 0)
            self.step_button.config(state=tk.NORMAL)
            self.auto_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.DISABLED)
            self.step_info_label.config(text=f"AC-3 + Backtracking: Tìm thấy giải pháp! Nodes: {visited_count}")
            messagebox.showinfo("Thông báo", f"AC-3 + Backtracking: Tìm thấy giải pháp sau {visited_count} nodes!")
        else:
            self.step_info_label.config(text="AC-3 + Backtracking: Không tìm thấy giải pháp!")
            messagebox.showinfo("Thông báo", "AC-3 + Backtracking: Không tìm thấy giải pháp!")

    def     show_csp(self):
        """Chạy thuật toán Backtracking với backtracking_with_steps."""
        # Reset giao diện để chạy Backtracking
        self.backtracking_steps = []
        self.step_info = []
        self.current_step = 0
        self.step_info_label.config(text="Đang chạy Backtracking...")
        self.step_count_label.config(text="Tổng số bước: 0")
        self.current_step_label.config(text="Bước hiện tại: 0")
        
        # Chạy backtracking_with_steps
        initial_state = [[None for _ in range(3)] for _ in range(3)]
        steps, visited_count = backtracking_with_steps(initial_state, self.goal_state)
        
        # Chuẩn bị step_info từ các bước
        self.step_info = [f"Trạng thái Backtracking: {step}" for step in steps]
        self.backtracking_steps = steps
        
        # Cập nhật giao diện
        if steps:
            self.step_count_label.config(text=f"Tổng số bước: {len(steps)}")
            self.update_backtracking_board(self.backtracking_steps[0], 0)
            self.step_button.config(state=tk.NORMAL)
            self.auto_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.DISABLED)
            self.step_info_label.config(text=f"Backtracking: Tìm thấy giải pháp! Nodes: {visited_count}")
            messagebox.showinfo("Thông báo", f"Backtracking: Tìm thấy giải pháp sau {visited_count} nodes!")
        else:
            self.step_info_label.config(text="Backtracking: Không tìm thấy giải pháp!")
            messagebox.showinfo("Thông báo", "Backtracking: Không tìm thấy giải pháp!")

    def run_test(self):
        """Chạy kiểm tra sử dụng logic từ test_algorithm."""
        self.backtracking_steps = []
        self.step_info = []
        self.current_step = 0
        self.step_info_label.config(text="Đang chạy kiểm tra TEST...")
        self.step_count_label.config(text="Tổng số bước: 0")
        self.current_step_label.config(text="Bước hiện tại: 0")

        path, step_info, step_count = run_test_algorithm(self.goal_state)
        
        self.backtracking_steps = path
        self.step_info = step_info
        
        self.step_count_label.config(text=f"Tổng số bước: {step_count}")
        self.update_backtracking_board(self.backtracking_steps[0], 0)
        self.step_button.config(state=tk.NORMAL)
        self.auto_button.config(state=tk.NORMAL)
        
        if not is_violate_constrain(path[-1], self.goal_state):
            self.step_info_label.config(text="TEST: Đã tìm thấy mục tiêu!")
            messagebox.showinfo("Kết quả kiểm tra", f"Đã tìm thấy mục tiêu sau {step_count} bước!")
        else:
            self.step_info_label.config(text=f"TEST: Không tìm thấy mục tiêu sau {step_count} bước!")
            messagebox.showinfo("Kết quả kiểm tra", f"Không tìm thấy mục tiêu sau {step_count} bước!")

    def solve(self, initial_state):
        nodes_expanded = [0]
        max_depth = [0]
        path = []
        step_info = []

        flat_state = [num if num is not None else 0 for row in initial_state for num in row]
        variables = [f"X{i+1}" for i in range(9)]
        value_order = list(range(9))
        domains = {var: value_order.copy() for var in variables}
        constraints = self.create_constraints()

        self.csp = {
            'variables': variables,
            'domains': domains,
            'constraints': constraints,
            'initial_assignment': {}
        }

        result = self.backtrack({}, 0, self.csp, nodes_expanded, max_depth, path, step_info)

        if result:
            solution_grid = [[0 for _ in range(3)] for _ in range(3)]
            for var, value in result.items():
                idx = int(var[1:]) - 1
                row, col = idx // 3, idx % 3
                solution_grid[row][col] = value
            self.step_info = step_info
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
            return [row[:] for row in grid]

        if assignment:
            path.append(capture_grid(assignment))

        if index == len(csp['variables']):
            grid = [[0 for _ in range(3)] for _ in range(3)]
            for var, value in assignment.items():
                idx = int(var[1:]) - 1
                row, col = idx // 3, idx % 3
                grid[row][col] = value
            inversions = self.count_inversions(assignment)
            if inversions % 2 == 0 and grid == self.goal_state:
                return assignment
            return None

        var = csp['variables'][index]
        values = csp['domains'][var][:]

        # if var == 'X1':
        #     values = [1] + [v for v in values if v != 1]
        # elif var == 'X9':
        #     values = [0] + [v for v in values if v != 0]
        # else:
        random.shuffle(values)

        for value in values:
            assignment[var] = value
            step_info.append(f"Thử {value} tại {var}")
            path.append(capture_grid(assignment))
            if self.is_consistent(var, value, assignment, csp):
                result = self.backtrack(assignment, index + 1, csp, nodes_expanded, max_depth, path, step_info)
                if result:
                    return result
            del assignment[var]
            step_info.append(f"Backtrack: Xóa {value} tại {var}")
            path.append(capture_grid(assignment))

        return None

    def update_backtracking_board(self, state, step_idx):
        for i in range(3):
            for j in range(3):
                value = state[i][j] if state[i][j] is not None else ""
                self.backtracking_tiles[i][j].config(text=str(value), bg="white")

        flat_state = [state[i][j] if state[i][j] is not None else 0 for i in range(3) for j in range(3)]
        for idx in range(9):
            i, j = divmod(idx, 3)
            if flat_state[idx] == 0 or (idx < 8 and flat_state[idx] != self.goal_flat[idx]):
                self.backtracking_tiles[i][j].config(bg="lightyellow")
                break

        if step_idx < len(self.step_info):
            self.step_info_label.config(text=self.step_info[step_idx])
        else:
            self.step_info_label.config(text="Hoàn thành!")
        
        self.current_step_label.config(text=f"Bước hiện tại: {step_idx + 1}")

    def next_backtracking_step(self):
        if self.current_step < len(self.backtracking_steps):
            self.update_backtracking_board(self.backtracking_steps[self.current_step], self.current_step)
            self.current_step += 1
            # Kích hoạt nút Quay lại
            self.prev_button.config(state=tk.NORMAL)
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
            self.step_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)
            self.animate_backtracking()
        else:
            self.backtracking_running = False
            self.auto_button.config(text="Tự động")
            if self.current_step < len(self.backtracking_steps):
                self.step_button.config(state=tk.NORMAL)
            if self.current_step > 0:
                self.prev_button.config(state=tk.NORMAL)

    def animate_backtracking(self):
        if self.current_step < len(self.backtracking_steps) and self.backtracking_running:
            self.update_backtracking_board(self.backtracking_steps[self.current_step], self.current_step)
            self.current_step += 1
            self.backtracking_window.after(500, self.animate_backtracking)
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
            if self.current_step > 0:
                self.prev_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

    def prev_backtracking_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_backtracking_board(self.backtracking_steps[self.current_step], self.current_step)
            if self.current_step < len(self.backtracking_steps) - 1:
                self.step_button.config(state=tk.NORMAL)
            if self.current_step == 0:
                self.prev_button.config(state=tk.DISABLED)
    
    def reset_backtracking(self):
        if self.backtracking_steps:
            self.current_step = 0
            self.update_backtracking_board(self.backtracking_steps[0], 0)
            self.step_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.DISABLED)
            self.auto_button.config(state=tk.NORMAL)
            self.backtracking_running = False
            self.auto_button.config(text="Tự động")

    def run_backtrack(self):
        """Chạy thuật toán Backtracking chỉ với ràng buộc không trùng lặp."""
        initial_state = [[None for _ in range(3)] for _ in range(3)]
        self.backtracking_steps = []
        self.step_info = []
        self.current_step = 0
        self.step_info_label.config(text="Đang chạy Backtracking (không ràng buộc cố định)...")
        self.step_count_label.config(text="Tổng số bước: 0")
        self.current_step_label.config(text="Bước hiện tại: 0")

        result = self.solve(initial_state)
        if result['solution']:
            self.backtracking_steps = result['path']
            self.update_backtracking_board(self.backtracking_steps[0], 0)
            self.step_button.config(state=tk.NORMAL)
            self.auto_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
            self.prev_button.config(state=tk.DISABLED)
            self.step_info_label.config(text=f"Backtracking: Tìm thấy giải pháp! Nodes: {result['nodes_expanded']}, Độ sâu tối đa: {result['max_depth']}")
            self.step_count_label.config(text=f"Tổng số bước: {len(result['path'])}")
            messagebox.showinfo("Thông báo", f"Backtracking: Tìm thấy giải pháp sau {result['nodes_expanded']} nodes!")
        else:
            self.step_info_label.config(text="Backtracking: Không tìm thấy giải pháp!")
            self.step_count_label.config(text="Tổng số bước: 0")
            messagebox.showinfo("Thông báo", "Backtracking: Không tìm thấy giải pháp!")
