import random
import time
from algorithms.common import goalTest, manhattanDistance

class GeneticAlgorithm:
    def __init__(self):
        self.counter = 0
        self.time_taken = 0
        self.path = []
        self.cost = 0
        self.depth = 0

    @staticmethod
    def is_solvable(state):
        state = list(map(int, str(state)))
        inversions = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                    inversions += 1
        return inversions % 2 == 0

    def GeneticSearch(self, initialState, population_size=100, generations=1000, mutation_rate=0.2):
        """Thuật toán di truyền để giải bài toán 8-puzzle"""
        start_time = time.time()

        def create_individual():
            while True:
                state = list(str(initialState))
                random.shuffle(state)
                individual = int("".join(state))
                if GeneticAlgorithm.is_solvable(individual):
                    return individual

        def repair_individual(individual):
            digits = list(map(int, str(individual)))
            missing = [x for x in range(9) if x not in digits]
            duplicates = [x for x in digits if digits.count(x) > 1]

            for i in range(len(digits)):
                if digits[i] in duplicates:
                    digits[i] = missing.pop(0)
                    duplicates.remove(digits[i])

            return int("".join(map(str, digits)))

        def fitness(state):
            # max_fitness = 36
            # return max_fitness - manhattanDistance(state)
            return 1 / (1 + manhattanDistance(state))


        def crossover(parent1, parent2):
            p1 = list(str(parent1))
            p2 = list(str(parent2))
            split = random.randint(1, len(p1) - 2)
            child = p1[:split] + [x for x in p2 if x not in p1[:split]]
            return repair_individual(int("".join(child)))

        def mutate(state):
            state = list(str(state))
            i, j = random.sample(range(len(state)), 2)
            state[i], state[j] = state[j], state[i]
            return repair_individual(int("".join(state)))

        population = [create_individual() for _ in range(population_size)]
        population = list(set(population))  # Loại bỏ cá thể trùng lặp
        chromosome_map = {state: [] for state in population}

        best_fitness = float('-inf')
        no_improvement_count = 0

        for generation in range(generations):
            self.counter += 1

            population = sorted(population, key=fitness, reverse=True)

            if goalTest(population[0]):
                self.solution = population[0]
                self.time_taken = time.time() - start_time
                self.path = chromosome_map[self.solution]
                self.cost = len(self.path)
                self.depth = self.cost
                return self.path, self.cost, self.depth, self.counter, self.time_taken

            current_best_fitness = fitness(population[0])
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if no_improvement_count >= 20 or len(set(population)) == 1:
                print("Không có cải thiện hoặc quần thể bị thoái hóa, thuật toán dừng.")
                break

            next_generation = population[:population_size // 2]

            while len(next_generation) < population_size:
                parent1, parent2 = random.sample(next_generation, 2)
                child = crossover(parent1, parent2)
                if random.random() < mutation_rate:
                    child = mutate(child)
                next_generation.append(child)
                chromosome_map[child] = chromosome_map[parent1] + [child]

            population = list(set(next_generation))

        self.time_taken = time.time() - start_time
        return [], 0, 0, self.counter, self.time_taken