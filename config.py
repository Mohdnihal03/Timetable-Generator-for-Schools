import os

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Algorithm configurations
GENETIC_ALGORITHM_CONFIG = {
    'POPULATION_SIZE': 50,
    'GENERATIONS': 100,
    'CROSSOVER_PROB': 0.7,
    'MUTATION_PROB': 0.2
}

# Time configurations
TIME_CONFIG = {
    'DAY_START': '9:00 AM',
    'DAY_END': '4:30 PM',
    'PERIOD_DURATION': 50
}