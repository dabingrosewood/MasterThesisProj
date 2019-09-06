from fitness.base_ff_classes.base_ff import base_ff
from utilities.stats.eval_counter import eval_counter

from fitness.cython.interface import eval_parity

class parity5(base_ff):
    maximise = False  # True as it ever was.

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    @eval_counter
    def evaluate(self, ind, **kwargs):
        # print(ind.phenotype)
        f=eval_parity(ind.phenotype,5)
        # print(f)

        return f
