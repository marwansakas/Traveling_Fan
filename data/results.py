import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from genetic_algo import Genetic
from stadiums_data import stadiums_data_maps, distance_values, stadiums_names

genetic_algo = Genetic(distance_values, 10, 300)
optimized_route, optimal_distance, generation = genetic_algo.run_evolution()

lats, lons = zip(*stadiums_data_maps)
plt.scatter(lons, lats, color='blue', label='Stadiums')
for i in range(len(optimized_route) - 1):
    plt.plot([stadiums_data_maps[optimized_route[i]][1], stadiums_data_maps[optimized_route[i + 1]][1]],
             [stadiums_data_maps[optimized_route[i]][0], stadiums_data_maps[optimized_route[i + 1]][0]],
             linestyle='-', color='red')

for i, (lat, lon) in enumerate(zip(lats, lons)):
    image = plt.imread('Images/Soccer-Football-Stadium.png')
    imagebox = OffsetImage(image, zoom=0.05)
    ab = AnnotationBbox(imagebox, (lon, lat), frameon=False, pad=1)
    plt.gca().add_artist(ab)

# Adding labels, legend, and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.title('Optimized Route for World Cup 2026 Stadiums')

# Show the plot
plt.show()