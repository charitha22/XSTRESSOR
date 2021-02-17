import sys
from z3 import *
from utils import *


def findInSymStore(expr, sym_store):

    if(len(expr.children()) == 0):
        return expr

    else:
        node = expr.decl()
        children = []
        for child in expr.children():
            children.append(findInSymStore(child, sym_store))

        return node(children)


class ExprWriter:

    def __init__(self, predicate_structure, value_vector, symbolic_store):
        self.pstruct = predicate_structure
        self.values = value_vector
        self.symbolic_store = symbolic_store
        self.condition = self.constructZ3Expr(self.pstruct, self.values)

    def constructZ3Expr(self, structure, leaf_values):

        expr_stack = Stack()
        j = len(leaf_values) - 1

        for i in range(0, len(structure)):
            item = structure[len(structure) - 1 - i]

            if("var" in str(item)):
                # multi dimensional case
                if("mda" in str(item)):

                    dim = int(str(item).split("mda")[1].split("_")[0])
                    idx_str = ""
                    # print j
                    for d in range(0, dim):
                        idx_str += "_" + str(leaf_values[j - dim + 1 + d])

                    name = str(item) + idx_str
                    sym_var = self.symbolic_store[name]
                    sym_var = findInSymStore(sym_var, self.symbolic_store)
                    expr_stack.push(sym_var)

                    j -= dim

                # single dimensional case
                else:
                    name = str(item) + str(leaf_values[j])

                    sym_var = self.symbolic_store[name]
                    sym_var = findInSymStore(sym_var, self.symbolic_store)
                    expr_stack.push(sym_var)

                    j -= 1

            elif("const" in str(item)):
                expr_stack.push(leaf_values[j])
                j -= 1

            elif(is_array(item)):

                expr_stack.push(item)
                # j-=1

            else:
                if(str(item) == "Not"):
                    arg = expr_stack.pop()
                    expr_stack.push(item(arg))

                else:

                    arg1 = expr_stack.pop()
                    arg2 = expr_stack.pop()

                    expr_stack.push(item(arg1, arg2))

        return expr_stack.top()
