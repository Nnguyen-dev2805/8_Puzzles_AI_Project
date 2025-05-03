# algorithms/simulatedannealing.py
import time
import random
import math
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class SimulatedAnnealingAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    def SimulatedAnnealing(self, inputState):
        start_time = time.time()
        integer_state = int(inputState)
        current_state = integer_state
        best_state = current_state
        parent = {current_state: None}
        temperature = 1000.0
        cooling_rate = 0.995
        min_temperature = 0.01
        counter = 0

        current_heuristic = manhattanDistance(current_state)
        best_heuristic = current_heuristic

        while temperature > min_temperature:
            counter += 1

            if goalTest(current_state):
                # print("Found goal state")
                path = getPath(parent, integer_state)
                # print("hehe");
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1
                self.depth = len(path) - 1
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken
            
            children = getChildren(getStringRepresentation(current_state))
            if not children:
                break

            next_state = int(random.choice(children))
            next_heuristic = manhattanDistance(next_state)
            delta_e = next_heuristic - current_heuristic

            if delta_e < 0 or random.random() < math.exp(-delta_e/temperature):
                parent[next_state] = current_state
                current_state = next_state
                current_heuristic = next_heuristic
                # self.depth += 1

            if current_heuristic < best_heuristic:
                best_state = current_state
                best_heuristic = current_heuristic

            temperature *= cooling_rate

        if best_state != integer_state:
            current_state = best_state
            if goalTest(current_state):
                path = getPath(parent, integer_state)
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1
                self.depth = len(path) - 1
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken
        print("Not found goal state")
        self.counter = counter
        self.time_taken = float(time.time() - start_time)
        return [], 0, self.counter, self.depth, self.time_taken