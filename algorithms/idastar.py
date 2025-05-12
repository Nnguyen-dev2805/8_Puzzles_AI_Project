import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class IDAStarAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_path_stack_size = 0 
        self.max_parent_size = 0  

    def IDAStar(self, inputState):
        start_time = time.perf_counter()  
        integer_state = int(inputState)
        counter = 0

        def search(state, g_cost, f_limit, parent, path_stack):
            nonlocal counter, next_f_limit, self
            h_cost = manhattanDistance(state)
            f_cost = h_cost + g_cost

            if len(path_stack) > self.max_path_stack_size:
                self.max_path_stack_size = len(path_stack)

            if len(parent) > self.max_parent_size:
                self.max_parent_size = len(parent)

            if f_cost > f_limit:
                next_f_limit = min(next_f_limit, f_cost)
                return False, []
            
            if goalTest(state):
                return True, getPath(parent, integer_state)
            
            children = getChildren(getStringRepresentation(state))
            path_stack.append(state)
            for child in children:
                child_int = int(child)
                if child_int in path_stack:
                    continue
                
                counter += 1
                parent[child_int] = state
                found, path = search(child_int, g_cost + 1, f_limit, parent, path_stack)
                if found:
                    return True, path
            path_stack.pop()
            return False, []

        h_initial = manhattanDistance(integer_state)
        f_limit = h_initial
        while True:
            parent = {}
            path_stack = []  # tránh lặp chu trình
            next_f_limit = float('inf')
            found, path = search(integer_state, 0, f_limit, parent, path_stack)

            if found:
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1
                self.depth = len(path) - 1
                self.time_taken = time.perf_counter() - start_time
                total_space = self.max_path_stack_size + self.max_parent_size
                return (self.path, self.cost, self.counter, self.depth, self.time_taken, total_space)
            
            if next_f_limit == float('inf'):
                self.counter = counter
                self.time_taken = time.perf_counter() - start_time
                total_space = self.max_path_stack_size + self.max_parent_size
                return [], 0, self.counter, self.depth, self.time_taken, total_space
            
            f_limit = next_f_limit