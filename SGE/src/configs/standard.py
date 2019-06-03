import sys
from rng_seeds import *


POPULATION_SIZE = 1908
NUMBER_OF_ITERATIONS = 20
ELITISM = 176
TOURNAMENT = 18
PROB_CROSSOVER = 0.39100753672515653
PROB_MUTATION = 0.07446143333601214
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
