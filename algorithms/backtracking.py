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
    # chuyển đổi state thành danh sách 9 phần tử để xử lý
    def flatten_state(state):
        if isinstance(state, (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state):
            return [state[i][j] for i in range(3) for j in range(3)]
        elif isinstance(state, (list, tuple)) and len(state) == 9:
            return list(state)
        else:
            raise ValueError("State must be a 3x3 grid or a flat list/tuple with 9 elements")

    # hàm ràng buộc điều kiện CSP
    # Với mỗi vị trí pos từ 0 đến 8 kiểm tra nếu là pos = 0 thì luôn đúng 
    # nếu là số 8 thì số tiếp theo phải là 0 
    # còn nếu không thì phải điền số hiện tại bằng max_num + 1
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

    # remaining_numbers danh sách các số chưa sử dụng
    # duyệt tất cả các số chưa sử dụng
    # gán vào vị trí pos kiểm tra ràng buộc nếu hợp lệ thì gọi điền tiếp
    # nếu sai thì xóa backtrack
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