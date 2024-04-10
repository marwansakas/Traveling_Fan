import matplotlib.pyplot as plt

from genetic_algo import Genetic
from stadiums_data import *


class Information:
    """class for graph ploting"""

    def __init__(self):
        self.all_best_fitness = []
        self.all_worst_fitness = []
        self.all_average_fitness = []
        self.num_of_gen = []
        self.best_fitness = 0

    def read_file(self, output_path):
        with open(output_path, "r") as my_file:
            lines = my_file.readlines()
            j = 0
            for i in range(3, len(lines), 9):
                best_fitness = float(lines[i + 1][6:].strip())
                self.best_fitness = best_fitness if best_fitness > self.best_fitness else self.best_fitness
                self.all_best_fitness.append(best_fitness)
                worst_fitness = float(lines[i + 2][7:].strip())
                self.all_worst_fitness.append(worst_fitness)
                average_fitness = float(lines[i][5:].strip())
                self.all_average_fitness.append(average_fitness)
                self.num_of_gen.append(j)
                j += 1

    def plot_graph(self):
        # x axis values
        x = self.num_of_gen
        # corresponding y axis values
        y1 = self.all_best_fitness
        y2 = self.all_worst_fitness
        y3 = self.all_average_fitness

        plt.figure(figsize=(10, 8))
        # plotting the points
        plt.plot(x, y1, color='black', label="Best Fitness")
        plt.plot(x, y2, color='gainsboro', label="Worst Fitness")
        plt.plot(x, y3, color='yellow', label="Average Fitness")

        # naming the x axis
        plt.xlabel('Number of generations')
        # naming the y axis
        plt.ylabel('Fitness values')

        # giving a title to my graph
        plt.title('Fitness/Generations')

        # show a legend on the plot
        plt.legend()

        # function to show the plot
        plt.show()


output_file_path_100 = "solution_100.txt"
output_file_path_500 = "solution_500.txt"
output_file_path_1000 = "solution_1000.txt"

with open(output_file_path_100, "w") as output_file:
    genetic_100 = Genetic(distance_values, population_size, 300)
    optimal_solution, optimal_distance, generation_limit = genetic_100.run_evolution(output_file)
    print(optimal_distance)

with open(output_file_path_500, "w") as output_file1:
    genetic_500 = Genetic(distance_values, population_size, 500)
    optimal_solution1, optimal_distance1, generation_limit1 = genetic_500.run_evolution(output_file1)
    print(optimal_distance1)

with open(output_file_path_1000, "w") as output_file2:
    genetic_1000 = Genetic(distance_values, population_size, 1000)
    optimal_solution2, optimal_distance2, generation_limit2 = genetic_1000.run_evolution(output_file2)
    print(optimal_distance2)


info_100 = Information()
info_100.read_file(output_file_path_100)
info_100.plot_graph()
info_500 = Information()
info_500.read_file(output_file_path_500)
info_500.plot_graph()
info_1000 = Information()
info_1000.read_file(output_file_path_1000)
info_1000.plot_graph()

