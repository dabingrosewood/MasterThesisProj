import sys
from rng_seeds import *


POPULATION_SIZE = 930
NUMBER_OF_ITERATIONS = 20
ELITISM = 70
TOURNAMENT = 29
PROB_CROSSOVER = 0.09268973797339197
PROB_MUTATION = 0.09077498575370926
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
