import sys
from rng_seeds import *


POPULATION_SIZE = 899
NUMBER_OF_ITERATIONS = 20
ELITISM = 68
TOURNAMENT = 18
PROB_CROSSOVER = 0.8333898468578903
PROB_MUTATION = 0.29815308134016705
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
