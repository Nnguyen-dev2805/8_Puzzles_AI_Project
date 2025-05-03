# algorithms/idastar.py
import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class IDAStarAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    def IDAStar(self, inputState):
        """Thuật toán IDA* sử dụng heuristic Manhattan Distance kết hợp A* và IDS cho bài toán 8-puzzle"""
        start_time = time.time()
        integer_state = int(inputState)
        counter = 0

        def search(state, g_cost, f_limit, parent, visited):
            nonlocal counter, next_f_limit
            h_cost = manhattanDistance(state)
            f_cost = h_cost + g_cost

            if f_cost > f_limit:
                next_f_limit = min(next_f_limit, f_cost)
                return False, []
            
            if goalTest(state):
                return True, getPath(parent, integer_state)
            
            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    counter += 1
                    visited.add(child_int)
                    parent[child_int] = state
                    found, path = search(child_int, g_cost + 1, f_limit, parent, visited)
                    if found:
                        return True, path
            return False, []

        h_initial = manhattanDistance(integer_state)
        f_limit = h_initial
        while True:
            visited = set()
            parent = {}
            visited.add(integer_state)
            next_f_limit = float('inf')
            found, path = search(integer_state, 0, f_limit, parent, visited)

            if found:
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1
                self.depth = len(path) - 1
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken
            
            if next_f_limit == float('inf'):
                self.counter = counter
                self.time_taken = float(time.time() - start_time)
                return [], 0, self.counter, self.depth, self.time_taken
            
            f_limit = next_f_limit