import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation


class BFSAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    def BFS(self, inputState):
        """Hàm BFS tìm kiếm theo chiều rộng cho bài toán 8-puzzle"""
        start_time = time.time()
        queue = []
        visited = set()
        parent = {}
        parent_cost = {}
        integer_state = int(inputState)
        queue.append(integer_state)
        couter = 0
        parent_cost[integer_state] = 0

        while queue:
            couter += 1
            state = queue.pop(0)

            if state in visited:
                continue

            if goalTest(state):
                path = getPath(parent, int(inputState))
                self.counter = couter
                self.path = path
                self.cost = len(path) - 1
                self.depth = parent_cost[state]
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken

            visited.add(state)

            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    queue.append(child_int)
                    parent[child_int] = state
                    parent_cost[child_int] = 1 + parent_cost[state]
        time_taken = float(time.time() - start_time)
        return None, 0, couter, self.depth, time_taken
