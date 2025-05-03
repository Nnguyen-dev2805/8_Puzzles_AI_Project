import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation
from collections import deque


class BFSAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    def BFS(self, inputState):
        start_time = time.time()
        queue = deque()
        visited = set()
        parent = {}
        parent_cost = {}
        integer_state = int(inputState)
        queue.append(integer_state)
        counter = 0
        parent_cost[integer_state] = 0

        while queue:
            counter += 1
            state = queue.popleft()

            if state in visited:
                continue

            if goalTest(state):
                path = getPath(parent, int(inputState))
                self.counter = counter
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
        return [], 0, counter, self.depth, time_taken
