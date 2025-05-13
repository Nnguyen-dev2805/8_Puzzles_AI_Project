# import time
# from collections import deque
# from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation

# class AndOrGraphSearchAlgorithm:
#     def __init__(self):
#         self.counter = 0  
#         self.path = []   
#         self.cost = 0    
#         self.depth = 0    
#         self.time_taken = 0  

#     def AndOrGraphSearch(self, inputState):
#         start_time = time.time()
#         integer_state = int(inputState) 

#         queue = deque([(integer_state, [])])  # (trạng thái, kế hoạch hành động)
#         visited = set([integer_state])        
#         parent = {integer_state: None}        
#         plan = {}                             

#         while queue:
#             self.counter += 1
#             state, actions = queue.popleft()  

#             if goalTest(state):
#                 self.path = getPath(parent, int(inputState))
#                 self.cost = len(self.path) - 1
#                 self.depth = self.cost
#                 self.time_taken = float(time.time() - start_time)
#                 return self.path, self.cost, self.counter, self.depth, self.time_taken

#             if state in plan:
#                 continue

#             children = getChildren(getStringRepresentation(state))
#             children = [int(child) for child in children if int(child) not in visited]

#             if not children:
#                 continue

#             child_plans = []
#             for child in children:
#                 visited.add(child)
#                 parent[child] = state
#                 child_actions = actions + [child] 
#                 queue.append((child, child_actions))
#                 child_plans.append(child)

#             plan[state] = child_plans

#         self.path = []
#         self.cost = 0
#         self.depth = 0
#         self.time_taken = float(time.time() - start_time)
#         return self.path, self.cost, self.counter, self.depth, self.time_taken

import time
from algorithms.common import goalTest, getStringRepresentation
from algorithms.q_learning import manhattanDistance

# Định nghĩa moves
dx = [-1, 1, 0, 0]  # UP, DOWN, LEFT, RIGHT
dy = [0, 0, -1, 1]
action_names = ["0", "1", "2", "3"]  # Tương ứng với UP, DOWN, LEFT, RIGHT

def checkValid(i, j):
    return 0 <= i < 3 and 0 <= j < 3

def getChildren(state):
    children = {}
    idx = state.index("0")
    i, j = divmod(idx, 3)
    for x in range(4):
        nx = i + dx[x]
        ny = j + dy[x]
        if checkValid(nx, ny):
            new_index = int(nx * 3 + ny)
            listTemp = list(state)
            listTemp[idx], listTemp[new_index] = listTemp[new_index], listTemp[idx]
            child_state = "".join(listTemp)
            children[action_names[x]] = child_state
    return children

class AndOrGraphSearchAlgorithm:
    def __init__(self):
        self.counter = 0  # Số node đã xử lý
        self.path = []    # Đường đi
        self.cost = 0     # Chi phí (số bước)
        self.depth = 0    # Độ sâu
        self.time_taken = 0  # Thời gian thực hiện

    def _string_to_2d(self, state_str):
        """Chuyển đổi chuỗi trạng thái thành trạng thái 2D."""
        nums = [int(c) for c in state_str]
        return [nums[i:i+3] for i in range(0, 9, 3)]

    def AndOrGraphSearch(self, inputState, goalState):
        start_time = time.perf_counter()
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0

        initial_state = getStringRepresentation(inputState)
        goal_state = getStringRepresentation(goalState)
        visited = set()

        def or_search(state, path):
            self.counter += 1
            if goalTest(int(state)):
                return [], self.counter
            if state in path:
                return None, self.counter

            visited.add(state)
            children = getChildren(state)
            # Sắp xếp hành động theo heuristic (khoảng cách Manhattan)
            move_states = [(manhattanDistance(int(child_state)), action) for action, child_state in children.items()]
            move_states.sort(key=lambda x: x[0])

            for _, action in move_states:
                new_state = children.get(action, state)
                plan, _ = and_search(new_state, path + [state])
                if plan is not None:
                    return [action] + plan, self.counter
            return None, self.counter

        def and_search(state, path):
            # Trong 8-puzzle xác định, node AND chỉ có một trạng thái con
            return or_search(state, path)

        plan, visited_count = or_search(initial_state, [])
        if plan:
            # Tái tạo đường đi
            path = [initial_state]
            current = initial_state
            for action in plan:
                current = getChildren(current).get(action, current)
                path.append(current)
            # Chuyển đổi path thành định dạng 2D
            self.path = [self._string_to_2d(state) for state in path]
            self.cost = len(plan)
            self.depth = len(plan)
        else:
            self.path = []
            self.cost = 0
            self.depth = 0

        self.time_taken = time.perf_counter() - start_time
        return self.path, self.cost, self.counter, self.depth, self.time_taken