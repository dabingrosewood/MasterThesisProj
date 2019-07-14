import sys
from rng_seeds import *


POPULATION_SIZE = 798
NUMBER_OF_ITERATIONS = 50
ELITISM = 102
TOURNAMENT = 34
PROB_CROSSOVER = 0.3059681009637951
PROB_MUTATION = 0.7857861038503274
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
