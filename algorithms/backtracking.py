import random
import time

class Backtracking8Puzzle:
    def __init__(self, update_callback=None):
        self.board = [None] * 9  # Bảng 8-puzzle (9 ô, ban đầu là None)
        self.used_values = set()  # Tập hợp các giá trị đã được sử dụng
        self.steps = 0  # Đếm số bước thực hiện
        self.update_callback = update_callback  # Hàm callback để cập nhật giao diện

    def is_valid(self, value):
        """Kiểm tra ràng buộc: Giá trị chưa được sử dụng."""
        return value not in self.used_values

    def backtrack(self, position=0):
        """Thuật toán Backtracking để gán giá trị cho từng ô."""
        if position == 9:  # Nếu đã gán giá trị cho tất cả các ô
            if self.update_callback:
                self.update_callback(self.board, "success")
            return True

        values = list(range(9))
        random.shuffle(values)

        for value in values:
            if self.is_valid(value):
                # Gán giá trị cho ô hiện tại
                self.board[position] = value
                self.used_values.add(value)
                self.steps += 1

                # Cập nhật giao diện
                if self.update_callback:
                    self.update_callback(self.board, "assign")
                time.sleep(0.5)  # Delay để quan sát

                # Tiếp tục gán giá trị cho ô tiếp theo
                if self.backtrack(position + 1):
                    return True

                # Backtrack: Hủy gán giá trị và thử giá trị khác
                self.board[position] = None
                self.used_values.remove(value)

                # Cập nhật giao diện khi backtrack
                if self.update_callback:
                    self.update_callback(self.board, "backtrack")
                time.sleep(0.5)  # Delay để quan sát

        return False

    def solve(self):
        """Giải bài toán 8-puzzle bằng Backtracking."""
        if self.update_callback:
            self.update_callback(self.board, "start")
        if self.backtrack():
            print("Thuật toán hoàn tất.")
        else:
            print("Không tìm thấy giải pháp.")