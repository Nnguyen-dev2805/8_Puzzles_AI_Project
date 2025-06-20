import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class AStarAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_pq_size = 0  
        self.max_visited_size = 0  

    def AStar(self, inputState):
        start_time = time.perf_counter()
        pq = []
        visited = {}
        parent = {}
        g_cost = {}
        integer_state = int(inputState)

        parent[integer_state] = None
        g_cost[integer_state] = 0
        h_cost = manhattanDistance(integer_state)
        f_cost = h_cost
        heapq.heappush(pq, (f_cost, 0, integer_state))
        counter = 0

        while pq:
            counter += 1

            if len(pq) > self.max_pq_size:
                self.max_pq_size = len(pq)
            
            if len(visited) > self.max_visited_size:
                self.max_visited_size = len(visited)

            f_cost, curr_cost, state = heapq.heappop(pq)

            if state in visited and curr_cost > visited[state]:
                continue

            visited[state] = curr_cost

            if goalTest(state):
                path = getPath(parent, int(inputState))
                self.counter = counter
                self.path = path
                self.cost = g_cost[state]
                self.depth = len(path) - 1
                self.time_taken = time.perf_counter() - start_time
                total_space = self.max_pq_size + self.max_visited_size
                return self.path, self.cost, self.counter, self.depth, self.time_taken,total_space

            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                new_g_cost = curr_cost + 1
                h_cost = manhattanDistance(child_int)
                new_f_cost = new_g_cost + h_cost

                if child_int not in visited or new_g_cost < visited[child_int]:
                    heapq.heappush(pq, (new_f_cost, new_g_cost, child_int))
                    parent[child_int] = state
                    g_cost[child_int] = new_g_cost

        self.time_taken = time.perf_counter() - start_time
        total_space = self.max_pq_size + self.max_visited_size
        return [], 0, counter, self.depth, self.time_taken,total_space