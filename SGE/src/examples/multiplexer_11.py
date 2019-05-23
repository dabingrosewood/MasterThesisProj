"""
#    This file was adapted from the DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.
"""

from util.interface.interface import eval_multiplexer

class Multiplexer_11:
    def evaluate(self, individual):
        """

        SOLUTION="( i3 and ( not i2 ) and ( not i1 ) and ( not i0 ) ) or ( i4 and ( not i2 ) and ( not i1 ) and ( i0 ) ) or ( i5 and ( not i2 ) and ( i1 ) and ( not i0 )) or ( i6 and ( not i2 ) and ( i1 ) and ( i0 ) ) or ( i7 and i2 and not( i1 ) and not ( i0 ) ) or ( i8 and i2 and ( not i1 ) and i0 ) or ( i9 and i2 and i1 and ( not i0 ) ) or ( i10 and i2 and i1 and i0 )"
        """
        error=eval_multiplexer(individual,3)

        return (error, {})


if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    experience_name = "Mux11/"
    grammar = grammar.Grammar("../grammars/mux11.bnf", 5)
    evaluation_function = Multiplexer_11() 
    core.sge.evolutionary_algorithm(grammar = grammar, eval_func=evaluation_function, exp_name=experience_name)