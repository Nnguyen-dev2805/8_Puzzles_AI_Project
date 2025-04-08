# algorithms/ids.py
import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation

class IDSAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    def IDS(self, inputState):
        start_time = time.time()
        integer_state = int(inputState)
        counter = 0

        def depth_limited_search(state, depth_limit, visited, parent, parent_cost):
            nonlocal counter
            counter += 1
            if goalTest(state):
                return True, getPath(parent, integer_state)
            if parent_cost[state] >= depth_limit:
                return False, []
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
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1
                self.depth = len(path) - 1
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken
            depth_limit += 1

        self.time_taken = float(time.time() - start_time)
        return [], 0, counter, self.depth, self.time_taken