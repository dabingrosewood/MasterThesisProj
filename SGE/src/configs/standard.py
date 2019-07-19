import sys
from rng_seeds import *


POPULATION_SIZE = 809
NUMBER_OF_ITERATIONS = 50
ELITISM = 454
TOURNAMENT = 12
PROB_CROSSOVER = 0.27245546335847953
PROB_MUTATION = 0.04870809356287287
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
