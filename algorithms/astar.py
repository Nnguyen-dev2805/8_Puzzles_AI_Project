# algorithms/astar.py
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

    def AStar(self, inputState):
        """Thuật toán A* sử dụng heuristic Manhattan Distance sự kết hợp giữa UCS và Greedy BFS cho bài toán 8-puzzle"""
        start_time = time.time()
        pq = []
        visited = {}
        parent = {}
        g_cost = {}
        integer_state = int(inputState)
        g_cost[integer_state] = 0
        h_cost = manhattanDistance(integer_state)
        f_cost = h_cost
        heapq.heappush(pq, (f_cost, 0, integer_state))
        counter = 0

        while pq:
            counter += 1
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
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken

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

        self.time_taken = float(time.time() - start_time)
        return None, 0, counter, self.depth, self.time_taken