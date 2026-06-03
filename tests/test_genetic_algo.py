import random
import unittest

from genetic_algo import Genetic, crossover, find_best, mutation


class GeneticAlgorithmTest(unittest.TestCase):
    def setUp(self):
        self.distance_matrix = [
            [0, 2, 9, 10],
            [1, 0, 6, 4],
            [15, 7, 0, 8],
            [6, 3, 12, 0],
        ]

    def test_fitness_sums_route_edges(self):
        genetic = Genetic(self.distance_matrix, population_size=4, generation_limit=3)

        self.assertEqual(genetic.fitness([0, 1, 3, 2]), 33)

    def test_crossover_preserves_each_city_once(self):
        random.seed(1)

        child = crossover([0, 1, 2, 3], [0, 3, 2, 1])

        self.assertEqual(sorted(child), [0, 1, 2, 3])

    def test_mutation_keeps_genome_membership(self):
        random.seed(2)
        genome = [0, 1, 2, 3]

        mutated = mutation(genome[:], num=5, probability=1.0)

        self.assertEqual(sorted(mutated), [0, 1, 2, 3])
        self.assertEqual(mutated[0], 0)

    def test_find_best_uses_lowest_fitness(self):
        population = [[0, 1, 2, 3], [0, 1, 3, 2], [0, 2, 1, 3]]
        genetic = Genetic(self.distance_matrix, population_size=4, generation_limit=3)

        self.assertEqual(find_best(population, genetic.fitness), [0, 1, 2, 3])


if __name__ == "__main__":
    unittest.main()
