import sys
from rng_seeds import *


POPULATION_SIZE = 715
NUMBER_OF_ITERATIONS = 20
ELITISM = 80
TOURNAMENT = 5
PROB_CROSSOVER = 0.5641983139639315
PROB_MUTATION = 0.13337086936828496
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
