import sys
from rng_seeds import *


POPULATION_SIZE = 1521
NUMBER_OF_ITERATIONS = 5
ELITISM = 87
TOURNAMENT = 9
PROB_CROSSOVER = 0.8914965908448913
PROB_MUTATION = 0.2314804461048674
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
