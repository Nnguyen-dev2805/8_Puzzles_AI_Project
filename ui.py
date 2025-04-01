import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
import random
import pandas as pd
from tkinter import filedialog

import AI_algorithm

# Khởi tạo các biến toàn cục
algorithm = None
initialState = None
statepointer = cost = counter = depth = 0
runtime = 0.0
path = []


class GUI:
    def __init__(self, master=None):
        self._job = None
        self.appFrame = ttk.Frame(master)
        self.appFrame.configure(height=800, width=1000)
        self.appFrame.pack(side="top")
        self.mainLabel = ttk.Label(self.appFrame)

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
        self.shufflebutton.configure(cursor="hand2", text="Shuffle")
        self.shufflebutton.place(anchor="n",height= 40, width=150, x=910, y=680)
        self.shufflebutton.bind("<ButtonPress>", self.shuffle)

        # solve button
        self.solvebutton = ttk.Button(self.appFrame)
        self.img_solveicon = tk.PhotoImage(file="assets/solve-icon.png")
        self.solvebutton.configure(
            cursor="hand2", text="Solve", image=self.img_solveicon, compound="top"
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
                "Best first search",
                "A*",
                "IDA*",
                "Simple Hill Climbing"
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
        self.exportFilebutton.configure(cursor="hand2", text="Xuất file toàn bộ đường dẫn")
        self.exportFilebutton.place(anchor="n",height= 40, width=180, x=500, y=580)
        self.exportFilebutton.bind("<ButtonPress>", self.exportFile)

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
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer -= 1
            self.refreshFrame()

    def nextSequence(self, event=None):
        global statepointer
        if statepointer < len(path) - 1:
            self.stopFastForward()
            statepointer += 1
            self.refreshFrame()

    def solve(self, event=None):
        global algorithm, initialState
        self.gif_loading.place(x=800, y=300, anchor="s")
        if self.readyToSolve():
            msg = (
                "Thuật toán: "
                + str(algorithm)
                + "\nTrạng thái ban đầu = "
                + str(initialState)
            )
            messagebox.showinfo("Xác nhận dữ liệu", msg)
            self.resetGrid()
            self.solveState()
            if len(path) == 0:
                messagebox.showinfo(
                    "Không thể giải", "Trạng thái ban đầu không thể giải!"
                )
                self.displaySearchAnalysis(True)
            else:
                self.refreshFrame()
        else:
            solvingerror = (
                "Không thể giải.\n"
                "Thuật toán sử dụng: " + str(algorithm) + "\n"
                "Trạng thái ban đầu   : " + str(initialState)
            )
            messagebox.showerror("Không thể giải!", solvingerror)
        self.gif_loading.place_forget()

    def enterInitialState(self, event=None):
        global initialState, statepointer
        inputState = simpledialog.askstring(
            "Nhập trạng thái ban đầu", "Vui lòng nhập trạng thái ban đầu!"
        )
        if inputState is not None:
            if self.validateState(inputState):
                # kiểm tra số nghịch thế
                inversions = self.countInversions(inputState)
                if inversions % 2 != 0:  # Nnu số nghịch thế là lẻ, không giải được
                    messagebox.showerror("Lỗi đầu vào", "Trạng thái ban đầu không thể giải được (số nghịch thế là lẻ)!")
                    return
                initialState = inputState
                self.reset()
                self.displayStateOnGrid(initialState)
                self.updateInitialStateGrid(initialState)
            else:
                messagebox.showerror("Lỗi đầu vào", "Trạng thái ban đầu không hợp lệ!")

    def selectAlgorithm(self, event=None):
        global algorithm
        try:
            choice = self.algorithmbox.get()
            self.reset()
            algorithm = choice
        except:
            pass
    def exportFile(self, event=None):
        global path, algorithm, initialState
        if not self.solved():
            messagebox.showwarning("Cảnh báo", "Chưa có đường dẫn để xuất! Vui lòng nhấn Solve trước.")
            return
        
        # hỏi người dùng chọn nơi lưu file và tên file
        file_name = filedialog.asksaveasfilename(
            defaultextension=".xlsx",  # đuôi mặc định là .xlsx
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],  # các loại file hỗ trợ
            initialfile=f"{algorithm}_path",  # tên file mặc định
            title="Chọn nơi lưu file Excel"
        )
        if not file_name:  # nếu người dùng hủy
            return

        # chuẩn bị dữ liệu cho sheet "Đường dẫn"
        data = []
        for i, state in enumerate(path):
            state_str = AI_algorithm.getStringRepresentation(state)
            matrix = [
                [self.adjustDigit(state_str[0]), self.adjustDigit(state_str[1]), self.adjustDigit(state_str[2])],
                [self.adjustDigit(state_str[3]), self.adjustDigit(state_str[4]), self.adjustDigit(state_str[5])],
                [self.adjustDigit(state_str[6]), self.adjustDigit(state_str[7]), self.adjustDigit(state_str[8])]
            ]
            # thêm tiêu đề bước
            data.append({
                "Bước": f"Ma trận bước {i}",
                "Cột 1": "",
                "Cột 2": "",
                "Cột 3": ""
            })
            # thêm 3 hàng của ma trận
            data.append({
                "Bước": "",
                "Cột 1": matrix[0][0],
                "Cột 2": matrix[0][1],
                "Cột 3": matrix[0][2]
            })
            data.append({
                "Bước": "",
                "Cột 1": matrix[1][0],
                "Cột 2": matrix[1][1],
                "Cột 3": matrix[1][2]
            })
            data.append({
                "Bước": "",
                "Cột 1": matrix[2][0],
                "Cột 2": matrix[2][1],
                "Cột 3": matrix[2][2]
            })
            # thêm dòng trống để phân tách
            data.append({
                "Bước": "",
                "Cột 1": "",
                "Cột 2": "",
                "Cột 3": ""
            })

        # tạo DataFrame từ dữ liệu
        df = pd.DataFrame(data)

        # thêm thông tin phân tích vào sheet thứ hai
        analysis_data = {
            "Thuật toán": [str(algorithm)],
            "Trạng thái ban đầu": [str(initialState)],
            "Số trạng thái đã duyệt qua": [counter],
            "Độ sâu": [depth],
            "Chi phí": [cost],
            "Thời gian chạy (s)": [runtime]
        }
        analysis_df = pd.DataFrame(analysis_data)

        # ghi vào file Excel
        try:
            with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Đường dẫn", index=False)
                analysis_df.to_excel(writer, sheet_name="Phân tích", index=False)
            messagebox.showinfo("Thành công", f"Đã xuất đường dẫn ra file: {file_name}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def fastForward(self, event=None):
        global statepointer, cost
        self.stopFastForward()
        if statepointer < cost:
            self.stopbutton.configure(state="enabled")
            statepointer += 1
            self.refreshFrame()
            ms = 100
            if 100 < cost <= 1000:
                ms = 20
            if cost > 1000:
                ms = 1
            self._job = self.stepCount.after(ms, self.fastForward)
        else:
            self.stopFastForward()

    def fastBackward(self, event=None):
        global statepointer
        self.stopFastForward()
        if statepointer > 0:
            self.stopbutton.configure(state="enabled")
            statepointer -= 1
            ms = 50
            if cost > 1000:
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
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer = 0
            self.refreshFrame()

    def shuffle(self, event=None):
        global initialState, statepointer
        while True:
            puzzle = list("012345678")
            random.shuffle(puzzle)
            initialState = "".join(puzzle)
            # Kiểm tra số nghịch thế
            inversions = self.countInversions(initialState)
            if inversions % 2 == 0:  # nếu số nghịch thế là chẵn, trạng thái giải được
                break
        self.reset()
        self.displayStateOnGrid(initialState)
        self.updateInitialStateGrid(initialState)
        messagebox.showinfo("Shuffled", f"Trạng thái ban đầu: {initialState}")

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
        for cell in [self.cell0, self.cell1, self.cell2, self.cell3, self.cell4, self.cell5, self.cell6, self.cell7, self.cell8,
                     self.cell0_1, self.cell1_1, self.cell2_1, self.cell3_1, self.cell4_1, self.cell5_1, self.cell6_1, self.cell7_1, self.cell8_1,
                     self.cell0_2, self.cell1_2, self.cell2_2, self.cell3_2, self.cell4_2, self.cell5_2, self.cell6_2, self.cell7_2, self.cell8_2]:
            cell.configure(background="#444444", foreground="#ffffff")

    def applyLightMode(self):
        self.appFrame.configure(style="Light.TFrame")
        self.mainLabel.configure(foreground="#003e3e")
        self.analysisbox.configure(background="#d6d6d6", foreground="#000000")
        self.stepCount.configure(background="#d6d6d6", foreground="#000000")
        for cell in [self.cell0, self.cell1, self.cell2, self.cell3, self.cell4, self.cell5, self.cell6, self.cell7, self.cell8,
                     self.cell0_1, self.cell1_1, self.cell2_1, self.cell3_1, self.cell4_1, self.cell5_1, self.cell6_1, self.cell7_1, self.cell8_1,
                     self.cell0_2, self.cell1_2, self.cell2_2, self.cell3_2, self.cell4_2, self.cell5_2, self.cell6_2, self.cell7_2, self.cell8_2]:
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
        global cost, statepointer, path
        if cost > 0:
            state = AI_algorithm.getStringRepresentation(path[statepointer])
            self.displayStateOnGrid(state)
            self.stepCount.configure(text=self.getStepCountString())
            self.displaySearchAnalysis()
        if statepointer == 0:
            self.resetbutton.configure(state="disabled")
            self.backbutton.configure(state="disabled")
            self.fastbackwardbutton.configure(state="disabled")
        else:
            self.resetbutton.configure(state="enabled")
            self.backbutton.configure(state="enabled")
            self.fastbackwardbutton.configure(state="enabled")
        if cost == 0 or statepointer == cost:
            self.fastforwardbutton.configure(state="disabled")
            self.nextbutton.configure(state="disabled")
        else:
            self.fastforwardbutton.configure(state="enabled")
            self.nextbutton.configure(state="enabled")

    @staticmethod
    def getStepCountString():
        global statepointer, cost
        return str(statepointer) + "/" + str(cost)

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
        global algorithm, initialState, counter, depth, cost, runtime
        if self.solved() or force_display is True:
            analytics = (
                "Phân tích của thuật toán:\n"
                + str(algorithm)
                + "\nTrạng thái ban đầu:\n"
                + str(initialState)
            )
            if force_display:
                analytics += "\n< Không thể giải >"
            analytics += (
                "\n-------------------------------"
                "\n"
                + "Số trạng thái đã duyệt qua: \n"
                + str(counter)
                + "\n"
                + "Độ sâu: \n"
                + str(depth)
                + "\n"
                + "Chi phí: \n"
                + str(cost)
                + "\n"
                + "Thời gian chạy: \n"
                + str(runtime)
                + " s"
            )
        else:
            analytics = ""
        self.analysisbox.configure(text=analytics)

    @staticmethod
    def solved():
        global path
        return len(path) > 0

    @staticmethod
    def readyToSolve():
        global initialState, algorithm
        return initialState is not None and algorithm is not None

    def resetGrid(self):
        global statepointer
        statepointer = 0
        self.refreshFrame()
        self.stepCount.configure(text=self.getStepCountString())

    def solveState(self):
        global path, cost, counter, depth, runtime, algorithm, initialState
        if str(algorithm) == "BFS":
            AI_algorithm.BFS(initialState)
            path, cost, counter, depth, runtime = (
                AI_algorithm.bfs_path,
                AI_algorithm.bfs_cost,
                AI_algorithm.bfs_counter,
                AI_algorithm.bfs_depth,
                AI_algorithm.time_bfs,
            )
        elif str(algorithm) == "DFS":
            AI_algorithm.DFS(initialState)
            path, cost, counter, depth, runtime = (
                AI_algorithm.dfs_path,
                AI_algorithm.dfs_cost,
                AI_algorithm.dfs_counter,
                AI_algorithm.dfs_depth,
                AI_algorithm.time_dfs,
            )
        elif str(algorithm) == "Uniform Cost Search":
            AI_algorithm.UCS(initialState)
            path, cost, counter, depth, runtime = (
                AI_algorithm.ucs_path,
                AI_algorithm.ucs_cost,
                AI_algorithm.ucs_counter,
                AI_algorithm.ucs_depth,
                AI_algorithm.time_ucs,
            )
        elif str(algorithm) == "Iterative Deepening":
            AI_algorithm.IDS(initialState)
            path, cost, counter, depth, runtime = (
                AI_algorithm.id_path,
                AI_algorithm.id_cost,
            AI_algorithm.time_astar,
        )
        elif str(algorithm) == "IDA*":
            AI_algorithm.IDAStar(initialState)
            path, cost, counter, depth, runtime = (
            AI_algorithm.idastar_path,
            AI_algorithm.idastar_cost,
            AI_algorithm.idastar_counter,
            AI_algorithm.idastar_depth,
            AI_algorithm.time_idastar,
        )
        elif str(algorithm) == "Simple Hill Climbing":
            AI_algorithm.SimpleHillClimbing(initialState)
            path, cost, counter, depth, runtime = (
            AI_algorithm.shc_path,
            AI_algorithm.shc_cost,
            AI_algorithm.shc_counter,
            AI_algorithm.shc_depth,
            AI_algorithm.time_shc,
        )

    def reset(self):
        global path, cost, counter, runtime
        path = []
        cost = counter = 0
        runtime = 0.0
        self.resetGrid()
        self.analysisbox.configure(text="")
