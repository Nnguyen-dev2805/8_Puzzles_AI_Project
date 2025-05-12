import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation


class IDSAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_stack_size = 0 
        self.max_visited_size = 0 

    def IDS(self, inputState):
        start_time = time.perf_counter()
        integer_state = int(inputState)
        counter = 0

        def depth_limited_search(state, depth_limit, parent, parent_cost, path_stack):
            nonlocal counter

            if parent_cost[state] > depth_limit:
                return False, []

            if goalTest(state):
                return True, getPath(parent, integer_state)

            path_stack.append(state)
            if len(path_stack) > self.max_stack_size:
                self.max_stack_size = len(path_stack)
            
            # Cập nhật kích thước tối đa đã thăm (dùng max_stack_size làm đại diện)
            if len(path_stack) > self.max_visited_size:
                self.max_visited_size = len(path_stack)
            children = getChildren(getStringRepresentation(state))

            for child in children:
                child_int = int(child)

                if child_int in path_stack:
                    continue

                counter += 1
                parent[child_int] = state
                parent_cost[child_int] = parent_cost[state] + 1

                found, path = depth_limited_search(
                    child_int, depth_limit, parent, parent_cost, path_stack
                )

                if found:
                    return True, path

            path_stack.pop()
            return False, []

        depth_limit = 0
        while True:
            parent = {integer_state: None}
            parent_cost = {integer_state: 0}
            path_stack = []

            found, path = depth_limited_search(
                integer_state, depth_limit, parent, parent_cost, path_stack
            )

            if found:
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1
                self.depth = len(path) - 1
                self.time_taken = float(time.perf_counter() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken, self.max_stack_size + self.max_visited_size

            depth_limit += 1
