import sys
from rng_seeds import *


POPULATION_SIZE = 871
NUMBER_OF_ITERATIONS = 50
ELITISM = 345
TOURNAMENT = 20
PROB_CROSSOVER = 0.38591314298903034
PROB_MUTATION = 0.5581471170547168
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]


MAX_REC_LEVEL= 5