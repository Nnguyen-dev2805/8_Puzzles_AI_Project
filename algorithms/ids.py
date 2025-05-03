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

        def depth_limited_search(state, depth_limit, parent, parent_cost):
            nonlocal counter
            if goalTest(state):
                return True, getPath(parent, integer_state)
            if parent_cost[state] >= depth_limit:
                return False, []
            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                if child_int not in parent:
                    counter += 1
                    parent[child_int] = state
                    parent_cost[child_int] = parent_cost[state] + 1
                    found, path = depth_limited_search(
                        child_int, depth_limit, parent, parent_cost
                    )
                    if found:
                        return True, path
            return False, []

        depth_limit = 0
        max_depth_limit= 1000 # giới hạn độ sâu tối đa
        # while True:
        while depth_limit <= max_depth_limit:
            parent = {integer_state: None}
            parent_cost = {integer_state: 0}
            found, path = depth_limited_search(
                integer_state, depth_limit, parent, parent_cost
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
        return [], 0, counter, self.depth, self.time_taken  # vì while True nên không bao giờ đến
