import sys
from rng_seeds import *


POPULATION_SIZE = 1946
NUMBER_OF_ITERATIONS = 50
ELITISM = 196
TOURNAMENT = 90
PROB_CROSSOVER = 0.1672710703417623
PROB_MUTATION = 0.3218853490927787
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
