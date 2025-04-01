import heapq
import math
import time

# moves
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

dfs_counter = 0
bfs_counter = 0
ucs_counter = 0
id_counter = 0  # iterative deepening
bfs_best_counter = 0
astar_counter = 0
idastar_counter = 0
shc_counter = 0

dfs_path = []
bfs_path = []
ucs_path = []
id_path = []
bfs_best_path = []
astar_path = []
idastar_path = []
shc_path = []

dfs_cost = 0
bfs_cost = 0
ucs_cost = 0
id_cost = 0
bfs_best_cost = 0
astar_cost = 0
idastar_cost = 0
shc_cost = 0

dfs_depth = 0
bfs_depth = 0
ucs_depth = 0
id_depth = 0
bfs_best_depth = 0
astar_depth = 0
idastar_depth = 0
shc_depth = 0

time_bfs = 0
time_dfs = 0
time_ucs = 0
time_id = 0
time_bfs_best = 0
time_astar = 0
time_idastar = 0
time_shc = 0

# hàm chuyển số thành chuỗi
def getStringRepresentation(x):
    return str(x).zfill(9)

# hàm check trạng thái đích
def goalTest(state):
    return state == 123456780


# hàm lấy đường đi
def getPath(parentMap, inputState):
    path = []
    temp = 123456780
    while temp != inputState:
        path.append(temp)
        temp = parentMap[temp]
    path.append(inputState)
    path.reverse()
    return path


# hàm lấy trạng thái tiếp theo
def getChildren(state):
    children = []
    idx = state.index("0")  # vị trí số 0
    i, j = divmod(idx, 3)
    for x in range(0, 4):
        nx = i + dx[x]
        ny = j + dy[x]
        new_index = int(nx * 3 + ny)
        if checkValid(nx, ny):
            listTemp = list(state)  # chuyển thành list các kí tự
            listTemp[idx], listTemp[new_index] = listTemp[new_index], listTemp[idx]
            children.append("".join(listTemp))
    return children


# hàm kiểm tra tính hợp lệ
def checkValid(i, j):
    if i >= 3 or i < 0 or j >= 3 or j < 0:
        return 0
    return 1


# hàm heuristic
def manhattanDistance(state):
    state_str = getStringRepresentation(state)
    total_distance = 0
    for i in range(9):
        if state_str[i] != '0':
            current_num = int(state_str[i])
            goal_x, goal_y = divmod(
                current_num - 1, 3
            )  # tọa độ mục tiêu -1 vì chỉ số từ 0 -> 8
            curr_x, curr_y = divmod(i, 3)
            total_distance += abs(goal_x - curr_x) + abs(goal_y - curr_y)
    return total_distance

# BFS algorithm
def BFS(inputState):
    start_time = time.time()
    queue = []
    visited = set()
    parent = {}
    parent_cost = {}
    integer_state = int(inputState)
    queue.append(integer_state)
    cnt = 0
    global bfs_counter, bfs_cost, bfs_depth, bfs_path, time_bfs
    bfs_cost = bfs_depth = 0
    parent_cost[integer_state] = 0

    while queue:
        cnt += 1
        state = queue.pop(0)

        if state in visited:
            continue

        visited.add(state)
        bfs_depth = max(bfs_depth, parent_cost[state])

        if goalTest(state):
            path = getPath(parent, int(inputState))
            bfs_counter = cnt
            bfs_path = path
            bfs_cost = len(path) - 1
            time_bfs = float(time.time() - start_time)
            return True

        children = getChildren(getStringRepresentation(state))
        for child in children:
            child_int = int(child)
            if child_int not in visited:
                queue.append(child_int)
                parent[child_int] = state
                parent_cost[child_int] = 1 + parent_cost[state]

    bfs_path = []
    bfs_cost = 0
    bfs_counter = cnt
    time_bfs = float(time.time() - start_time)
    return False


# DFS algorithm
def DFS(inputState):
    start_time = time.time()
    stack = []
    visited = set()
    parent = {}
    parent_cost = {}
    integer_state = int(inputState)
    stack.append(integer_state)
    cnt = 0
    global dfs_counter, dfs_cost, dfs_depth, dfs_path, time_dfs
    dfs_cost = dfs_depth = 0
    parent_cost[integer_state] = 0

    while stack:
        cnt += 1
        state = stack.pop()
        if state not in visited:
            visited.add(state)
            dfs_depth = max(dfs_depth, parent_cost[state])

            if goalTest(state):
                path = getPath(parent, int(inputState))
                dfs_counter = cnt
                dfs_path = path
                dfs_cost = len(path) - 1
                time_dfs = float(time.time() - start_time)
                return True

            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    stack.append(child_int)
                    parent[child_int] = state
                    parent_cost[child_int] = 1 + parent_cost[state]

    dfs_path = []
    dfs_cost = 0
    dfs_counter = cnt
    time_dfs = float(time.time() - start_time)
    return False


# UCS algorithm
def UCS(inputState):
    start_time = time.time()
    pq = []
    visited = set()
    parent = {}
    parent_cost = {}
    integer_state = int(inputState)
    heapq.heappush(pq, (0, integer_state))  # (cost, state)
    cnt = 0
    global ucs_counter, ucs_cost, ucs_depth, ucs_path, time_ucs
    ucs_cost = ucs_depth = 0
    parent_cost[integer_state] = 0

    while pq:
        cnt += 1
        curr_cost, state = heapq.heappop(pq)
        if state not in visited:
            visited.add(state)
            ucs_depth = max(ucs_depth, curr_cost)

            if goalTest(state):
                path = getPath(parent, int(inputState))
                ucs_counter = cnt
                ucs_path = path
                ucs_cost = len(path) - 1
                time_ucs = float(time.time() - start_time)
                return True

            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    new_cost = curr_cost + 1
                    heapq.heappush(pq, (new_cost, child_int))
                    parent[child_int] = state
                    parent_cost[child_int] = new_cost

    ucs_path = []
    ucs_cost = 0
    ucs_counter = cnt
    time_ucs = float(time.time() - start_time)
    return False


# IDS algorithm: thuật kết hợp giữa DFS và BFS
def IDS(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    global id_counter, id_cost, id_depth, id_path, time_id
    id_counter = 0
    id_cost = 0
    id_path = []
    id_depth = 0

    def depth_limited_search(state, depth_limit, visited, parent, parent_cost):
        nonlocal cnt  # khai báo nonlocal để cho biết nó là thằng cnt bên ngoài
        cnt += 1
        if goalTest(state):
            return True, getPath(parent, integer_state)
        if parent_cost[state] >= depth_limit:
            return False, []  # đạt đến độ sau dừng mở rộng trạng thái
        children = getChildren(getStringRepresentation(state))
        for child in children:
            child_int = int(child)
            if child_int not in visited:
                visited.add(child_int)
                parent[child_int] = state
                parent_cost[child_int] = parent_cost[state] + 1
                found, path = depth_limited_search(
                    child_int, depth_limit, visited, parent, parent_cost
                )
                if found:
                    return True, path
        return False, []

    cnt = 0
    depth_limit = 0
    while True:
        visited = set()
        parent = {}
        parent_cost = {}
        parent_cost[integer_state] = 0
        visited.add(integer_state)
        found, path = depth_limited_search(
            integer_state, depth_limit, visited, parent, parent_cost
        )
        if found:
            id_counter = cnt
            id_path = path
            id_cost = len(path) - 1
            id_depth = max(id_depth, len(path) - 1)
            time_id = time.time() - start_time
            return True
        # if depth_limit > 50: # giới hạn độ sâu
        #     id_counter = cnt
        #     id_path = []
        #     id_cost = 0
        #     time_id = float(time.time() - start_time)
        #     return False
        depth_limit += 1


# BestFirstSearch algorithm
# ưu tiên mở rộng trạng thái có khả năng gần đích nhất
# xét heuristic bằng manhattan distance
def BestFirstSearch(inputState):
    start_time = time.time()
    pq = []
    visited = set()
    parent = {}
    parent_cost = {}
    integer_state = int(inputState)
    parent_cost[integer_state] = 0
    manhanttan_cost = manhattanDistance(integer_state)
    heapq.heappush(pq, (manhanttan_cost, integer_state))
    cnt = 0

    global bfs_best_counter, bfs_best_cost, bfs_best_depth, bfs_best_path, time_bfs_best
    bfs_best_cost = bfs_best_depth = 0

    while pq:
        cnt += 1
        _, state = heapq.heappop(pq)
        if state not in visited:
            visited.add(state)
            bfs_best_depth = max(bfs_best_depth, parent_cost[state])
            if goalTest(state):
                path = getPath(parent, int(inputState))
                bfs_best_counter = cnt
                bfs_best_path = path
                bfs_best_cost = len(path) - 1
                time_bfs_best = float(time.time() - start_time)
                return True
            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    parent_cost[child_int] = parent_cost[state] + 1
                    new_manhanttan_cost = manhattanDistance(child_int)
                    heapq.heappush(pq, (new_manhanttan_cost, child_int))
                    parent[child_int] = state
    bfs_best_path = []
    bfs_best_cost = 0
    bfs_best_counter = cnt
    time_bfs_best = float(time.time() - start_time)
    return False

# A* algorithm - là thuật toán kết hợp giữa UCS và BestFirstSearch
# Đánh giá dựa trên hàm f(n) = g(n) + h(n)
# Trong đó g(n) là chi phí từ trạng thái ban đầu đến trạng thái hiện tại
# h(n) là heuristic ước lượng chi phí từ trạng thái n đến trạng thái đích 

def AStar(inputState):
    start_time = time.time()
    pq = []
    visited = {}
    parent = {}
    g_cost = {} # chi phí từ trạng thái ban đầu đến trạng thái hiện tại
    integer_state = int(inputState)
    g_cost[integer_state] = 0
    h_cost = manhattanDistance(integer_state)
    f_cost = h_cost
    heapq.heappush(pq, (f_cost,0,integer_state))
    cnt = 0

    global astar_counter, astar_cost, astar_depth, astar_path, time_astar
    astar_cost = astar_depth = 0

    while pq:
        cnt += 1
        f_cost,curr_cost,state = heapq.heappop(pq)

        # nếu trạng thái đã được thăm và trạng thái này có cost >= cost của hiện tại
        if state in visited and curr_cost >= visited[state]:
            continue

        # cập nhật visited với chi phí thấp nhất
        visited[state] = curr_cost
        astar_depth = max(astar_depth,curr_cost)

        if goalTest(state):
            path = getPath(parent, int(inputState))
            astar_counter = cnt
            astar_path = path
            astar_cost = len(path) - 1
            time_astar = float(time.time() - start_time)
            return True

        children = getChildren(getStringRepresentation(state))
        for child in children:
            child_int = int(child)
            new_g_cost = curr_cost + 1
            h_cost = manhattanDistance(child_int)
            new_f_cost = new_g_cost + h_cost 

            # nếu trạng thái con chưa được thăm hoặc có chi phí thấp hơn
            if child_int not in visited or new_g_cost < visited[child_int]:
                heapq.heappush(pq, (new_f_cost, new_g_cost, child_int))
                parent[child_int] = state
                g_cost[child_int] = new_g_cost
    astar_path = []
    astar_cost = 0
    astar_counter = cnt
    time_astar = float(time.time() - start_time)
    return False

# thuật toán kết hợp giữa IDS và A*, sử dụng hàm heuristic để giới hạn độ sâu tìm kiếm
def IDAStar(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    global idastar_counter, idastar_cost, idastar_depth, idastar_path, time_idastar
    idastar_counter = 0
    idastar_cost = 0
    idastar_depth = 0
    idastar_path = []

    # hàm tìm kiếm với độ sau giới hạn f_cost 
    def search(state,g_cost,f_limit,parent,visited):
        nonlocal cnt,next_f_limit
        cnt += 1
        h_cost = manhattanDistance(state)
        f_cost = h_cost + g_cost

        # nếu f_cost vượt quá giới hạn, trả về False và giá trị f_cost nhỏ nhất vượt quá
        if f_cost > f_limit:
            next_f_limit = min(next_f_limit,f_cost)
            return False,[]
        
        if goalTest(state):
            return True,getPath(parent,int(inputState))
        
        children = getChildren(getStringRepresentation(state))
        for child in children:
            child_int = int(child)
            if child_int not in visited:
                visited.add(child_int)
                parent[child_int] = state
                found,path = search(child_int,g_cost+1,f_limit,parent,visited)
                if found:
                    return True, path
        return False,[]
    
    cnt = 0
    h_initial = manhattanDistance(integer_state)
    f_limit = h_initial # giới hạn ban đầu là h(n) của trạng thái ban đầu
    while True:
        visited = set()
        parent ={}
        visited.add(integer_state)
        next_f_limit = float('inf') # giá trị f_cost nhỏ nhất vượt qua f_limit
        found,path = search(integer_state,0,f_limit,parent,visited)

        if found:
            idastar_counter = cnt
            time_idastar = float(time.time() - start_time)
            idastar_cost = len(path) - 1
            idastar_depth = idastar_cost
            idastar_path = path
            return True
        
        if next_f_limit == float('inf'): # Không còn trạng thái nào để mở rộng
            idastar_counter = cnt
            idastar_path = []
            idastar_cost = 0
            idastar_depth = 0
            time_idastar = float(time.time() - start_time)     
            return False
        f_limit = next_f_limit # cập nhật giới hạn

def SimpleHillClimbing(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    global shc_counter, shc_cost, shc_depth, shc_path, time_shc
    shc_counter = 0
    shc_cost = 0
    shc_depth = 0
    shc_path = []

    current_state = integer_state
    parent = {}
    visited = set()
    depth = 0

    while True:
        shc_counter += 1
        visited.add(current_state)

        if goalTest(current_state):
            path = getPath(parent,int(inputState))
            shc_path = path 
            shc_cost = len(path) - 1
            shc_depth = depth
            time_shc = float(time.time() - start_time)
            return True
        
        children = getChildren(getStringRepresentation(current_state))
        best_child = None
        best_heristic = float('inf')

        # tìm trạng thái con có heristic tốt nhất (nhỏ nhất)
        for child in children:
            child_int = int(child)
            if child_int not in visited:
                h_cost = manhattanDistance(child_int)
                if h_cost < best_heristic:
                    best_heristic = h_cost
                    best_child = child_int
        
        if best_child is None:
            shc_path = []
            shc_cost = 0
            shc_depth = depth
            shc_counter = shc_counter
            time_shc = float(time.time() - start_time)
            return False

        parent[best_child] = current_state
        current_state = best_child
        depth += 1
        
