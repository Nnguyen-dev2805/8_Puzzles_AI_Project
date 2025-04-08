# moves
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def getStringRepresentation(x):
    """Hàm chuyển đổi trạng thái thành chuỗi"""
    return str(x).zfill(9)


def goalTest(state):
    """Hàm kiểm tra trạng thái đích"""
    return state == 123456780


def getPath(parentMap, inputState):
    """Hàm lấy đường đi từ trạng thái ban đầu đến trạng thái đích"""
    path = []
    temp = 123456780
    while temp != inputState:
        path.append(temp)
        temp = parentMap[temp]
    path.append(inputState)
    path.reverse()
    return path


def getChildren(state):
    """Hàm lấy trạng thái tiếp theo của trạng thái hiện tại"""
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
    """Hàm kiểm tra tính hợp lệ của tọa độ"""
    if i >= 3 or i < 0 or j >= 3 or j < 0:
        return 0
    return 1


def manhattanDistance(state):
    """Hàm tính khoảng cách Manhattan"""
    state_str = getStringRepresentation(state)
    total_distance = 0
    for i in range(9):
        if state_str[i] != "0":
            current_num = int(state_str[i])
            goal_x, goal_y = divmod(current_num - 1, 3)
            curr_x, curr_y = divmod(i, 3)
            total_distance += abs(goal_x - curr_x) + abs(goal_y - curr_y)
    return total_distance
