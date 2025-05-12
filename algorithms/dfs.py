import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation


class DFSAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_stack_size = 0
        self.max_visited_size = 0

    def DFS(self, inputState):
        start_time = time.perf_counter()

        stack = []
        visited = set()
        parent = {}
        parent_cost = {}
        integer_state = int(inputState)
        stack.append(integer_state)
        counter = 0
        parent_cost[integer_state] = 0

        while stack:
            counter += 1
            if len(stack) > self.max_stack_size:
                self.max_stack_size = len(stack)

            state = stack.pop()
            if goalTest(state):
                    path = getPath(parent, int(inputState))
                    self.counter = counter
                    self.path = path
                    self.cost = len(path) - 1
                    self.depth = len(path) - 1
                    self.time_taken = time.perf_counter() - start_time
                    total_space = self.max_stack_size + self.max_visited_size
                    return (
                        self.path,
                        self.cost,
                        self.counter,
                        self.depth,
                        self.time_taken,
                        total_space
                    )
            
            if state not in visited:
                visited.add(state)
                children = getChildren(getStringRepresentation(state))
                for child in children:
                    child_int = int(child)
                    if child_int not in visited:
                        stack.append(child_int)
                        parent[child_int] = state
                        parent_cost[child_int] = 1 + parent_cost[state]
                        self.depth = max(self.depth, parent_cost[child_int])
                        
        self.time_taken = time.perf_counter() - start_time
        total_space = self.max_stack_size + self.max_visited_size
        return [], 0, counter, self.depth, self.time_taken,total_space
