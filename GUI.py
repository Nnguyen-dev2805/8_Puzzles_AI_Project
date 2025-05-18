import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
import random
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import seaborn as sns

from backtracking_window import BacktrackingWindow
from partially_obs_belief_window import PartiallyObsBeliefWindow
from no_obs_belief_window import NoObsBeliefWindow
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import AI_algorithm

from algorithms import (
    bfs,
    dfs,
    greed_best_first_search,
    ucs,
    ids,
    astar,
    idastar,
    simple_hill_climbing,
    stochastic_hill_climbing,
    simulated_annealing,
    beam_search,
    genetic_search,
    and_or_graph_search,
    belief_state_search,
    backtracking,
    q_learning,
    no_observation_belief_state_search,
    partially_observable_search,
)  


class GUI:
    def __init__(self, master=None):
        self.master = master
        self.algorithm = None
        self.initialState = None
        self.statepointer = 0
        self.cost = 0  
        self.counter = 0  
        self.depth = 0 
        self.runtime = 0.0
        self.path = []
        self.memory_size = 0 
        self.runtime_data = {}
        self._job = None
        self.appFrame = ttk.Frame(master)
        self.appFrame.configure(height=800, width=1200)
        self.appFrame.pack(side="top")
        self.mainLabel = ttk.Label(self.appFrame)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()


        window_width = 1000
        window_height = 800

        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        self.master.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
       
        self.mainLabel.configure(
            anchor="center",
            font="{Roboto} 36 {bold}",
            foreground="#003e3e",
            justify="center",
            text="8-Puzzle Solver - Nhất Nguyên",
        )
        self.mainLabel.place(anchor="center", x=500, y=50)

        # prev button
        self.backbutton = ttk.Button(self.appFrame)
        self.img_backicon = tk.PhotoImage(file="assets/back-icon.png")
        self.backbutton.configure(cursor="hand2", image=self.img_backicon)
        self.backbutton.place(anchor="center", height=80, width=80, x=450, y=700)
        self.backbutton.bind("<ButtonPress>", self.prevSequence)

        # next button
        self.nextbutton = ttk.Button(self.appFrame)
        self.img_nexticon = tk.PhotoImage(file="assets/next-icon.png")
        self.nextbutton.configure(cursor="hand2", image=self.img_nexticon)
        self.nextbutton.place(anchor="center", height=80, width=80, x=550, y=700)
        self.nextbutton.bind("<ButtonPress>", self.nextSequence)

        # fast forward button
        self.fastforwardbutton = ttk.Button(self.appFrame)
        self.img_fastforwardicon = tk.PhotoImage(file="assets/fast-forward-icon.png")
        self.fastforwardbutton.configure(cursor="hand2", image=self.img_fastforwardicon)
        self.fastforwardbutton.place(anchor="center", height=80, width=80, x=650, y=700)
        self.fastforwardbutton.bind("<ButtonPress>", self.fastForward)

        # fast backward button
        self.fastbackwardbutton = ttk.Button(self.appFrame)
        self.img_fastbackwardicon = tk.PhotoImage(file="assets/fast-backward-icon.png")
        self.fastbackwardbutton.configure(
            cursor="hand2", image=self.img_fastbackwardicon
        )
        self.fastbackwardbutton.place(
            anchor="center", height=80, width=80, x=350, y=700
        )
        self.fastbackwardbutton.bind("<ButtonPress>", self.fastBackward)

        # stop button
        self.stopbutton = ttk.Button(self.appFrame)
        self.img_stopicon = tk.PhotoImage(file="assets/stop.png")
        self.stopbutton.configure(
            cursor="hand2", image=self.img_stopicon, state="disabled"
        )
        self.stopbutton.place(anchor="center", height=80, width=80, x=750, y=700)
        self.stopbutton.bind("<ButtonPress>", self.stopFastForward)

        # reset button
        self.resetbutton = ttk.Button(self.appFrame)
        self.img_reseticon = tk.PhotoImage(file="assets/reset-icon.png")
        self.resetbutton.configure(
            cursor="hand2", image=self.img_reseticon, state="disabled"
        )
        self.resetbutton.place(anchor="center", height=80, width=80, x=250, y=700)
        self.resetbutton.bind("<ButtonPress>", self.resetStepCounter)

        # đếm số bước chạy
        self.stepCount = ttk.Label(self.appFrame)
        self.stepCount.configure(
            anchor="center",
            background="#d6d6d6",
            font="{@Malgun Gothic Semilight} 12 {}",
            justify="center",
            text="0 / 0",
        )
        self.stepCount.place(anchor="center", width=200, x=500, y=640)

        # nút shuffle (thay thế contributors)
        self.shufflebutton = ttk.Button(self.appFrame)
        self.shufflebutton.configure(cursor="hand2", text="Tạo mới trạng thái")
        self.shufflebutton.place(anchor="n", height=40, width=150, x=910, y=680)
        self.shufflebutton.bind("<ButtonPress>", self.shuffle)

        # solve button
        self.solvebutton = ttk.Button(self.appFrame)
        self.img_solveicon = tk.PhotoImage(file="assets/solve-icon.png")
        self.solvebutton.configure(
            cursor="hand2", text="Giải", image=self.img_solveicon, compound="top"
        )
        self.solvebutton.place(anchor="s", height=150, width=150, x=910, y=300)
        self.solvebutton.bind("<ButtonPress>", self.solve)

        self.gif_loading = tk.Label(self.appFrame)

        # combobox để chọn thuật toán
        self.algorithmbox = ttk.Combobox(self.appFrame)
        self.algorithmbox.configure(
            cursor="hand2",
            state="readonly",
            values=(
                "BFS",
                "DFS",
                "Uniform Cost Search",
                "Iterative Deepening",
                "Greed Best First Search",
                "A*",
                "IDA*",    
                "Simple Hill Climbing",
                "Stochastic Hill Climbing",
                "Simulated Annealing",                
                "Genetic Search",
                "Beam Search",
                "AND OR Graph Search",
                "QLearning",
            ),
        )
        self.algorithmbox.place(anchor="center", height=30, width=150, x=910, y=330)
        self.algorithmbox.bind("<<ComboboxSelected>>", self.selectAlgorithm)

        # label chọn thuật toán
        self.algolabel = ttk.Label(self.appFrame)
        self.algolabel.configure(anchor="center", text="Chọn thuật toán:")
        self.algolabel.place(anchor="center", x=780, y=330)

        # hộp phân tích
        self.analysisbox = ttk.Label(self.appFrame)
        self.analysisbox.configure(
            anchor="center",
            text="",
            background="#d6d6d6",
            borderwidth=3,
            relief="sunken",
        )
        self.analysisbox.place(anchor="center", width=180, height=230, x=910, y=530)

        # nút in đường dẫn path xuất file excel
        self.exportFilebutton = ttk.Button(self.appFrame)
        self.exportFilebutton.configure(
            cursor="hand2", text="Xuất file toàn bộ đường dẫn"
        )
        self.exportFilebutton.place(anchor="n", height=40, width=180, x=500, y=580)
        self.exportFilebutton.bind("<ButtonPress>", self.exportFile)

        # nút vẽ biểu đồ so sánh runtime
        self.runtimeChartButton = ttk.Button(self.appFrame)
        self.runtimeChartButton.configure(cursor="hand2", text="Vẽ biểu đồ so sánh")
        self.runtimeChartButton.place(anchor="n", height=40, width=180, x=500, y=530)
        self.runtimeChartButton.bind("<ButtonPress>", self.drawRuntimeChart)


        # Thêm nút Backtracking vào giao diện chính
        self.backtracking_button = ttk.Button(self.appFrame)
        self.backtracking_button.configure(cursor="hand2", text="Backtracking")
        self.backtracking_button.place(anchor="n", height=40, width=150, x=120, y=600)
        self.backtracking_button.bind("<ButtonPress>", self.openBacktrackingWindow)

        # Thêm nút Partially obs Belief vào giao diện chính
        self.backtracking_button = ttk.Button(self.appFrame)
        self.backtracking_button.configure(cursor="hand2", text="Partially Obs Belief")
        self.backtracking_button.place(anchor="n", height=40, width=150, x=120, y=650)
        self.backtracking_button.bind("<ButtonPress>", self.PartiallyObsBeliefWindow)

        # Thêm nút No obs Belief vào giao diện chính
        self.backtracking_button = ttk.Button(self.appFrame)
        self.backtracking_button.configure(cursor="hand2", text="No Obs Belief")
        self.backtracking_button.place(anchor="n", height=40, width=150, x=120, y=700)
        self.backtracking_button.bind("<ButtonPress>", self.NoObsBeliefWindow)


        # tạo các ô cho puzzle
        self.cell0 = ttk.Label(self.appFrame)
        self.cell0.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell0.place(anchor="center", height=100, width=100, x=400, y=250)

        self.cell1 = ttk.Label(self.appFrame)
        self.cell1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text="1",
        )
        self.cell1.place(anchor="center", height=100, width=100, x=500, y=250)

        self.cell2 = ttk.Label(self.appFrame)
        self.cell2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text="2",
        )
        self.cell2.place(anchor="center", height=100, width=100, x=600, y=250)

        self.cell3 = ttk.Label(self.appFrame)
        self.cell3.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text="3",
        )
        self.cell3.place(anchor="center", height=100, width=100, x=400, y=350)

        self.cell4 = ttk.Label(self.appFrame)
        self.cell4.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text="4",
        )
        self.cell4.place(anchor="center", height=100, width=100, x=500, y=350)

        self.cell5 = ttk.Label(self.appFrame)
        self.cell5.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text="5",
        )
        self.cell5.place(anchor="center", height=100, width=100, x=600, y=350)

        self.cell6 = ttk.Label(self.appFrame)
        self.cell6.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text="6",
        )
        self.cell6.place(anchor="center", height=100, width=100, x=400, y=450)

        self.cell7 = ttk.Label(self.appFrame)
        self.cell7.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text="7",
        )
        self.cell7.place(anchor="center", height=100, width=100, x=500, y=450)

        self.cell8 = ttk.Label(self.appFrame)
        self.cell8.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 48 {}",
            justify="center",
            relief="sunken",
            text="8",
        )
        self.cell8.place(anchor="center", height=100, width=100, x=600, y=450)

        # tạo các ô cho puzzle để hiện trạng thái ban đầu

        self.first_Label = ttk.Label(self.appFrame)

        self.first_Label.configure(
            anchor="center",
            font="{Roboto} 14 {bold}",
            foreground="#003e3e",
            justify="center",
            text="Trạng thái ban đầu",
        )
        self.first_Label.place(anchor="center", x=120, y=120)

        self.cell0_1 = ttk.Label(self.appFrame)
        self.cell0_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell0_1.place(anchor="center", height=50, width=50, x=70, y=180)

        self.cell1_1 = ttk.Label(self.appFrame)
        self.cell1_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell1_1.place(anchor="center", height=50, width=50, x=120, y=180)

        self.cell2_1 = ttk.Label(self.appFrame)
        self.cell2_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell2_1.place(anchor="center", height=50, width=50, x=170, y=180)

        self.cell3_1 = ttk.Label(self.appFrame)
        self.cell3_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell3_1.place(anchor="center", height=50, width=50, x=70, y=230)

        self.cell4_1 = ttk.Label(self.appFrame)
        self.cell4_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell4_1.place(anchor="center", height=50, width=50, x=120, y=230)

        self.cell5_1 = ttk.Label(self.appFrame)
        self.cell5_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell5_1.place(anchor="center", height=50, width=50, x=170, y=230)

        self.cell6_1 = ttk.Label(self.appFrame)
        self.cell6_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell6_1.place(anchor="center", height=50, width=50, x=70, y=280)

        self.cell7_1 = ttk.Label(self.appFrame)
        self.cell7_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell7_1.place(anchor="center", height=50, width=50, x=120, y=280)

        self.cell8_1 = ttk.Label(self.appFrame)
        self.cell8_1.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell8_1.place(anchor="center", height=50, width=50, x=170, y=280)

        # tạo các ô cho puzzle để hiện trạng thái mục tiêu

        self.last_Label = ttk.Label(self.appFrame)

        self.last_Label.configure(
            anchor="center",
            font="{Roboto} 14 {bold}",
            foreground="#003e3e",
            justify="center",
            text="Trạng thái mục tiêu",
        )
        self.last_Label.place(anchor="center", x=120, y=380)

        self.cell0_2 = ttk.Label(self.appFrame)
        self.cell0_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text="1",
        )
        self.cell0_2.place(anchor="center", height=50, width=50, x=70, y=440)

        self.cell1_2 = ttk.Label(self.appFrame)
        self.cell1_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text="2",
        )
        self.cell1_2.place(anchor="center", height=50, width=50, x=120, y=440)

        self.cell2_2 = ttk.Label(self.appFrame)
        self.cell2_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text="3",
        )
        self.cell2_2.place(anchor="center", height=50, width=50, x=170, y=440)

        self.cell3_2 = ttk.Label(self.appFrame)
        self.cell3_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text="4",
        )
        self.cell3_2.place(anchor="center", height=50, width=50, x=70, y=490)

        self.cell4_2 = ttk.Label(self.appFrame)
        self.cell4_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text="5",
        )
        self.cell4_2.place(anchor="center", height=50, width=50, x=120, y=490)

        self.cell5_2 = ttk.Label(self.appFrame)
        self.cell5_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text="6",
        )
        self.cell5_2.place(anchor="center", height=50, width=50, x=170, y=490)

        self.cell6_2 = ttk.Label(self.appFrame)
        self.cell6_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text="7",
        )
        self.cell6_2.place(anchor="center", height=50, width=50, x=70, y=540)

        self.cell7_2 = ttk.Label(self.appFrame)
        self.cell7_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text="8",
        )
        self.cell7_2.place(anchor="center", height=50, width=50, x=120, y=540)

        self.cell8_2 = ttk.Label(self.appFrame)
        self.cell8_2.configure(
            anchor="center",
            background="#5aadad",
            borderwidth=3,
            font="{Franklin Gothic Medium} 20 {}",
            justify="center",
            relief="sunken",
            text=" ",
        )
        self.cell8_2.place(anchor="center", height=50, width=50, x=170, y=540)

        # nút nhập ma trận
        self.enterstatebutton = ttk.Button(self.appFrame)
        self.img_inputicon = tk.PhotoImage(file="assets/input-icon.png")
        self.enterstatebutton.configure(
            cursor="hand2",
            text="Nhập trạng thái đầu",
            image=self.img_inputicon,
            compound="left",
        )
        self.enterstatebutton.place(anchor="n", width=150, x=910, y=350)
        self.enterstatebutton.bind("<ButtonPress>", self.enterInitialState)

        # dark mode
        self.is_dark_mode = False  # Track the current theme
        self.darkmodebutton = ttk.Button(self.appFrame)
        self.darkmodebutton.configure(cursor="hand2", text="Chế độ tối")
        self.darkmodebutton.place(anchor="n", height=40, width=150, x=910, y=740)
        self.darkmodebutton.bind("<ButtonPress>", self.toggleDarkMode)

        self.mainwindow = self.appFrame

        self.gif = [
            tk.PhotoImage(file="assets/loading.gif", format="gif -index %i" % i)
            for i in range(10)
        ]

    def run(self):
        self.displayStateOnGrid("000000000")
        self.gif_loading.place_forget()
        self.refreshFrame()
        self.mainwindow.after(0, self.refreshGIF, 0)
        self.mainwindow.mainloop()

    # ------------ Chức năng của mấy cái nút ---------------

    def refreshGIF(self, ind):
        frame = self.gif[ind]
        ind = (ind + 1) % 10
        self.gif_loading.configure(image=frame)
        self.appFrame.after(50, self.refreshGIF, ind)

    def prevSequence(self, event=None):
        if self.statepointer > 0:
            self.stopFastForward()
            self.statepointer -= 1
            self.refreshFrame()
    
    def selectAlgorithmFromTree(self, event=None):
        selected_item = self.algorithm_tree.selection()[0]
        algorithm = self.algorithm_tree.item(selected_item, "text")
        if algorithm not in ["Uninformed Search", "Informed Search", "Local Search", "Non-deterministic Search"]:
            self.algorithm = algorithm
            self.reset()

    def PartiallyObsBeliefWindow(self, event=None):
        PartiallyObsBeliefWindow(self.master)
    
    def NoObsBeliefWindow(self, event=None):
        NoObsBeliefWindow(self.master)

    def openBacktrackingWindow(self, event=None):
        BacktrackingWindow(self.master)

    def create_backtracking_board(self, window):
        # Tạo frame chính cho bảng
        board_frame = ttk.Frame(window)
        board_frame.pack(pady=20)  # Dùng pack() cho frame chính
        
        # Tạo frame riêng cho bảng 3x3 (chỉ dùng grid() trong frame này)
        grid_frame = ttk.Frame(board_frame)
        grid_frame.pack()  # Dùng pack() để đặt grid_frame vào board_frame
        
        self.backtracking_tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                tile = tk.Label(
                    grid_frame,  # Sử dụng grid_frame thay vì board_frame
                    text="",
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2,
                    relief="raised",
                    bg="white"
                )
                tile.grid(row=i, column=j, padx=2, pady=2)  # Dùng grid() trong grid_frame
                row.append(tile)
            self.backtracking_tiles.append(row)
        
        # Tạo frame riêng cho mục tiêu (dùng pack() hoặc grid() riêng biệt)
        goal_frame = ttk.Frame(window)
        goal_frame.pack(pady=10)
        
        tk.Label(goal_frame, text="Mục tiêu:", font=("Arial", 12)).pack()
        
        # Tạo frame riêng cho bảng mục tiêu (chỉ dùng grid() trong frame này)
        goal_grid_frame = ttk.Frame(goal_frame)
        goal_grid_frame.pack()
        
        goal_state = [1,2,3,4,5,6,7,8,0]
        for i in range(3):
            for j in range(3):
                idx = i*3 + j
                val = goal_state[idx] if goal_state[idx] != 0 else ""
                tk.Label(
                    goal_grid_frame,  # Sử dụng goal_grid_frame thay vì goal_frame
                    text=str(val),
                    font=("Arial", 16),
                    width=4,
                    height=2,
                    relief="sunken"
                ).grid(row=i, column=j, padx=2, pady=2)
    
    def start_backtracking(self, window):
        # Khởi tạo trạng thái ban đầu (rỗng)
        initial_state = [0]*9  # 0 đại diện cho ô trống
        self.backtracking_solution = []
        self.current_step = 0
        
        # Tìm giải pháp
        if self.solve_backtracking(initial_state, 0):
            self.backtracking_steps = self.backtracking_solution.copy()
            self.update_backtracking_board(self.backtracking_steps[0])
            self.step_button.config(state=tk.NORMAL)
            self.auto_button.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy giải pháp")

    def solve_backtracking(self, state, position):
        # Điều kiện dừng: nếu đã điền hết tất cả ô
        if position == 9:
            return True
        
        # Giá trị mong muốn tại vị trí hiện tại (1-8, ô cuối là 0)
        desired_value = position + 1 if position < 8 else 0
        
        # Nếu ô đã có giá trị đúng thì chuyển sang ô tiếp theo
        if state[position] == desired_value:
            return self.solve_backtracking(state, position + 1)
        
        # Nếu ô đã có giá trị khác (không phải 0) thì không hợp lệ
        if state[position] != 0:
            return False
        
        # Thử điền giá trị mong muốn vào ô trống
        state[position] = desired_value
        self.backtracking_solution.append(state.copy())
        
        # Tiếp tục đệ quy
        if self.solve_backtracking(state, position + 1):
            return True
        
        # Backtrack nếu không thành công
        state[position] = 0
        self.backtracking_solution.append(state.copy())
        return False
    def update_backtracking_board(self, state):
        for i in range(3):
            for j in range(3):
                idx = i*3 + j
                value = state[idx] if state[idx] != 0 else ""
                self.backtracking_tiles[i][j].config(text=str(value))
        
        # Highlight ô đang được xử lý
        for i in range(9):
            if state[i] == 0 or (i < 8 and state[i] != i+1):
                row, col = i//3, i%3
                self.backtracking_tiles[row][col].config(bg="lightyellow")
                break

    def next_backtracking_step(self):
        if self.current_step < len(self.backtracking_steps):
            self.update_backtracking_board(self.backtracking_steps[self.current_step])
            self.current_step += 1
        else:
            self.step_button.config(state=tk.DISABLED)
            messagebox.showinfo("Thông báo", "Đã hoàn thành backtracking!")

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
            self.update_backtracking_board(self.backtracking_steps[self.current_step])
            self.current_step += 1
            self.master.after(500, self.animate_backtracking)  # Cập nhật mỗi 0.5 giây
        elif self.backtracking_running:
            self.backtracking_running = False
            self.auto_button.config(text="Tự động")
            messagebox.showinfo("Thông báo", "Đã hoàn thành backtracking!")
    
    def runBacktracking(self, cells):
        """Thực hiện thuật toán Backtracking và cập nhật giao diện."""

        def update_grid(board, status, cells):
            """Cập nhật bảng 8-puzzle trên giao diện."""
            for i in range(3):
                for j in range(3):
                    value = board[i * 3 + j]
                    cells[i][j].configure(
                        text=value if value is not None else "",
                        background="#5aadad" if value is not None else "#ffffff",
                    )
                    
        solver = backtracking.Backtracking8Puzzle(update_callback=lambda board, status: update_grid(board, status, cells))
        solver.solve()

    def nextSequence(self, event=None):
        if self.statepointer < len(self.path) - 1:
            self.stopFastForward()
            self.statepointer += 1
            self.refreshFrame()

    def solve(self, event=None):
        self.gif_loading.place(x=800, y=300, anchor="s")
        if self.readyToSolve():
            msg = (
                "Thuật toán: "
                + str(self.algorithm)
                + "\nTrạng thái ban đầu = "
                + str(self.initialState)
            )
            messagebox.showinfo("Xác nhận dữ liệu", msg)
            self.resetGrid()
            self.solveState()
            if len(self.path) == 0:
                messagebox.showinfo(
                    "Không thể giải", "Trạng thái ban đầu không thể giải!"
                )
                self.displaySearchAnalysis(True)
            else:
                self.refreshFrame()
        else:
            solvingerror = (
                "Không thể giải.\n"
                "Thuật toán sử dụng: " + str(self.algorithm) + "\n"
                "Trạng thái ban đầu   : " + str(self.initialState)
            )
            messagebox.showerror("Không thể giải!", solvingerror)
        self.gif_loading.place_forget()

    def enterInitialState(self, event=None):
        inputState = simpledialog.askstring(
            "Nhập trạng thái ban đầu", "Vui lòng nhập trạng thái ban đầu!"
        )
        if inputState is not None:
            if self.validateState(inputState):
                # kiểm tra số nghịch thế
                inversions = self.countInversions(inputState)
                if inversions % 2 != 0:  # Nnu số nghịch thế là lẻ, không giải được
                    messagebox.showerror(
                        "Lỗi đầu vào",
                        "Trạng thái ban đầu không thể giải được (số nghịch thế là lẻ)!",
                    )
                    return
                if (
                    inputState != self.initialState
                ):  # Only reset runtime_data if the state changes
                    self.initialState = inputState
                    self.runtime_data = {}  # Reset runtime data
                self.reset()
                self.displayStateOnGrid(self.initialState)
                self.updateInitialStateGrid(self.initialState)
            else:
                messagebox.showerror("Lỗi đầu vào", "Trạng thái ban đầu không hợp lệ!")

    def selectAlgorithm(self, event=None):
        try:
            choice = self.algorithmbox.get()
            self.reset()
            self.algorithm = choice
            # self.runtime_data = {}
        except:
            pass

    def exportFile(self, event=None):
        if not self.solved():
            messagebox.showwarning(
                "Cảnh báo", "Chưa có đường dẫn để xuất! Vui lòng nhấn Solve trước."
            )
            return

        file_name = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"{self.algorithm}_path",
            title="Chọn nơi lưu file Excel",
        )
        if not file_name:
            return

        data = []
        for i, state in enumerate(self.path):
            state_str = AI_algorithm.getStringRepresentation(state)
            matrix = [
                [
                    self.adjustDigit(state_str[0]),
                    self.adjustDigit(state_str[1]),
                    self.adjustDigit(state_str[2]),
                ],
                [
                    self.adjustDigit(state_str[3]),
                    self.adjustDigit(state_str[4]),
                    self.adjustDigit(state_str[5]),
                ],
                [
                    self.adjustDigit(state_str[6]),
                    self.adjustDigit(state_str[7]),
                    self.adjustDigit(state_str[8]),
                ],
            ]
            data.append(
                {"Bước": f"Ma trận bước {i}", "Cột 1": "", "Cột 2": "", "Cột 3": ""}
            )
            data.append(
                {
                    "Bước": "",
                    "Cột 1": matrix[0][0],
                    "Cột 2": matrix[0][1],
                    "Cột 3": matrix[0][2],
                }
            )
            data.append(
                {
                    "Bước": "",
                    "Cột 1": matrix[1][0],
                    "Cột 2": matrix[1][1],
                    "Cột 3": matrix[1][2],
                }
            )
            data.append(
                {
                    "Bước": "",
                    "Cột 1": matrix[2][0],
                    "Cột 2": matrix[2][1],
                    "Cột 3": matrix[2][2],
                }
            )
            data.append({"Bước": "", "Cột 1": "", "Cột 2": "", "Cột 3": ""})

        df = pd.DataFrame(data)

        analysis_data = {
            "Thuật toán": [str(self.algorithm)],
            "Trạng thái ban đầu": [str(self.initialState)],
            "Số trạng thái đã duyệt qua": [self.counter],
            "Độ sâu": [self.depth],
            "Chi phí": [self.cost],
            "Thời gian chạy (s)": [self.runtime],
        }
        analysis_df = pd.DataFrame(analysis_data)

        try:
            with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Đường dẫn", index=False)
                analysis_df.to_excel(writer, sheet_name="Phân tích", index=False)
            messagebox.showinfo("Thành công", f"Đã xuất đường dẫn ra file: {file_name}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def fastForward(self, event=None):
        self.stopFastForward()
        if self.statepointer < self.cost:
            self.stopbutton.configure(state="enabled")
            self.statepointer += 1
            self.refreshFrame()
            ms = 100
            if 100 < self.cost <= 1000:
                ms = 20
            if self.cost > 1000:
                ms = 1
            self._job = self.stepCount.after(ms, self.fastForward)
        else:
            self.stopFastForward()

    def fastBackward(self, event=None):
        self.stopFastForward()
        if self.statepointer > 0:
            self.stopbutton.configure(state="enabled")
            self.statepointer -= 1
            ms = 50
            if self.cost > 1000:
                ms = 1
            self._job = self.stepCount.after(ms, self.fastBackward)
        else:
            self.stopFastForward()
        self.refreshFrame()

    def stopFastForward(self, event=None):
        if self._job is not None:
            self.stopbutton.configure(state="disabled")
            self.stepCount.after_cancel(self._job)
            self._job = None

    def resetStepCounter(self, event=None):
        if self.statepointer > 0:
            self.stopFastForward()
            self.statepointer = 0
            self.refreshFrame()

    def shuffle(self, event=None):
        while True:
            puzzle = list("012345678")
            random.shuffle(puzzle)
            self.initialState = "".join(puzzle)
            # Kiểm tra số nghịch thế
            inversions = self.countInversions(self.initialState)
            if inversions % 2 == 0:  # nếu số nghịch thế là chẵn, trạng thái giải được
                break
        self.reset()
        # self.displayImageOnGrid(self.initialState)
        self.displayStateOnGrid(self.initialState)
        self.updateInitialStateGrid(self.initialState)
        messagebox.showinfo(
            "Trạng thái mới", f"Trạng thái ban đầu: {self.initialState}"
        )

    def displayStateOnGrid(self, state):
        if not self.validateState(state):
            state = "000000000"
        self.cell0.configure(text=self.adjustDigit(state[0]))
        self.cell1.configure(text=self.adjustDigit(state[1]))
        self.cell2.configure(text=self.adjustDigit(state[2]))
        self.cell3.configure(text=self.adjustDigit(state[3]))
        self.cell4.configure(text=self.adjustDigit(state[4]))
        self.cell5.configure(text=self.adjustDigit(state[5]))
        self.cell6.configure(text=self.adjustDigit(state[6]))
        self.cell7.configure(text=self.adjustDigit(state[7]))
        self.cell8.configure(text=self.adjustDigit(state[8]))

    def updateInitialStateGrid(self, state):
        self.cell0_1.configure(text=self.adjustDigit(state[0]))
        self.cell1_1.configure(text=self.adjustDigit(state[1]))
        self.cell2_1.configure(text=self.adjustDigit(state[2]))
        self.cell3_1.configure(text=self.adjustDigit(state[3]))
        self.cell4_1.configure(text=self.adjustDigit(state[4]))
        self.cell5_1.configure(text=self.adjustDigit(state[5]))
        self.cell6_1.configure(text=self.adjustDigit(state[6]))
        self.cell7_1.configure(text=self.adjustDigit(state[7]))
        self.cell8_1.configure(text=self.adjustDigit(state[8]))

    def toggleDarkMode(self, event=None):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.applyDarkMode()
            self.darkmodebutton.configure(text="Chế độ sáng")
        else:
            self.applyLightMode()
            self.darkmodebutton.configure(text="Chế độ tối")

    def applyDarkMode(self):
        self.appFrame.configure(style="Dark.TFrame")
        self.mainLabel.configure(foreground="#ff0000")
        self.analysisbox.configure(background="#333333", foreground="#ffffff")
        self.stepCount.configure(background="#333333", foreground="#ffffff")
        for cell in [
            self.cell0,
            self.cell1,
            self.cell2,
            self.cell3,
            self.cell4,
            self.cell5,
            self.cell6,
            self.cell7,
            self.cell8,
            self.cell0_1,
            self.cell1_1,
            self.cell2_1,
            self.cell3_1,
            self.cell4_1,
            self.cell5_1,
            self.cell6_1,
            self.cell7_1,
            self.cell8_1,
            self.cell0_2,
            self.cell1_2,
            self.cell2_2,
            self.cell3_2,
            self.cell4_2,
            self.cell5_2,
            self.cell6_2,
            self.cell7_2,
            self.cell8_2,
        ]:
            cell.configure(background="#444444", foreground="#ffffff")

    def applyLightMode(self):
        self.appFrame.configure(style="Light.TFrame")
        self.mainLabel.configure(foreground="#003e3e")
        self.analysisbox.configure(background="#d6d6d6", foreground="#000000")
        self.stepCount.configure(background="#d6d6d6", foreground="#000000")
        for cell in [
            self.cell0,
            self.cell1,
            self.cell2,
            self.cell3,
            self.cell4,
            self.cell5,
            self.cell6,
            self.cell7,
            self.cell8,
            self.cell0_1,
            self.cell1_1,
            self.cell2_1,
            self.cell3_1,
            self.cell4_1,
            self.cell5_1,
            self.cell6_1,
            self.cell7_1,
            self.cell8_1,
            self.cell0_2,
            self.cell1_2,
            self.cell2_2,
            self.cell3_2,
            self.cell4_2,
            self.cell5_2,
            self.cell6_2,
            self.cell7_2,
            self.cell8_2,
        ]:
            cell.configure(background="#5aadad", foreground="#000000")

    # ------------- Các hàm hỗ trợ -----------------

    @staticmethod
    def validateState(inputState):
        seen = []
        if inputState is None or len(inputState) != 9 or not inputState.isnumeric():
            return False
        for dig in inputState:
            if dig in seen or dig == "9":
                return False
            seen.append(dig)
        return True

    @staticmethod
    def adjustDigit(digit):
        if digit == "0":
            return " "
        return digit

    def refreshFrame(self):
        if self.cost > 0:
            state = AI_algorithm.getStringRepresentation(self.path[self.statepointer])
            self.displayStateOnGrid(state)
            self.stepCount.configure(text=self.getStepCountString())
            self.displaySearchAnalysis()
        if self.statepointer == 0:
            self.resetbutton.configure(state="disabled")
            self.backbutton.configure(state="disabled")
            self.fastbackwardbutton.configure(state="disabled")
        else:
            self.resetbutton.configure(state="enabled")
            self.backbutton.configure(state="enabled")
            self.fastbackwardbutton.configure(state="enabled")
        if self.cost == 0 or self.statepointer == self.cost:
            self.fastforwardbutton.configure(state="disabled")
            self.nextbutton.configure(state="disabled")
        else:
            self.fastforwardbutton.configure(state="enabled")
            self.nextbutton.configure(state="enabled")

    def getStepCountString(self):
        return str(self.statepointer) + "/" + str(self.cost)

    @staticmethod
    def countInversions(state):
        # chuyển trạng thái thành danh sách, bỏ qua ô trống (0)
        state_list = [int(d) for d in state if d != "0"]
        inversions = 0
        # đếm số nghịch thế
        for i in range(len(state_list)):
            for j in range(i + 1, len(state_list)):
                if state_list[i] > state_list[j]:
                    inversions += 1
        return inversions

    def displaySearchAnalysis(self, force_display=False):
        if self.solved() or force_display is True:
            analytics = (
                "Phân tích của thuật toán:\n"
                + str(self.algorithm)
                + "\nTrạng thái ban đầu:\n"
                + str(self.initialState)
            )
            if force_display:
                analytics += "\n< Không thể giải >"
            analytics += (
                "\n-------------------------------"
                "\n"
                + "Số trạng thái đã duyệt qua: \n"
                + str(self.counter)
                + "\n"
                + "Độ sâu: \n"
                + str(self.depth)
                + "\n"
                + "Chi phí: \n"
                + str(self.cost)
                + "\n"
                + "Thời gian chạy: \n"
                + str(self.runtime)
                + " s"
                + "\nKích thước bộ nhớ: \n"
                + str(self.memory_size)
            )
        else:
            analytics = ""
        self.analysisbox.configure(text=analytics)

    def solved(self):
        return len(self.path) > 0

    def readyToSolve(self):
        return self.initialState is not None and self.algorithm is not None

    def resetGrid(self):
        self.statepointer = 0
        self.refreshFrame()
        self.stepCount.configure(text=self.getStepCountString())

    def solveState(self):
        if self.algorithm == "BFS":
            self.solveBFS()

        elif str(self.algorithm) == "DFS":
            self.solveDFS()

        elif str(self.algorithm) == "Uniform Cost Search":
            self.solveUCS()

        elif str(self.algorithm) == "Iterative Deepening":
            self.solveIDS()

        elif str(self.algorithm) == "Greed Best First Search":
            self.solveGreedBestFirstSearch()
        
        elif str(self.algorithm) == "A*":
            self.solveAStar()

        elif str(self.algorithm) == "IDA*":
            self.solveIDAStar()

        elif str(self.algorithm) == "Simple Hill Climbing":
            self.solveSimpleHillClimbing()
        
        elif str(self.algorithm) == "Stochastic Hill Climbing":
            self.solveStochasticHillClimbing()

        elif str(self.algorithm) == "Simulated Annealing":
            self.solveSimulatedAnnealing()

        elif str(self.algorithm) == "Beam Search":
            self.solveBeamSearch()
        elif str(self.algorithm) == "Genetic Search":
            self.solveGeneticSearch()

        elif str(self.algorithm) == "AND OR Graph Search":
            self.solveAndOrGraphSearch()
        
        elif str(self.algorithm) == "Belief State Search":
            self.solveBeliefStateSearch()

        elif str(self.algorithm) == "QLearning":
            self.solveQLearning()

        if self.algorithm and self.initialState:
            self.runtime_data[self.algorithm] = {
                "depth": self.depth,
                "memory_size": self.memory_size,
                "runtime": self.runtime,
                # "cost": self.cost,
                "counter": self.counter,
                # "depth": self.depth,
            }

    def reset(self):
        self.path = []
        self.cost = self.counter = 0
        self.runtime = 0.0
        self.resetGrid()
        self.analysisbox.configure(text="")

    # ----------------- Các thuật toán ------------------

    def solveBFS(self):
        bfs_solver = bfs.BFSAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = bfs_solver.BFS(
            self.initialState
        )

    def solveDFS(self):
        dfs_solver = dfs.DFSAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = dfs_solver.DFS(
            self.initialState
        )

    def solveUCS(self):
        ucs_solver = ucs.UCSAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = ucs_solver.UCS(
            self.initialState
        )

    def solveIDS(self):
        ids_solver = ids.IDSAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = ids_solver.IDS(
            self.initialState
        )
    
    def solveGreedBestFirstSearch(self):
        best_first_solver = greed_best_first_search.GreedBestFirstSearchAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = best_first_solver.BestFirstSearch(
            self.initialState
        )
    
    def solveAStar(self):
        astar_solver = astar.AStarAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = astar_solver.AStar(
            self.initialState
        )
    
    def solveIDAStar(self):
        ida_star_solver = idastar.IDAStarAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = ida_star_solver.IDAStar(
            self.initialState
        )
    
    def solveSimpleHillClimbing(self):
        simple_hill_climbing_solver = simple_hill_climbing.SimpleHillClimbingAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = simple_hill_climbing_solver.SimpleHillClimbing(
            self.initialState
        )
    
    def solveStochasticHillClimbing(self):
        stochastic_hill_climbing_solver = stochastic_hill_climbing.StochasticHillClimbingAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = stochastic_hill_climbing_solver.StochasticHillClimbing(
            self.initialState
        )

    def solveSimulatedAnnealing(self):
        simulated_annealing_solver = simulated_annealing.SimulatedAnnealingAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtim,self.memory_size = simulated_annealing_solver.SimulatedAnnealing(
            self.initialState
        )

    def solveBeamSearch(self):
        beam_search_solver = beam_search.BeamSearchAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size= beam_search_solver.BeamSearch(
            self.initialState
        )
    
    def solveGeneticSearch(self):
        genetic_search_solver = genetic_search.GeneticAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = genetic_search_solver.GeneticSearch(
            self.initialState
        )
    
    def solveAndOrGraphSearch(self):
        and_or_graph_search_solver = and_or_graph_search.AndOrGraphSearchAlgorithm()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = and_or_graph_search_solver.AndOrGraphSearch(
            self.initialState,123456780
        )
    
    def solveQLearning(self):
        q_learning_solver = q_learning.QLearning()
        self.path, self.cost, self.counter, self.depth, self.runtime,self.memory_size = q_learning_solver.train(
            self.initialState,123456780
        )

    
    # ----------------- Vẽ biểu đồ ------------------

    def drawRuntimeChart(self, event=None):
        if not self.runtime_data: 
            return
        
        algorithms = list(self.runtime_data.keys())
        metrics = {
            "Thời gian chạy (s)": [],
            "Kích thước bộ nhớ (node)": [],
            "Số trạng thái duyệt": [],
            "Độ sâu lời giải": []
        }

        for algo in algorithms:
            runtime = self.runtime_data[algo].get("runtime", 0)
            metrics["Thời gian chạy (s)"].append(runtime)  
            
            metrics["Kích thước bộ nhớ (node)"].append(self.runtime_data[algo].get("memory_size", 0))
            metrics["Số trạng thái duyệt"].append(self.runtime_data[algo].get("counter", 0))
            metrics["Độ sâu lời giải"].append(self.runtime_data[algo].get("depth", 0))

        fig = make_subplots(
            rows=2, 
            cols=2, 
            subplot_titles=list(metrics.keys()),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
        marker_symbols = ['circle', 'square', 'diamond', 'cross']
        
        for i, (name, values) in enumerate(metrics.items()):
            row = (i//2)+1
            col = (i%2)+1
            
            text_values = []
            for v in values:
                if name == "Thời gian chạy (s)":
                    text_values.append(f'{v:.3f}'.rstrip('0').rstrip('.') if '.' in f'{v:.3f}' else f'{v:.3f}')
                else:
                    text_values.append(f'{v:,}' if isinstance(v, (int, float)) else str(v))
            
            fig.add_trace(
                go.Scatter(
                    x=algorithms,
                    y=values,
                    name=name,
                    mode='lines+markers+text',
                    text=text_values,
                    textposition='top center',
                    marker=dict(
                        size=12,
                        color=colors[i],
                        symbol=marker_symbols[i],
                        line=dict(width=2, color='DarkSlateGrey')
                    ),
                    line=dict(width=3, color=colors[i]),
                    textfont=dict(size=11, color=colors[i]),
                    hoverinfo='x+y+name',
                    hoverlabel=dict(bgcolor='white', font_size=12)
                ),
                row=row, col=col
            )

            if name == "Thời gian chạy (s)":
                min_val = min(values)
                max_val = max(values)

                y_range = [
                    min_val * 0.9 if min_val > 0 else -0.1 * max_val,
                    max_val * 1.2
                ]
                
                fig.update_yaxes(
                    tickformat=".3f",  
                    range=y_range,
                    row=row, col=col
                )
        
        fig.update_layout(
            title_text='<b>SO SÁNH HIỆU SUẤT THUẬT TOÁN</b>',
            title_font=dict(size=22, family='Arial', color='black'),
            title_x=0.5,
            showlegend=False,
            height=850,
            width=1000,
            template='plotly_white',
            margin=dict(l=50, r=50, b=50, t=100, pad=4),
            hovermode='x unified',
            plot_bgcolor='rgba(245,245,245,0.8)'
        )
        
        fig.update_xaxes(
            tickangle=-30,
            tickfont=dict(size=10),
            showline=True,
            linecolor='gray',
            mirror=True
        )
        
        fig.update_yaxes(
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='lightgray',
            showline=True,
            linecolor='gray',
            mirror=True,
            # tickformat=',.0f'  # Định dạng số
        )
        
        fig.update_annotations(
            font_size=13,
            yshift=10
        )
        
        fig.show(config={'displayModeBar': True})