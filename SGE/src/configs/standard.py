import sys
from rng_seeds import *


POPULATION_SIZE = 400
NUMBER_OF_ITERATIONS = 50
ELITISM = 255
TOURNAMENT = 41
PROB_CROSSOVER = 0.5971679745535864
PROB_MUTATION = 0.19905763506133
RUN = len(sys.argv) > 1 and int(sys.argv[1]) or 0
# SEED is set to the RUN-th number in rng_seeeds.py
SEED = seeds[RUN]
sampling_snap = [0,25, 50]
