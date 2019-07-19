import sys
from rng_seeds import *


POPULATION_SIZE = 811
NUMBER_OF_ITERATIONS = 50
ELITISM = 271
TOURNAMENT = 44
PROB_CROSSOVER = 0.8741109232391596
PROB_MUTATION = 0.8551493629772271
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
