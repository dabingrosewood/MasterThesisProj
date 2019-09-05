import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from util.cython.interface import eval_max_py


class MAX_PY:
    def evaluate(self, individual):

        # print(individual)
        error=eval_max_py(individual)

        return (error, {})


if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    import os
    from configs.standard import MAX_REC_LEVEL

    experience_name = "max_py/"
    grammar = grammar.Grammar("../grammars/max_py.bnf", 5)
    evaluation_function = MAX_PY()
    core.sge.evolutionary_algorithm(grammar=grammar, eval_func=evaluation_function, exp_name=experience_name)