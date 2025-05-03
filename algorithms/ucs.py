# algorithms/ucs.py
import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation


class UCSAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0

    def UCS(self, inputState):
        start_time = time.time()
        pq = []
        visited = set()
        parent = {}
        parent_cost = {}
        integer_state = int(inputState)
        heapq.heappush(pq, (0, integer_state))
        counter = 0
        parent_cost[integer_state] = 0

        while pq:
            counter += 1
            curr_cost, state = heapq.heappop(pq)

            if goalTest(state):
                path = getPath(parent, int(inputState))
                self.counter = counter
                self.path = path
                self.cost = len(path) - 1
                self.depth = len(path) - 1
                self.time_taken = float(time.time() - start_time)
                return (
                    self.path,
                    self.cost,
                    self.counter,
                    self.depth,
                    self.time_taken,
                )

            if state not in visited:
                visited.add(state)

                children = getChildren(getStringRepresentation(state))
                for child in children:
                    child_int = int(child)
                    new_cost = curr_cost + 1
                    # nếu đã từng duyệt rồi nhưng h chi phí thấp hơn thì chấp nhận
                    if child_int not in visited or new_cost < parent_cost.get(
                        child_int, float("inf")
                    ):
                        heapq.heappush(pq, (new_cost, child_int))
                        parent[child_int] = state
                        parent_cost[child_int] = new_cost

        self.time_taken = float(time.time() - start_time)
        return None, 0, counter, self.depth, self.time_taken
