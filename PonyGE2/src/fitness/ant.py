from fitness.base_ff_classes.base_ff import base_ff
from utilities.stats.eval_counter import eval_counter

from fitness.cython.interface import eval_ant

class ant(base_ff):
    """
    wait to be modified
    # Py-max is a max-style problem where the goal is to generate a function
    # which outputs a large number. In the standard GP Max [Gathercole and
    # Ross] problem this function can only use the constant (0.5) and functions
    # (+, *). The Py-max problem allows more programming: numerical expressions,
    # assignment statements and loops. See pymax.pybnf.
    #
    # Chris Gathercole and Peter Ross. An adverse interaction between crossover
    # and restricted tree depth in genetic programming. In John R. Koza,
    # David E. Goldberg, David B. Fogel, and Rick L. Riolo, editors, Genetic
    # Programming 1996: Proceedings of the First Annual Conference.
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
