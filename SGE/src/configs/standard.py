import sys
from rng_seeds import *


POPULATION_SIZE = 838
NUMBER_OF_ITERATIONS = 50
ELITISM = 188
TOURNAMENT = 34
PROB_CROSSOVER = 0.20903706940179123
PROB_MUTATION = 0.01740167888680022
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
