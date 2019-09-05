import sys
from rng_seeds import *


POPULATION_SIZE = 699
NUMBER_OF_ITERATIONS = 50
ELITISM = 434
TOURNAMENT = 23
PROB_CROSSOVER = 0.41176880050447806
PROB_MUTATION = 0.5059349761962667
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]


MAX_REC_LEVEL= 5