import pygame
from stadium import Stadium
from genetic_algo import Genetic
from utils import *
from data.stadiums_data import distance_values, stadiums_names, real_stadiums_points
from data.colors import White, Black, Gray, line_color, text_color, line_color1, text_color1
from data.constants import *
import sys

pygame.font.init()
pygame.init()
screen_info = pygame.display.Info()
pygame.display.set_caption("Traveling Fan Problem ⚽")
screen_width = screen_info.current_w
screen_height = screen_info.current_h
offset_x_min, offset_x_max, offset_y_min, offset_y_max = find_offset(screen_width, screen_height)


class Manager(object):
    size = (screen_width, screen_height)
    screen = pygame.display.set_mode(size)  # screen size
    show_index = True  # show index of stadium
    stadiums_num = 16  # number of the real stadiums.
    genetic = Genetic(distance_values, population_size, 300)  # the generation limit where added just for
    # run_evolution function, nothing to do with the visualization.
    generation = 300  # default number of generations

    def __init__(self, Stadiums=None, real_stadiums=True):
        if Stadiums is None:
            Stadiums = real_stadiums_points(self.size)

        self.Stadiums = Stadiums
        self.real_stadiums = real_stadiums
        if real_stadiums:
            self.record_distance = sum_real_distances(distance_values)  # cause real stadiums has its own data
        else:
            self.record_distance = sum_distance(self.Stadiums)
        self.optimal_routes = self.Stadiums.copy()
        self.current_list = self.Stadiums.copy()  # worst
        self.color = text_color
        self.line = line_color
        self.optimal_stadiums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def reset_genetic(self):  # when the user want to reset the process on same points
        if self.real_stadiums:
            self.genetic = Genetic(distance_values, population_size, 300)
        else:
            matrix = create_distance_matrix(self.Stadiums)
            self.genetic = Genetic(matrix, population_size, 300)

    def genetic_algorithm(self):
        output_filename = "output.txt"
        if self.genetic.generation <= self.generation:
            # same as run_evolution but for the generation that the user select
            if self.genetic.generation == 0:
                self.genetic.generate_population()
                with open(output_filename, "w") as output_file:
                    fittest, worst, gen = self.genetic.run(output_file)
            else:
                with open(output_filename, "a") as output_file:
                    fittest, worst, gen = self.genetic.run(output_file)
            for i in range(self.stadiums_num):
                self.current_list[i] = self.Stadiums[worst[i]]
            if self.genetic.fitness(fittest) < self.record_distance:
                for i in range(self.stadiums_num):
                    self.optimal_routes[i] = self.Stadiums[fittest[i]]
                    self.optimal_stadiums = fittest
                self.record_distance = self.genetic.fitness(fittest)
            self.draw_calculate_lines(True)

    def random_points(self):  # create random points for the user to see how it works.
        points = [
            (randint(offset_x_min, screen_width - offset_x_max), randint(offset_y_min, screen_height - offset_y_max))
            for i in range(self.stadiums_num)]
        self.Stadiums = [Stadium(x, y, stadium_image) for (x, y) in points]
        self.record_distance = sum_distance(self.Stadiums)
        self.optimal_routes = self.Stadiums.copy()
        self.current_list = self.Stadiums.copy()
        matrix = create_distance_matrix(self.Stadiums)
        self.genetic = Genetic(matrix, population_size, 300)

    def text(self, started=True):  # print the stat's to the screen
        text_font = pygame.font.SysFont("Times", 20)
        text_font1 = pygame.font.SysFont("Times", 20, 15)
        text_font2 = pygame.font.SysFont("Arial Black", 40)
        text_surface1 = text_font.render("Best distance : " + str(round(self.record_distance, 2)), False, self.color)
        text_surface2 = text_font.render(f"Genetic Algorithm - {self.generation}", False, self.color)
        if self.genetic.generation > self.generation:
            text_surface3 = text_font.render(f"Number of generations: {self.generation}", False, self.color)
        else:
            text_surface3 = text_font.render(f"Number of generations: {self.genetic.generation}", False, self.color)
        text_surface4 = text_font2.render("... Press ' SPACE ' to start ...", False, self.color)
        if self.real_stadiums:
            j = 170
            for i in range(len(self.optimal_stadiums)):
                text_surface = text_font1.render(
                    f"{stadiums_names[self.optimal_stadiums[i]]} - {i}",
                    False, self.color)
                self.screen.blit(text_surface, (100, j))
                j += 30
        self.screen.blit(text_surface1, (100, 80))
        self.screen.blit(text_surface2, (100, 50))
        self.screen.blit(text_surface3, (100, 20))
        if not started:
            self.screen.blit(text_surface4, (screen_width // 2, screen_height - 200))

    def draw_shortest_path(self):
        if len(self.optimal_routes) > 0:
            for j in range(self.stadiums_num):
                i = (j + 1) % self.stadiums_num
                pygame.draw.line(self.screen, self.line,
                                 (self.optimal_routes[j].x, self.optimal_routes[j].y),
                                 (self.optimal_routes[i].x, self.optimal_routes[i].y),
                                 line_thickness)
                self.optimal_routes[j].draw(self, self.show_index, j)

    def draw_stadiums(self):
        for stadium in self.Stadiums:
            stadium.draw(self)

    def draw_calculate_lines(self, draw_current):
        if draw_current:
            for i, point in enumerate(self.current_list):
                _i = (i + 1) % len(self.current_list)
                pygame.draw.line(self.screen, Gray, (point.x, point.y),
                                 (self.current_list[_i].x, self.current_list[_i].y), 1)

        else:
            for i, point in enumerate(self.Stadiums):
                _i = (i + 1) % len(self.Stadiums)
                pygame.draw.line(self.screen, Gray, (point.x, point.y), (self.Stadiums[_i].x, self.Stadiums[_i].y),
                                 1)

    def Background(self, color=None):
        if color is None:
            image_path = background_image  # Replace with the path to your image file
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (screen_width, screen_height))
            self.screen.blit(image, (0, 0))
            self.color = text_color
            self.line = line_color
        else:
            self.screen.fill(color)
            self.color = text_color1
            self.line = line_color1
