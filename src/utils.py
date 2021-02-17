import os
import sys
import re
from z3 import *
DBG = 0


class SymStore:

    def __init__(self):
        self.sym_store = {}
        self.ver_store = {}

    def getSymVar(self, var, idx_vec, isAssignment):
        idx = ""
        for i in idx_vec:
            idx += "___"+str(i)

        var_name = str(var) + "_sym__" + idx.lstrip("_")

        if var_name not in self.ver_store.keys():
            self.ver_store[var_name] = 0

        # if an assignment update the version number
        if(isAssignment):
            self.ver_store[var_name] += 1

        ver_num = self.ver_store[var_name]

        # variable name with version number
        var_name_with_ver = var_name+"___"+str(ver_num)

        if(var_name_with_ver not in self.sym_store.keys()):
            self.sym_store[var_name_with_ver] = Int(var_name_with_ver)

        return self.sym_store[var_name_with_ver]


def printDbgMsg(msg):
    if(DBG == 1):
        print("DEBUG : "+str(msg))


def printInfoMsg(msg):
    print("INFO : "+str(msg))


def printErrMsg(msg):
    print("ERROR : "+str(msg))


def allSame(values):
    for i in range(0, len(values)-1):
        if(values[i] != values[i+1]):
            return False

    return True


# write a solution to a file
def writeSolutionToFile(solution, scale):
    file_name = "output_"+str(scale)+".out"
    file = open(file_name, "w")

    for s in solution:
        file.write(s+"\n")

    file.close()


def dim_of_list(a):
    if not type(a) == list:
        return []
    return [len(a)] + dim_of_list(a[0])

# the serial data


def getDiff(data):
    diff_data = []

    for i in range(1, len(data)):
        diff_data.append(data[i]-data[i-1])

    return diff_data


def getArrayIndices(var_name):
    arr_indices = []
    idx_part = var_name.split("sym")[1].lstrip('_')
    words = idx_part.split("___")

    if(len(words) == 1):
        arr_indices.append(int(idx_part))

    else:
        for w in words:
            arr_indices.append(int(w))

    return arr_indices


# this function vists an ast node in post order
# and extract the values at leaves and also records
# the structure of the ast node
# Assume : leaves must be integer values
def visit(expr, pre_order, leaves):

    if(len(expr.children()) == 0):

        # TODO:  decide if the leaf is array element or constant??
        if("__" in str(expr.decl())):
            arr_idx = getArrayIndices(str(expr.decl()))
            for item in arr_idx:
                leaves.append(item)
            # give a unique name to the variable
            if(len(arr_idx) == 1):
                pre_order.append("var_"+str(expr.decl()).split("sym")[0])
            else:
                pre_order.append("var_"+"mda"+str(len(arr_idx)) +
                                 "_"+str(expr.decl()).split("sym")[0])

        elif(is_int_value(expr)):
            pre_order.append("const")
            leaves.append(int(str(expr)))

        elif("Array" in str(expr.sort())):
            pre_order.append(expr)
        else:
            print(expr)
            print expr.sort()
            print("Unknown type in leaf node of z3 expression!")
            sys.exit(-1)

        return
    else:
        pre_order.append(expr.decl())
        for c in expr.children():
            visit(c, pre_order, leaves)


def getPredStrucAndValueVec(expr):
    structure = []
    value_vec = []

    visit(expr, structure, value_vec)
    return [structure, value_vec]


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        last_idx = len(self.stack)-1

        if(last_idx == -1):
            return None
        else:
            last_val = self.stack[last_idx]
            del self.stack[last_idx]

            return last_val

    def printStack(self):
        print(self.stack)

    def top(self):
        last_idx = len(self.stack)-1
        if(last_idx == -1):
            return None
        else:
            return self.stack[last_idx]


if __name__ == "__main__":
    main()
