import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class SimpleHillClimbingAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_visited_size = 0

    def SimpleHillClimbing(self, inputState):
        start_time = time.time()
        integer_state = int(inputState)
        current_state = integer_state
        parent = {}
        visited = set()
        counter = 0
        depth = 0

        while True:
            counter += 1
            visited.add(current_state)

            if len(visited) > self.max_visited_size:
                self.max_visited_size = len(visited)

            if goalTest(current_state):
                path = getPath(parent, integer_state)
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1
                self.depth = len(path) - 1
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken,self.max_visited_size
            
            children = getChildren(getStringRepresentation(current_state))
            best_child = None
            best_heuristic = manhattanDistance(current_state)

            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    h_cost = manhattanDistance(child_int)
                    if h_cost < best_heuristic:
                        best_heuristic = h_cost
                        best_child = child_int
            
            if best_child is None:
                self.counter = counter
                self.depth = depth
                self.time_taken = float(time.time() - start_time)
                return [], 0, self.counter, self.depth, self.time_taken,self.max_visited_size

            parent[best_child] = current_state
            current_state = best_child
            depth += 1