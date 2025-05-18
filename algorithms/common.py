# moves
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def getStringRepresentation(x):
    return str(x).zfill(9)


def goalTest(state):
    return state == 123456780


def getPath(parentMap, start_state):
    """Hàm lấy đường đi từ trạng thái ban đầu đến trạng thái đích"""
    path = []
    # Tìm trạng thái mục tiêu trong parentMap
    current_state = next((state for state, p in parentMap.items() if goalTest(state)), None)
    if current_state is None:
        return [start_state]  # Trả về trạng thái ban đầu nếu không tìm thấy mục tiêu
    while current_state is not None and current_state != start_state:
        path.append(current_state)
        current_state = parentMap.get(current_state)
    path.append(start_state)
    return path[::-1]


def getChildren(state):
    children = []
    idx = state.index("0")
    i, j = divmod(idx, 3)
    for x in range(0, 4):
        nx = i + dx[x]
        ny = j + dy[x]
        new_index = int(nx * 3 + ny)
        if checkValid(nx, ny):
            listTemp = list(state)
            listTemp[idx], listTemp[new_index] = listTemp[new_index], listTemp[idx]
            children.append("".join(listTemp))
    return children


def checkValid(i, j):
    if i >= 3 or i < 0 or j >= 3 or j < 0:
        return 0
    return 1


def manhattanDistance(state):
    state_str = getStringRepresentation(state)
    total_distance = 0
    for i in range(9):
        if state_str[i] != "0":
            current_num = int(state_str[i])
            goal_x, goal_y = divmod(current_num - 1, 3)
            curr_x, curr_y = divmod(i, 3)
            total_distance += abs(goal_x - curr_x) + abs(goal_y - curr_y)
    return total_distance
