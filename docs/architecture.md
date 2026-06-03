# Architecture Notes

Traveling Fan combines a Pygame interface with a genetic algorithm that searches for shorter stadium routes.

## Core Modules

- `main.py` starts the visual application.
- `manager.py` owns the UI loop, current stadium set, algorithm generation count, and drawing behavior.
- `genetic_algo.py` contains the route genome model, selection, crossover, mutation, and fitness calculation.
- `stadium.py` and `utils.py` provide drawing helpers and distance calculations.
- `data/` stores stadium coordinates, constants, images, generated route outputs, and experiment plots.

## Verification

The automated test suite focuses on deterministic genetic-algorithm behavior that can run in CI without opening the Pygame window. Full visual verification still happens manually by running `python main.py`.

