import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from util.cython.interface import eval_parity
class Parity_5:
    def evaluate(self, individual):

        error=eval_parity(individual,5)

        return (error, {})


if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    from configs.standard import MAX_REC_LEVEL

    experience_name = "Parity5/"
    grammar = grammar.Grammar("../grammars/parity5.bnf", 5)
    evaluation_function = Parity_5()
    core.sge.evolutionary_algorithm(grammar = grammar, eval_func=evaluation_function, exp_name=experience_name)