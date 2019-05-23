from fitness.base_ff_classes.base_ff import base_ff
from utilities.stats.eval_counter import eval_counter

from fitness.cython.interface import eval_ant

class ant(base_ff):



    """
    best='ifa begin ' 'mv' ' end begin ' 'tl' 'ifa begin ' 'ifa begin ' 'mv' ' end begin ' 'tr' ' end' ' end begin ' 'tr' 'tl' 'tr' ' end' 'ifa begin ' 'mv' ' end begin ' 'tl' ' end' 'mv' ' end' 
    """

    maximise = False  # True as it ever was.

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    @eval_counter
    def evaluate(self, ind, **kwargs):
        # print(ind.phenotype)
        f=eval_ant(ind.phenotype)

        return f
