import time
from collections import deque
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation

class AndOrGraphSearchAlgorithm:
    def __init__(self):
        self.counter = 0  
        self.path = []   
        self.cost = 0    
        self.depth = 0    
        self.time_taken = 0  

    def AndOrGraphSearch(self, inputState):
        start_time = time.time()
        integer_state = int(inputState) 

        queue = deque([(integer_state, [])])  # (trạng thái, kế hoạch hành động)
        visited = set([integer_state])        
        parent = {integer_state: None}        
        plan = {}                             

        while queue:
            self.counter += 1
            state, actions = queue.popleft()  

            if goalTest(state):
                self.path = getPath(parent, int(inputState))
                self.cost = len(self.path) - 1
                self.depth = self.cost
                self.time_taken = float(time.time() - start_time)
                return self.path, self.cost, self.counter, self.depth, self.time_taken

            if state in plan:
                continue

            children = getChildren(getStringRepresentation(state))
            children = [int(child) for child in children if int(child) not in visited]

            if not children:
                continue

            child_plans = []
            for child in children:
                visited.add(child)
                parent[child] = state
                child_actions = actions + [child] 
                queue.append((child, child_actions))
                child_plans.append(child)

            plan[state] = child_plans

        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = float(time.time() - start_time)
        return self.path, self.cost, self.counter, self.depth, self.time_taken