import time
import random
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class StochasticHillClimbingAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    def StochasticHillClimbing(self, inputState):
        start_time = time.time()
        integer_state = int(inputState)
        current_state = integer_state
        parent = {current_state: None}
        visited = set()
        counter = 0
        depth = 0

        while True:
            counter += 1
            visited.add(current_state)

            if goalTest(current_state):
                path = getPath(parent, integer_state)
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1  
                self.depth = len(path) - 1 
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken

            children = getChildren(getStringRepresentation(current_state))
            better_children = []
            current_heuristic = manhattanDistance(current_state)

            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    h_cost = manhattanDistance(child_int)
                    if h_cost < current_heuristic:
                        better_children.append(child_int)

            if not better_children:
                self.counter = counter
                self.depth = depth
                self.time_taken = float(time.time() - start_time)
                return [], 0, self.counter, self.depth, self.time_taken

            next_state = random.choice(better_children)
            parent[next_state] = current_state
            current_state = next_state
            depth += 1