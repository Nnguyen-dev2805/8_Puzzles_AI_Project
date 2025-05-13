import random

def ac3(csp):
    """
    Thuật toán AC-3 để đảm bảo tính nhất quán cung.
    Args:
        csp: Một dict chứa các thành phần của CSP:
            - variables: List các biến (ô trong bảng 3x3).
            - domains: Dict ánh xạ biến đến miền giá trị của nó.
            - constraints: Dict ánh xạ cặp biến (var1, var2) đến hàm kiểm tra ràng buộc.
    Returns:
        - (True, domains, ac3_log): Nếu đạt nhất quán cung, trả về True, miền giá trị đã thu hẹp, và log của AC-3.
        - (False, None, ac3_log): Nếu không thể đạt nhất quán cung (miền rỗng), trả về False, None, và log.
    """
    queue = [(var1, var2) for var1 in csp['variables'] for var2 in csp['variables'] if var1 != var2 and (var1, var2) in csp['constraints']]
    ac3_log = []
    domains = {var: values[:] for var, values in csp['domains'].items()}  # Sao chép miền
    
    while queue:
        (xi, xj) = queue.pop(0)
        if revise(csp, xi, xj, domains, ac3_log):
            if not domains[xi]:
                ac3_log.append(f"Domain of {xi} became empty, CSP is unsolvable.")
                return False, None, ac3_log
            for xk in [v for v in csp['variables'] if v != xi and v != xj and (v, xi) in csp['constraints']]:
                queue.append((xk, xi))
    
    return True, domains, ac3_log

def revise(csp, xi, xj, domains, ac3_log):
    """
    Hàm REVISE trong AC-3: Sửa miền giá trị của xi dựa trên ràng buộc với xj.
    Args:
        csp: Bài toán CSP.
        xi, xj: Hai biến cần kiểm tra.
        domains: Dict chứa miền giá trị hiện tại.
        ac3_log: List để ghi lại log các giá trị bị xóa.
    Returns:
        True nếu miền của xi bị sửa, False nếu không.
    """
    revised = False
    di = domains[xi].copy()
    for x in di:
        if not any(csp['constraints'][(xi, xj)](x, y) for y in domains[xj]):
            domains[xi].remove(x)
            ac3_log.append(f"Removed value {x} from domain of {xi} due to constraint with {xj}")
            revised = True
    return revised

def backtracking_with_ac3(initial_state, goal_state):
    """
    Hàm Backtracking sử dụng AC-3 để giải bài toán 8-Puzzle.
    Args:
        initial_state: Trạng thái ban đầu (danh sách 3x3).
        goal_state: Trạng thái mục tiêu (danh sách 3x3).
    Returns:
        (steps, visited_count, ac3_log): Các bước giải, số trạng thái đã thăm, và log của AC-3.
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

    variables = [(i, j) for i in range(3) for j in range(3)]
    domains = {(i, j): list(range(9)) for i, j in variables}
    for var in variables:
        random.shuffle(domains[var])
    
    constraints = {}
    for var1 in variables:
        for var2 in variables:
            if var1 != var2:
                constraints[(var1, var2)] = lambda x, y: x != y
    for i in range(3):
        for j in range(3):
            if goal_state[i][j] == 0:
                var = (i, j)
                for other_var in variables:
                    if other_var != var:
                        constraints[(var, other_var)] = lambda x, y, v=0: x == v
                        constraints[(other_var, var)] = lambda y, x, v=0: x == v
    
    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': constraints
    }
    
    consistent, domains, ac3_log = ac3(csp)
    if not consistent:
        return [], 0, ac3_log

    goal = [[goal_flat[i * 3 + j] for j in range(3)] for i in range(3)]
    board = [[None for _ in range(3)] for _ in range(3)]
    steps = []
    visited_count = 0

    def is_valid_assignment(pos, value):
        i, j = divmod(pos, 3)
        for k in range(pos):
            ki, kj = divmod(k, 3)
            if board[ki][kj] == value:
                return False
        return True

    def backtrack(pos):
        nonlocal visited_count
        i, j = divmod(pos, 3)
        
        if pos == 9:
            if all(board[i][j] == goal[i][j] for i in range(3) for j in range(3)):
                steps.append([row[:] for row in board])
                return True
            return False
        
        for value in domains[(i, j)]:
            if not is_valid_assignment(pos, value):
                continue
            board[i][j] = value
            if not is_continuous_sequence(board, pos):
                board[i][j] = None
                continue
            steps.append([row[:] for row in board])
            visited_count += 1
            if backtrack(pos + 1):
                return True
            board[i][j] = None
            steps.append([row[:] for row in board])
        
        return False

    success = backtrack(0)
    
    if not success:
        ac3_log.append("Backtracking failed to find a solution after AC-3.")
        return [], visited_count, ac3_log
    
    return steps, visited_count, ac3_log