import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from util.cython.interface import eval_ant


class ANT:
    def evaluate(self, individual):
        """
        SOLUTION = "ifa begin  mv  end begin  tl ifa begin  mv end begin  tr  end  tr ifa begin mv end begin  tl  end mv  end"
        """

        # print(individual)
        error=eval_ant(individual)

        return (error, {})


if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    import os
    from configs.standard import MAX_REC_LEVEL

    experience_name = "ant/"
    grammar = grammar.Grammar("../grammars/ant.bnf", 5)
    evaluation_function = ANT()
    core.sge.evolutionary_algorithm(grammar=grammar, eval_func=evaluation_function, exp_name=experience_name)