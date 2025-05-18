import tkinter as tk
from tkinter import ttk, messagebox
import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance
from algorithms import no_observation_belief_state_search

class NoObsBeliefWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("No Observation Belief State Search")
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        self.window.minsize(900, 700)

        # Đặt font Roboto
        roboto_font = ("Roboto", 12)
        roboto_bold = ("Roboto", 16, "bold")

        # Biến lưu trữ trạng thái
        self.initial_states = []
        self.goal_states = []
        self.max_iterations = tk.IntVar(value=1000)
        self.time_limit = tk.DoubleVar(value=10.0)
        self.path = []
        self.current_step = 0
        self.running = False

        # Tiêu đề
        title_label = ttk.Label(self.window, text="No Observation Belief State Search", font=roboto_bold)
        title_label.pack(pady=10)

        # Frame chính để chứa ô nhập liệu và bảng 3x3
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10)

        # Frame cho nhập liệu (bên trái)
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(side="left", padx=10, pady=10, fill="y")

        # Nhập Initial Belief States
        initial_label = ttk.Label(input_frame, text="Trạng Thái Niềm Tin Ban Đầu (9 số, mỗi dòng):", font=roboto_font)
        initial_label.pack(anchor="w", pady=5)
        self.initial_text = tk.Text(input_frame, height=5, width=30, font=roboto_font)
        self.initial_text.pack(pady=5)
        initial_default = ["123405678", "123450678", "120453678"]
        self.initial_text.insert(tk.END, "\n".join(initial_default) + "\n")
        initial_example = ttk.Label(input_frame, text="Ví dụ: 123456078", font=roboto_font)
        initial_example.pack(anchor="w", pady=5)

        # Nhập Goal Belief States
        goal_label = ttk.Label(input_frame, text="Trạng Thái Niềm Tin Mục Tiêu (9 số, mỗi dòng):", font=roboto_font)
        goal_label.pack(anchor="w", pady=5)
        self.goal_text = tk.Text(input_frame, height=5, width=30, font=roboto_font)
        self.goal_text.pack(pady=5)
        goal_default = ["123456780", "123456708"]
        self.goal_text.insert(tk.END, "\n".join(goal_default) + "\n")
        goal_example = ttk.Label(input_frame, text="Ví dụ: 123456780", font=roboto_font)
        goal_example.pack(anchor="w", pady=5)

        # Nhập Max Iterations
        max_iter_frame = ttk.Frame(input_frame)
        max_iter_frame.pack(anchor="w", pady=5)
        max_iter_label = ttk.Label(max_iter_frame, text="Số Lần Lặp Tối Đa:", font=roboto_font)
        max_iter_label.pack(side="left", padx=5)
        max_iter_entry = ttk.Entry(max_iter_frame, textvariable=self.max_iterations, font=roboto_font, width=10)
        max_iter_entry.pack(side="left")

        # Nhập Time Limit
        time_limit_frame = ttk.Frame(input_frame)
        time_limit_frame.pack(anchor="w", pady=5)
        time_limit_label = ttk.Label(time_limit_frame, text="Giới Hạn Thời Gian (giây):", font=roboto_font)
        time_limit_label.pack(side="left", padx=5)
        time_limit_entry = ttk.Entry(time_limit_frame, textvariable=self.time_limit, font=roboto_font, width=10)
        time_limit_entry.pack(side="left")

        # Frame cho bảng 3x3 và bảng mục tiêu (bên phải)
        board_container = ttk.Frame(main_frame)
        board_container.pack(side="right", padx=20, pady=10)

        # Tạo bảng 3x3 để hiển thị trạng thái
        self.create_board(board_container)

        # Frame cho kết quả phân tích (dưới ô nhập liệu)
        result_frame = ttk.Frame(input_frame)
        result_frame.pack(pady=10, fill="x")
        self.result_text = tk.Text(result_frame, height=10, width=50, font=roboto_font)
        self.result_text.pack(pady=5)

        # Frame cho các nút điều khiển
        control_frame = ttk.Frame(self.window)
        control_frame.pack(pady=5)

        self.start_button = ttk.Button(control_frame, text="Bắt đầu", command=self.start_algorithm)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.step_button = ttk.Button(control_frame, text="Từng bước", command=self.next_step, state=tk.DISABLED)
        self.step_button.pack(side=tk.LEFT, padx=5)

        self.auto_button = ttk.Button(control_frame, text="Tự động", command=self.auto_play, state=tk.DISABLED)
        self.auto_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = ttk.Button(control_frame, text="Quay lại", command=self.prev_step, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(control_frame, text="Reset", command=self.reset, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Nhãn thông tin bước
        self.step_info_label = tk.Label(self.window, text="Nhấn 'Bắt đầu' để chạy thuật toán", font=roboto_font)
        self.step_info_label.pack(pady=5)

        self.step_count_label = tk.Label(self.window, text="Tổng số bước: 0", font=roboto_font)
        self.step_count_label.pack(pady=5)

        self.current_step_label = tk.Label(self.window, text="Bước hiện tại: 0", font=roboto_font)
        self.current_step_label.pack(pady=5)

        # Nút Đóng
        close_button = ttk.Button(self.window, text="Đóng", command=self.window.destroy)
        close_button.pack(pady=10)

    def create_board(self, parent):
        """Tạo bảng 3x3 để hiển thị trạng thái của 8-puzzle."""
        board_frame = ttk.Frame(parent)
        board_frame.pack(pady=20)

        grid_frame = ttk.Frame(board_frame)
        grid_frame.pack()

        self.tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                tile = tk.Label(
                    grid_frame,
                    text="",
                    font=("Roboto", 24, "bold"),
                    width=4,
                    height=2,
                    relief="raised",
                    bg="white"
                )
                tile.grid(row=i, column=j, padx=2, pady=2)
                row.append(tile)
            self.tiles.append(row)

        # Hiển thị trạng thái mục tiêu (sẽ được cập nhật sau khi chạy thuật toán)
        self.goal_frame = ttk.Frame(parent)
        self.goal_frame.pack(pady=10)

        tk.Label(self.goal_frame, text="Mục tiêu:", font=("Roboto", 12)).pack()

        self.goal_grid_frame = ttk.Frame(self.goal_frame)
        self.goal_grid_frame.pack()

        # Khởi tạo với trạng thái rỗng, sẽ cập nhật sau
        for i in range(3):
            for j in range(3):
                tk.Label(
                    self.goal_grid_frame,
                    text="",
                    font=("Roboto", 16),
                    width=4,
                    height=2,
                    relief="sunken"
                ).grid(row=i, column=j, padx=2, pady=2)

    def update_board(self, state):
        """Cập nhật bảng 3x3 với trạng thái hiện tại."""
        # Đảm bảo state là danh sách 2 chiều 3x3
        if isinstance(state, list) and len(state) == 1 and all(isinstance(row, list) for row in state[0]):
            state = state[0]  # Trích xuất lưới 3x3 từ danh sách lồng
        elif isinstance(state, str):
            state = [int(state[i * 3 + j]) for i in range(3) for j in range(3)]
            state = [state[i:i + 3] for i in range(0, 9, 3)]
        elif isinstance(state, list) and len(state) == 9 and all(isinstance(x, (int, str)) for x in state):
            state = [state[i:i + 3] for i in range(0, 9, 3)]

        # Kiểm tra định dạng hợp lệ
        if not (isinstance(state, list) and len(state) == 3 and all(len(row) == 3 for row in state)):
            self.step_info_label.config(text="Lỗi: Trạng thái không hợp lệ!")
            return

        for i in range(3):
            for j in range(3):
                value = state[i][j] if state[i][j] != 0 else ""
                self.tiles[i][j].config(text=str(value), bg="white")

        # So sánh với trạng thái mục tiêu (sẽ được cập nhật từ path)
        if hasattr(self, 'goal_state_2d') and self.goal_state_2d is not None:
            for i in range(3):
                for j in range(3):
                    if state[i][j] == 0:
                        self.tiles[i][j].config(bg="lightgray")
                    elif state[i][j] == self.goal_state_2d[i][j]:
                        self.tiles[i][j].config(bg="lightgreen")
                    else:
                        self.tiles[i][j].config(bg="lightyellow")

    def update_goal_board(self, goal_state):
        """Cập nhật bảng mục tiêu với trạng thái cuối cùng từ path."""
        if isinstance(goal_state, list) and len(goal_state) == 1 and all(isinstance(row, list) for row in goal_state[0]):
            goal_state = goal_state[0]
        elif isinstance(goal_state, str):
            goal_state = [int(goal_state[i * 3 + j]) for i in range(3) for j in range(3)]
            goal_state = [goal_state[i:i + 3] for i in range(0, 9, 3)]
        elif isinstance(goal_state, list) and len(goal_state) == 9 and all(isinstance(x, (int, str)) for x in goal_state):
            goal_state = [goal_state[i:i + 3] for i in range(0, 9, 3)]

        if not (isinstance(goal_state, list) and len(goal_state) == 3 and all(len(row) == 3 for row in goal_state)):
            return

        self.goal_state_2d = goal_state  # Lưu trạng thái mục tiêu để so sánh
        for i in range(3):
            for j in range(3):
                value = goal_state[i][j] if goal_state[i][j] != 0 else ""
                self.goal_grid_frame.grid_slaves(row=i, column=j)[0].config(text=str(value))

    def parse_state(self, text):
        """Phân tích chuỗi nhập liệu thành danh sách trạng thái 9 số."""
        states = []
        lines = text.splitlines()
        for line in lines:
            if not line.strip():
                continue
            try:
                cleaned = line.replace(' ', '')
                if len(cleaned) != 9 or not all(c in '012345678' for c in cleaned):
                    raise ValueError("Định dạng trạng thái không hợp lệ")
                states.append(cleaned)
            except ValueError as e:
                messagebox.showerror("Lỗi", f"Đầu vào không hợp lệ: {e}")
                return None
        return states if states else None
    def start_algorithm(self):
        """Chạy thuật toán và chuẩn bị hiển thị kết quả."""
        self.result_text.delete(1.0, tk.END)
        self.path = []
        self.current_step = 0  # Bắt đầu từ bước 0, nhưng sẽ hiển thị từ bước 1

        initial_states = self.parse_state(self.initial_text.get(1.0, tk.END))
        goal_states = self.parse_state(self.goal_text.get(1.0, tk.END))

        if not initial_states or not goal_states:
            messagebox.showerror("Lỗi", "Vui lòng nhập trạng thái ban đầu và mục tiêu hợp lệ.")
            return

        self.initial_states = initial_states
        self.goal_states = goal_states

        algorithm = no_observation_belief_state_search.NoObservationBeliefStateSearchAlgorithm()
        start_time = time.perf_counter()
        path, cost, counter, depth, time_taken, total_space = algorithm.NoObsBeliefStateSearch(
            initial_states, goal_states,
            max_iterations=self.max_iterations.get(),
            time_limit=self.time_limit.get()
        )

        self.result_text.insert(tk.END, f"Thời Gian Thực Thi: {time_taken:.2f} giây\n")
        self.result_text.insert(tk.END, f"Chi Phí (Số Bước): {cost}\n")
        self.result_text.insert(tk.END, f"Số Trạng Thái Khám Phá: {counter}\n")
        self.result_text.insert(tk.END, f"Độ Sâu: {depth}\n")
        self.result_text.insert(tk.END, f"Tổng Không Gian Sử Dụng: {total_space} nút\n")
        self.result_text.insert(tk.END, "\nĐường Đi:\n")
        for i, step in enumerate(path):
            self.result_text.insert(tk.END, f"Bước {i}:\n")
            for row in step[0] if isinstance(step, list) and len(step) == 1 else step:
                self.result_text.insert(tk.END, str(row) + "\n")
            self.result_text.insert(tk.END, "\n")

        if not path:
            self.result_text.insert(tk.END, "Không tìm thấy giải pháp trong giới hạn cho phép.\n")
            self.step_info_label.config(text="Không tìm thấy giải pháp!")
            return

        # Chuẩn hóa path để chỉ chứa các lưới 2 chiều 3x3
        self.path = []
        for step in path:
            if isinstance(step, list) and len(step) == 1 and all(isinstance(row, list) for row in step[0]):
                self.path.append(step[0])  # Trích xuất lưới 3x3 từ danh sách lồng
            else:
                self.path.append(step)

        self.step_count_label.config(text=f"Tổng số bước: {len(self.path)}")
        self.step_info_label.config(text="Đã tìm thấy giải pháp! Nhấn 'Từng bước' hoặc 'Tự động' để xem.")
        # Hiển thị bước 1 (index 0 trong self.path, nhưng ghi là bước 1)
        if len(self.path) > 0:
            self.update_board(self.path[0])
            self.current_step = 1
            # Cập nhật trạng thái mục tiêu bằng trạng thái cuối cùng trong path
            if len(self.path) > 1:
                self.update_goal_board(self.path[-1])
        self.current_step_label.config(text=f"Bước hiện tại: {self.current_step}")
        self.step_button.config(state=tk.NORMAL)
        self.auto_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.prev_button.config(state=tk.DISABLED)

    def next_step(self):
        if self.current_step < len(self.path):
            self.current_step += 1
            self.update_board(self.path[self.current_step - 1])
            self.current_step_label.config(text=f"Bước hiện tại: {self.current_step}")
            self.prev_button.config(state=tk.NORMAL)
            if self.current_step == len(self.path):
                self.step_button.config(state=tk.DISABLED)
                self.step_info_label.config(text="Đã hoàn thành đường đi!")
                messagebox.showinfo("Thông báo", "Đã hoàn thành đường đi!")

    def prev_step(self):
        if self.current_step > 1:
            self.current_step -= 1
            self.update_board(self.path[self.current_step - 1])
            self.current_step_label.config(text=f"Bước hiện tại: {self.current_step}")
            self.step_button.config(state=tk.NORMAL)
            if self.current_step == 1:
                self.prev_button.config(state=tk.DISABLED)

    def auto_play(self):
        if not self.running:
            self.running = True
            self.auto_button.config(text="Dừng lại")
            self.step_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)
            self.animate()
        else:
            self.running = False
            self.auto_button.config(text="Tự động")
            if self.current_step < len(self.path):
                self.step_button.config(state=tk.NORMAL)
            if self.current_step > 1:
                self.prev_button.config(state=tk.NORMAL)

    def animate(self):
        if self.current_step < len(self.path) and self.running:
            self.current_step += 1
            self.update_board(self.path[self.current_step - 1])
            self.current_step_label.config(text=f"Bước hiện tại: {self.current_step}")
            self.window.after(500, self.animate)
        elif self.running:
            self.running = False
            self.auto_button.config(text="Tự động")
            self.step_info_label.config(text="Đã hoàn thành đường đi!")
            messagebox.showinfo("Thông báo", "Đã hoàn thành đường đi!")
            if self.current_step > 1:
                self.prev_button.config(state=tk.NORMAL)

    def reset(self):
        self.current_step = 1
        if self.path:
            self.update_board(self.path[0])
            if len(self.path) > 1:
                self.update_goal_board(self.path[-1])  # Khôi phục trạng thái mục tiêu cuối cùng
        self.current_step_label.config(text=f"Bước hiện tại: {self.current_step}")
        self.step_button.config(state=tk.NORMAL)
        self.auto_button.config(state=tk.NORMAL)
        self.prev_button.config(state=tk.DISABLED)
        self.running = False
        self.auto_button.config(text="Tự động")
        self.step_info_label.config(text="Đã reset! Nhấn 'Từng bước' hoặc 'Tự động' để xem lại.")

    def NoObsBeliefWindow(self, event=None):
        self.window.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoObsBeliefWindow(root)
    root.mainloop()