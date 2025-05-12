# import time
# import heapq
# from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

# class GreedBestFirstSearchAlgorithm:
#     def __init__(self):
#         self.counter = 0
#         self.path = []
#         self.cost = 0
#         self.depth = 0
#         self.time_taken = 0

#     def BestFirstSearch(self, inputState):
#         start_time = time.time()
#         pq = []  
#         visited = set()
#         parent = {}
#         parent_cost = {}
#         integer_state = int(inputState)
        
#         parent[integer_state] = None
#         parent_cost[integer_state] = 0
#         manhattan_cost = manhattanDistance(integer_state)
#         heapq.heappush(pq, (manhattan_cost, integer_state))
        
#         while pq:
#             self.counter += 1
#             _, state = heapq.heappop(pq)
#             if state in visited:
#                 continue

#             if goalTest(state):
#                 self.path = getPath(parent, int(inputState))
#                 self.cost = len(self.path) - 1
#                 self.depth = len(self.path) - 1
#                 self.time_taken = float(time.time() - start_time)
#                 return self.path, self.cost, self.counter, self.depth, self.time_taken
                
#             visited.add(state)
                       
#             children = getChildren(getStringRepresentation(state))
#             for child in children:
#                 child_int = int(child)
#                 if child_int not in visited:
#                     parent_cost[child_int] = parent_cost[state] + 1
#                     new_manhattan_cost = manhattanDistance(child_int)
#                     heapq.heappush(pq, (new_manhattan_cost, child_int))
#                     parent[child_int] = state
#         self.time_taken = float(time.time() - start_time)
#         return [], 0, self.counter, self.depth, self.time_taken


import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class GreedBestFirstSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_pq_size = 0  # Kích thước tối đa của hàng đợi ưu tiên
        self.max_visited_size = 0  # Kích thước tối đa của visited

    def BestFirstSearch(self, inputState):
        start_time = time.perf_counter()  # Sử dụng perf_counter cho độ chính xác cao
        pq = []  
        visited = set()
        parent = {}
        parent_cost = {}
        integer_state = int(inputState)
        
        parent[integer_state] = None
        parent_cost[integer_state] = 0
        manhattan_cost = manhattanDistance(integer_state)
        heapq.heappush(pq, (manhattan_cost, integer_state))
        
        while pq:
            self.counter += 1

            # Cập nhật kích thước tối đa của hàng đợi ưu tiên
            if len(pq) > self.max_pq_size:
                self.max_pq_size = len(pq)

            # Cập nhật kích thước tối đa của visited
            if len(visited) > self.max_visited_size:
                self.max_visited_size = len(visited)

            _, state = heapq.heappop(pq)
            if state in visited:
                continue

            if goalTest(state):
                self.path = getPath(parent, int(inputState))
                self.cost = len(self.path) - 1
                self.depth = len(self.path) - 1
                self.time_taken = time.perf_counter() - start_time
                total_space = self.max_pq_size + self.max_visited_size
                return (self.path, self.cost, self.counter, self.depth, self.time_taken, total_space)
                
            visited.add(state)
                       
            children = getChildren(getStringRepresentation(state))
            for child in children:
                child_int = int(child)
                if child_int not in visited:
                    parent_cost[child_int] = parent_cost[state] + 1
                    new_manhattan_cost = manhattanDistance(child_int)
                    heapq.heappush(pq, (new_manhattan_cost, child_int))
                    parent[child_int] = state

        self.time_taken = time.perf_counter() - start_time
        total_space = self.max_pq_size + self.max_visited_size
        return [], 0, self.counter, self.depth, self.time_taken, total_space