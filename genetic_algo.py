from typing import List, Callable, Tuple
import random
from functools import partial

matrix = List[List[int]]
Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]


def find_best(populations, fitness_func: FitnessFunc):
    min_distance = float('inf')
    min_genome = []
    for genome in populations:
        if fitness_func(genome) < min_distance:
            min_distance = fitness_func(genome)
            min_genome = genome
    return min_genome


def find_worst(populations, fitness_func: FitnessFunc):
    max_distance = -1  # distance > 0
    max_genome = []
    for genome in populations:
        if fitness_func(genome) > max_distance:
            max_distance = fitness_func(genome)
            max_genome = genome
    return max_genome


def crossover(a: Genome, b: Genome) -> Genome:  # Performs crossover between two parent genomes to create an offspring.
    offspring = []
    start = random.randint(0, len(a) - 1)
    finish = random.randint(start + 1, len(a))
    suba = a[start:finish]
    remaning_cities_from_b = [city for city in b if city not in suba]
    for i in range(len(a)):
        if start <= i < finish:
            offspring.append(suba.pop(0))
        else:
            offspring.append(remaning_cities_from_b.pop(0))
    return offspring


def mutation(genome: Genome, num: int,
             probability: float) -> Genome:  # Applies mutations to a genome with a specified probability.
    for _ in range(num):
        index1, index2 = random.randrange(1, len(genome)), random.randrange(1, len(genome))
        if random.random() < probability:
            genome[index1], genome[index2] = genome[index2], genome[index1]

    return genome


def genome_to_string(genome: Genome) -> str:  # Converts a genome to a string for printing.
    return "-".join(map(str, genome))


class Genetic:

    def __init__(self, distance_matrix, population_size, generation_limit):
        self.distance_matrix = distance_matrix
        self.genome_size = len(distance_matrix)
        self.population_size = population_size
        self.population: Population = []
        self.generation_limit = generation_limit
        self.mutations_probability = 0.09
        self.mutations_num: int = 4
        self.generation = 0

    def generate_genome(self) -> Genome:  # Generates a random genome (sol).
        random_path = list(range(1, len(self.distance_matrix)))
        random.shuffle(random_path)
        return [0] + random_path

    def generate_population(self):  # -> Population:  # Generates a population of genomes.
        self.population = [self.generate_genome() for _ in range(self.population_size)]

    def apply_crossovers_and_mutations(self, survivors: Population) -> Population:
        # Applies crossovers and mutations to create offspring from a set of survivors.
        offsprings = []
        halfway = len(survivors) // 2
        for i in range(halfway):
            a, b = survivors[i], survivors[i + halfway]
            offsprings.append(mutation(crossover(a, b), self.mutations_num, self.mutations_probability))
            offsprings.append(mutation(crossover(b, a), self.mutations_num, self.mutations_probability))

        return offsprings

    def fitness(self, g: Genome) -> int:  # Computes the fitness of a genome based on a distance matrix.
        return sum([self.distance_matrix[g[i - 1]][g[i]] for i in range(len(g))])

    def population_fitness(self, fitness_func: FitnessFunc) -> int:  # Computes the total fitness of a population.
        return sum([fitness_func(genome) for genome in self.population])

    def thanos_snap_the_population(self, fitness_func: FitnessFunc):
        # Selects survivors from the population based on their fitness.
        survivors = []
        random.shuffle(self.population)
        halfway = len(self.population) // 2
        for i in range(halfway):
            if fitness_func(self.population[i]) < fitness_func(self.population[i + halfway]):
                survivors.append(self.population[i])
            else:
                survivors.append(self.population[i + halfway])
        return survivors

    def generate_new_generation(self, fitness_func: FitnessFunc) -> Population:
        # Generates a new generation by combining survivors and their offspring.
        survivors = self.thanos_snap_the_population(fitness_func)
        new_generation = survivors + self.apply_crossovers_and_mutations(survivors)
        return new_generation

    def sort_population(self, fitness_func: FitnessFunc) -> Population:
        # Sorts the population based on fitness.
        return sorted(self.population, key=fitness_func)

    def print_stats(self, generation_id: int, fitness_func: FitnessFunc):
        # Prints statistics for a generation.
        print(f"GENERATION {generation_id}")
        print("=============")
        print("Populations: [%s]" % ", ".join([genome_to_string(gene) for gene in self.population]))
        print("Avg: %f" % (self.population_fitness(fitness_func) / len(self.population)))
        best = find_best(self.population, self.fitness)
        worst = find_worst(self.population, self.fitness)
        print("Best: %f\n" % fitness_func(best))
        print("Worst: %f\n" % fitness_func(worst))
        print(
            "Best Route: %s\n" % (genome_to_string(best)))
        print(
            "Worst Route: %s\n" % (genome_to_string(worst)))

        return best

    def print_stats_to_file(self, generation_id: int, fitness_func: FitnessFunc, output_file):
        # Writes statistics for a generation into the output file.
        output_file.write(f"GENERATION {generation_id}\n")
        output_file.write("=============\n")
        output_file.write("Populations: [%s]\n" % ", ".join([genome_to_string(gene) for gene in self.population]))
        output_file.write("Avg: %f\n" % (self.population_fitness(fitness_func) / len(self.population)))
        best = find_best(self.population, self.fitness)
        worst = find_worst(self.population, self.fitness)
        output_file.write("Best: %f\n" % fitness_func(best))
        output_file.write("Worst: %f\n" % fitness_func(worst))
        output_file.write(
            "Best Route: %s\n" % (genome_to_string(best)))
        output_file.write(
            "Worst Route: %s\n" % (genome_to_string(worst)))
        output_file.write("\n")
        return best

    def run_evolution(self, output_file=None) \
            -> Tuple[Genome, int, int]:
        self.generate_population()  # Runs the genetic algorithm for a specified number of generations.
        optimal = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        optimal_distance = self.fitness(optimal)
        best = []
        for i in range(self.generation_limit):
            # self.population = self.sort_population(partial(self.fitness))
            best = find_best(self.population, self.fitness)
            if optimal_distance > self.fitness(best):
                optimal = best
                optimal_distance = self.fitness(best)
            if output_file is not None:
                self.print_stats_to_file(i, partial(self.fitness), output_file)
            next_generation = self.generate_new_generation(partial(self.fitness))
            self.population = next_generation
        # self.population = self.sort_population(partial(self.fitness))
        if optimal_distance > self.fitness(best):
            optimal = best
            optimal_distance = self.fitness(best)
        if output_file is not None:
            self.print_stats_to_file(self.generation_limit, partial(self.fitness), output_file)

        return optimal, optimal_distance, self.generation_limit

    def run(self, output) \
            -> Tuple[Genome, Genome, int]:
        # Runs the genetic algorithm step by step.
        best = find_best(self.population, self.fitness)
        worst = find_worst(self.population, self.fitness)
        #   self.print_stats(self.generation, partial(self.fitness))
        self.print_stats_to_file(self.generation, partial(self.fitness), output)
        next_generation = self.generate_new_generation(partial(self.fitness))
        self.population = next_generation
        self.generation += 1

        return best, worst, self.generation
