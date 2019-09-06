import sys
from rng_seeds import *


POPULATION_SIZE = 525
NUMBER_OF_ITERATIONS = 50
ELITISM = 466
TOURNAMENT = 27
PROB_CROSSOVER = 0.3806784568776531
PROB_MUTATION = 0.3818409923320236
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]


MAX_REC_LEVEL= 5