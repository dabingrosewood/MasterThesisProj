import sys
from rng_seeds import *


POPULATION_SIZE = 196
NUMBER_OF_ITERATIONS = 51
ELITISM = 196
TOURNAMENT = 14
PROB_CROSSOVER = 0.031999726672843454
PROB_MUTATION = 0.12168805178837176
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
