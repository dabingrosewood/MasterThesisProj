import sys
from rng_seeds import *


POPULATION_SIZE = 1856
NUMBER_OF_ITERATIONS = 20
ELITISM = 116
TOURNAMENT = 48
PROB_CROSSOVER = 0.9523458457274003
PROB_MUTATION = 0.6127086847277086
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
