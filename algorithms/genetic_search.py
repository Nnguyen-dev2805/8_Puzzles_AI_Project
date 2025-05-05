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
        start_time = time.perf_counter()

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
            max_fitness = 36
            return max_fitness - manhattanDistance(state)

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

        population = []
        seen = set()
        seen.add(initialState)
        population.append(initialState) 
        while len(population) < population_size:
            individual = create_individual()
            if individual not in seen:
                seen.add(individual)
                population.append(individual)

        chromosome_map = {initialState: [initialState]}
        for state in population:
            if state != initialState:
                chromosome_map[state] = [state]

        best_fitness = float('-inf')
        best_individual = initialState
        no_improvement_count = 0

        for generation in range(generations):
            self.counter += 1

            # sắp xếp quần thể theo fitness
            population = sorted(population, key=fitness, reverse=True)

            # kiểm tra cá thể tốt nhất
            if goalTest(population[0]):
                self.solution = population[0]
                self.time_taken = time.perf_counter() - start_time
                self.path = chromosome_map[self.solution]
                self.cost = len(self.path) - 1
                self.depth = self.cost
                return self.path, self.cost, self.depth, self.counter, self.time_taken

            # Cập nhật fitness tốt nhất
            current_best_fitness = fitness(population[0])
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = population[0]
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            # điều kiện dừng
            if no_improvement_count >= 20 or len(set(population)) == 1:
                print("Không có sự cải thiện hoặc suy thoái dân số, dừng lại.")
                break

            # lựa chọn (Elitism + Tournament Selection)
            next_generation = population[:population_size // 4]  # giữ 1/4 tốt nhất

            while len(next_generation) < population_size:
                tournament_size = 5
                tournament = random.sample(population, min(tournament_size, len(population)))
                parent1 = max(tournament, key=fitness)
                tournament = random.sample(population, min(tournament_size, len(population)))
                parent2 = max(tournament, key=fitness)
                while parent2 == parent1 and len(population) > 1:
                    tournament = random.sample(population, min(tournament_size, len(population)))
                    parent2 = max(tournament, key=fitness)

                # lai ghép
                child = crossover(parent1, parent2)
                # đột biến
                if random.random() < mutation_rate:
                    child = mutate(child)

                # thêm cá thể con
                next_generation.append(child)
                # cập nhật chromosome_map
                if child not in chromosome_map:
                    chromosome_map[child] = chromosome_map[parent1] + [child]

            # loại bỏ trùng lặp và đảm bảo kích thước quần thể
            seen = set()
            population = []
            for individual in next_generation:
                if individual not in seen:
                    seen.add(individual)
                    population.append(individual)
            while len(population) < population_size:
                individual = create_individual()
                if individual not in seen:
                    seen.add(individual)
                    population.append(individual)
                    chromosome_map[individual] = [individual]

        # trả về cá thể tốt nhất nếu không tìm được giải pháp
        self.time_taken = time.perf_counter() - start_time
        if goalTest(best_individual):
            self.solution = best_individual
            self.path = chromosome_map[self.solution]
            self.cost = len(self.path) - 1
            self.depth = self.cost
            return self.path, self.cost, self.depth, self.counter, self.time_taken
        return [], 0, 0, self.counter, self.time_taken