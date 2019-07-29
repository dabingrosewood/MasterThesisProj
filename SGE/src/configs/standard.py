import sys
from rng_seeds import *


POPULATION_SIZE = 769
NUMBER_OF_ITERATIONS = 50
ELITISM = 499
TOURNAMENT = 5
PROB_CROSSOVER = 0.14848269815650755
PROB_MUTATION = 0.0634640154362045
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]


MAX_REC_LEVEL= 5