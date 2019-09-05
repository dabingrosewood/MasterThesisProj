from fitness.base_ff_classes.base_ff import base_ff

from utilities.stats.eval_counter import eval_counter
from fitness.cython.interface import eval_max_py


class max_py(base_ff):

    maximise = False  # True as it ever was.
    
    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
    
    def evaluate(self, ind, **kwargs):

        fitness=eval_max_py(ind.phenotype)

        # p, d = ind.phenotype, {}
        # exec(p, d)
        # fitness2 = d['XXX_output_XXX']  # this is the program's output: a number.
        #
        # print(fitness,fitness2)

        return fitness
