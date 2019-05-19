import sys
from rng_seeds import *


POPULATION_SIZE = 1525
NUMBER_OF_ITERATIONS = 5
ELITISM = 98
TOURNAMENT = 19
PROB_CROSSOVER = 0.6030522290921541
PROB_MUTATION = 0.19244564875161554
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
