import sys
from rng_seeds import *


POPULATION_SIZE = 721
NUMBER_OF_ITERATIONS = 50
ELITISM = 297
TOURNAMENT = 3
PROB_CROSSOVER = 0.7284303222253719
PROB_MUTATION = 0.4339305160308168
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]


MAX_REC_LEVEL= 5