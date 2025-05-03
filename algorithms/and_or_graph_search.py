import time
from collections import deque
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation

class AndOrGraphSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    # def AndOrGraphSearch(self, inputState):
    #     """Thuật toán AND-OR Graph Search cho bài toán 8-puzzle"""
    #     start_time = time.time()
    #     integer_state = int(inputState)
    #     visited = set()

    #     def or_search(state, visited):
    #         """Hàm OR-Search: Trả về True nếu trạng thái có thể giải quyết"""
    #         if goalTest(state):
    #             return True, []
    #         if state in visited:
    #             return False, None
    #         visited.add(state)

    #         children = getChildren(getStringRepresentation(state))
    #         for child in children:
    #             child_int = int(child)
    #             solved, policy = or_search(child_int, visited)
    #             if solved:
    #                 return True, [child_int] + policy
    #         return False, None

    #     # def and_search(state, visited):
    #     #     """Hàm AND-Search: Trả về True nếu tất cả các trạng thái con có thể giải quyết"""
    #     #     children = getChildren(getStringRepresentation(state))
    #     #     policy = []
    #     #     for child in children:
    #     #         child_int = int(child)
    #     #         solved, sub_policy = or_search(child_int, visited)
    #     #         if not solved:
    #     #             return False, None
    #     #         policy.append((child_int, sub_policy))
    #     #     return True, policy

    #     solved, policy = or_search(integer_state, visited)
    #     self.time_taken = float(time.time() - start_time)
    #     self.counter = len(visited)

    #     if solved:
    #         self.path = policy
    #         self.cost = len(policy) -1
    #         self.depth = self.cost
    #         return policy, self.cost, self.counter, self.depth, self.time_taken
    #     else:
    #         return [], self.cost, self.counter, self.depth, self.time_taken
    # def AndOrGraphSearch(self, inputState):
    #     """Thuật toán AND-OR Graph Search cho bài toán 8-puzzle"""
    #     start_time = time.time()
    #     integer_state = int(inputState)
    #     visited = set()
    #     queue = deque([(integer_state, [integer_state])])
    #     parent = {integer_state: None} 

    #     while queue:
    #         self.counter += 1
    #         state, current_path = queue.popleft()

    #         if state in visited:
    #             continue
    #         visited.add(state)

    #         if goalTest(state):
    #             self.path = current_path
    #             self.cost = len(self.path) - 1
    #             self.depth = self.cost
    #             self.time_taken = float(time.time() - start_time)
    #             return self.path, self.cost, self.counter, self.depth, self.time_taken

    #         children = getChildren(getStringRepresentation(state))
    #         for child in children:
    #             child_int = int(child)
    #             if child_int not in visited:
    #                 queue.append((child_int, current_path + [child_int]))
    #                 parent[child_int] = state

    #     self.path = []
    #     self.cost = 0
    #     self.depth = 0
    #     self.time_taken = float(time.time() - start_time)
    #     return self.path, self.cost, self.counter, self.depth, self.time_taken
    def AndOrGraphSearch(self, inputState):
        """Thuật toán AND-OR Graph Search cho bài toán 8-puzzle (dùng DFS không đệ quy)"""
        start_time = time.time()
        integer_state = int(inputState)
        visited = set()
        stack = []
        parent = {integer_state: None}  
        stack.append(integer_state)

        while stack:
            self.counter += 1
            state = stack.pop() 

            if state in visited:
                continue
            visited.add(state)

            if goalTest(state):
                self.path = getPath(parent, int(inputState))
                self.cost = len(self.path) - 1
                self.depth = self.cost
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken

            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    stack.append(child_int)
                    parent[child_int] = state
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = float(time.time() - start_time)
        return self.path, self.cost, self.counter, self.depth, self.time_taken