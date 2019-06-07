import sys
from rng_seeds import *


POPULATION_SIZE = 1000
NUMBER_OF_ITERATIONS = 51
ELITISM = 100
TOURNAMENT = 12
PROB_CROSSOVER = 0.9
PROB_MUTATION = 0.2
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
