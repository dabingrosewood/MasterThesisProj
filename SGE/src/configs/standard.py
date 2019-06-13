import sys
from rng_seeds import *


POPULATION_SIZE = 450
NUMBER_OF_ITERATIONS = 20
ELITISM = 74
TOURNAMENT = 38
PROB_CROSSOVER = 0.9929669088911559
PROB_MUTATION = 0.1383521260161108
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
