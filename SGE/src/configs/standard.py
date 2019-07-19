import sys
from rng_seeds import *


POPULATION_SIZE = 947
NUMBER_OF_ITERATIONS = 50
ELITISM = 223
TOURNAMENT = 49
PROB_CROSSOVER = 0.4768538096800432
PROB_MUTATION = 0.7450874862465603
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
