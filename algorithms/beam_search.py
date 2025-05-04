import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class BeamSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    def BeamSearch(self, inputState, beam_width=2):
        start_time = time.time()
        integer_state = int(inputState)
        pq = [(manhattanDistance(integer_state), 0, integer_state)]
        visited = set()
        parent = {}
        parent_depth = {integer_state: 0}
        counter = 0

        while pq:
            counter += 1
            current_beam = []
            for _ in range(min(len(pq), beam_width)):
                if pq:
                    h_cost, depth, state = heapq.heappop(pq)
                    if state not in visited:
                        current_beam.append((h_cost, depth, state))

            if not current_beam:
                break

            for _, depth, state in current_beam:
                if state in visited:
                    continue
                visited.add(state)

                if goalTest(state):
                    path = getPath(parent, integer_state)
                    self.counter = counter
                    self.path = path
                    self.cost = len(path) - 1
                    self.depth = len(path) - 1
                    self.time_taken = float(time.time() - start_time)
                    return self.path, self.cost, self.counter, self.depth, self.time_taken
                
                children = getChildren(getStringRepresentation(state))
                next_beam = []
                for child in children:
                    child_int = int(child)
                    if child_int not in visited:
                        h_cost = manhattanDistance(child_int)
                        next_beam.append((h_cost, depth + 1, child_int))
                        parent[child_int] = state
                        parent_depth[child_int] = depth + 1

                next_beam.sort()
                for h_cost, new_depth, child_int in next_beam[:beam_width]:
                    heapq.heappush(pq, (h_cost, new_depth, child_int))

        self.counter = counter
        self.time_taken = float(time.time() - start_time)
        return [], 0, self.counter, self.depth, self.time_taken