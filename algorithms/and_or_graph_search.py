import time
from algorithms.common import goalTest, getStringRepresentation
from algorithms.q_learning import manhattanDistance

dx = [-1, 1, 0, 0]  
dy = [0, 0, -1, 1]
action_names = ["0", "1", "2", "3"]  

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
        self.counter = 0       
        self.path = []         
        self.cost = 0         
        self.depth = 0         
        self.time_taken = 0    
        self.memory_size = 0   # Kích thước bộ nhớ (bytes)

    def _string_to_2d(self, state_str):
        """Chuyển đổi chuỗi trạng thái thành ma trận 3x3"""
        nums = [int(c) for c in state_str]
        return [nums[i:i+3] for i in range(0, 9, 3)]

    def _2d_to_string(self, state_2d):
        """Chuyển ma trận 3x3 thành chuỗi"""
        return ''.join(str(num) for row in state_2d for num in row)

    def _2d_to_int(self, state_2d):
        """Chuyển ma trận 3x3 thành số nguyên"""
        return int(self._2d_to_string(state_2d))

    def AndOrGraphSearch(self, inputState, goalState):
        start_time = time.perf_counter()
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.memory_size = 0
        max_recursion_depth = 0  # Theo dõi độ sâu đệ quy tối đa

        initial_state = getStringRepresentation(inputState)
        goal_state = getStringRepresentation(goalState)
        visited = set()

        def or_search(state, path, recursion_depth=0):
            nonlocal max_recursion_depth
            self.counter += 1
            max_recursion_depth = max(max_recursion_depth, recursion_depth)

            if goalTest(int(state)):
                memory_size = (len(visited) * 8) + (max_recursion_depth * 16)
                return [], self.counter, memory_size
            if state in path:
                memory_size = (len(visited) * 8) + (max_recursion_depth * 16)
                return None, self.counter, memory_size

            visited.add(state)
            children = getChildren(state)
            move_states = [(manhattanDistance(int(child_state)), action) for action, child_state in children.items()]
            move_states.sort(key=lambda x: x[0])

            for _, action in move_states:
                new_state = children.get(action, state)
                plan, counter, memory_size = and_search(new_state, path + [state], recursion_depth + 1)
                if plan is not None:
                    return [action] + plan, counter, memory_size
            memory_size = (len(visited) * 8) + (max_recursion_depth * 16)
            return None, self.counter, memory_size

        def and_search(state, path, recursion_depth):
            # Trong 8-puzzle xác định, node AND chỉ có một trạng thái con
            return or_search(state, path, recursion_depth)

        plan, visited_count, self.memory_size = or_search(initial_state, [])

        if plan:
            # Tái tạo đường đi từ kế hoạch hành động
            path = [initial_state]
            current = initial_state
            for action in plan:
                current = getChildren(current).get(action, current)
                path.append(current)

            # Chuyển trạng thái từ chuỗi -> số nguyên để đồng bộ với thuật toán khác
            self.path = [int(state) for state in path]

            self.cost = len(plan)
            self.depth = len(plan)
        else:
            self.path = []
            self.cost = 0
            self.depth = 0

        self.time_taken = time.perf_counter() - start_time
        return self.path, self.cost, self.counter, self.depth, self.time_taken, self.memory_size







# ---------------------- AND OR VERSION 2 ----------------------

# import time
# from algorithms.common import goalTest, getStringRepresentation
# from algorithms.q_learning import manhattanDistance

# # Định nghĩa các bước di chuyển: UP, DOWN, LEFT, RIGHT
# dx = [-1, 1, 0, 0]
# dy = [0, 0, -1, 1]
# action_names = ["0", "1", "2", "3"]  # UP, DOWN, LEFT, RIGHT

# def checkValid(i, j):
#     return 0 <= i < 3 and 0 <= j < 3

# def getChildren(state):
#     children = {}
#     idx = state.index("0")
#     i, j = divmod(idx, 3)
#     for x in range(4):
#         nx = i + dx[x]
#         ny = j + dy[x]
#         if checkValid(nx, ny):
#             new_index = nx * 3 + ny
#             listTemp = list(state)
#             listTemp[idx], listTemp[new_index] = listTemp[new_index], listTemp[idx]
#             child_state = ''.join(listTemp)
#             children[action_names[x]] = child_state
#     return children

# class AndOrGraphSearchAlgorithm:
#     def __init__(self):
#         self.counter = 0
#         self.path = []
#         self.cost = 0
#         self.depth = 0
#         self.time_taken = 0

#     def _string_to_2d(self, state_str):
#         nums = [int(c) for c in state_str]
#         return [nums[i:i+3] for i in range(0, 9, 3)]

#     def AndOrGraphSearch(self, inputState, goalState):
#         start_time = time.perf_counter()
#         self.counter = 0
#         self.path = []
#         self.cost = 0
#         self.depth = 0

#         initial_state = getStringRepresentation(inputState)
#         goal_state = getStringRepresentation(goalState)

#         max_depth = 20
#         max_space = 1
#         visited = set()

#         def recur(state, path, depth, visited):
#             nonlocal max_space
#             self.counter += 1
#             if depth > max_depth:
#                 return False, []

#             if goalTest(int(state)):
#                 return True, []

#             if state in visited:
#                 return False, []

#             visited.add(state)

#             best_path = None

#             for action in ["0", "1", "2", "3"]: 
#                 children = getChildren(state)
#                 if action not in children:
#                     continue
#                 next_state = children[action]

#                 if next_state in visited:
#                     continue

#                 # Với 8-puzzle xác định, hành động chỉ tạo ra 1 kết quả (AND node có 1 successor)
#                 success, sub_path = recur(next_state, path + [action], depth + 1, visited)

#                 if success:
#                     candidate_path = [action] + sub_path
#                     if not best_path or len(candidate_path) < len(best_path):
#                         best_path = candidate_path

#             visited.remove(state)

#             if best_path:
#                 max_space = max(max_space, len(best_path) + len(visited))
#                 return True, best_path
#             return False, []

#         success, plan = recur(initial_state, [], 0, set())

#         if success:
#             # Tái tạo đường đi
#             current = initial_state
#             self.path = [self._string_to_2d(current)]
#             for action in plan:
#                 current = getChildren(current)[action]
#                 self.path.append(self._string_to_2d(current))
#             self.cost = len(plan)
#             self.depth = len(plan)
#         else:
#             self.path = []
#             self.cost = 0
#             self.depth = 0

#         self.time_taken = time.perf_counter() - start_time
#         return self.path, self.cost, self.counter, self.depth, self.time_taken
