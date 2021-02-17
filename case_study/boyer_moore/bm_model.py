import sys
import os
import re
from z3 import *
import random
import src.path_analyzer as pa
import time
from src.utils import writeSolutionToFile

path = "./wc_smt2s/"


def split_conditions(expr):

    splitted = []
    start = False

    # hack : need to remove contantant delta1
    # delta2 array constraints
    pattern = r'delta[1,2]\[[0-9]+\] == [0-9]+'

    if(str(expr.decl()) != "And"):
        print("expr root is not AND")
        sys.exit(-1)

    for c in expr.children():
        # hack to simplify And(expr, True)
        if(str(c.decl()) == "And" and str(c.children()[1]) == "True"):
            splitted.append(c.children()[0])

        elif(not start and "LB" in str(c)):
            splitted.append("l1_s")
            start = True
        elif(start and "LB" in str(c)):
            splitted.append("l1_e")
            start = False

        elif(re.search(pattern, str(c), re.M | re.I)):
            continue
        else:

            splitted.append(c)

    # this is a hack :(
    result = []
    bad_removed = False
    for c in reversed(splitted):

        if("!=" in str(c) and not bad_removed):
            bad_removed = True
        else:
            result.append(c)

    return list(reversed(result))[:-2]


def read_wc_path_constraints(files):

    path_conditions = []

    for f in files:
        # print f
        pc = parse_smt2_file(f)
        # print pc
        path_conditions.append(split_conditions(pc))

    return path_conditions


def get_smt2_files():

    files = os.listdir(path)
    # print files
    return [path+f for f in files]


def genDelta1Constraints(delta1):
    result = []

    for i in range(0, 256):
        if(i == 97):
            result.append(Select(delta1, i) == 2)
        elif(i == 98):
            result.append(Select(delta1, i) == 1)
        else:
            result.append(Select(delta1, i) == 3)

    return result


def genDelta2Constraints(delta2):

    result = []
    result.append(Select(delta2, 0) == 5)
    result.append(Select(delta2, 1) == 4)
    result.append(Select(delta2, 2) == 1)

    return result


def genInitialConstraints(symbolic_store, symbolic_arrays):

    conditions = []

    for array in symbolic_arrays:
        if("delta1" in str(array)):
            conditions += genDelta1Constraints(array)

        elif("delta2" in str(array)):
            conditions += genDelta2Constraints(array)

    return conditions


def main():
    t1 = time.time()
    wc_smt_files = get_smt2_files()
    wc_path_conditions = read_wc_path_constraints(wc_smt_files)

    # for c in wc_path_conditions[4]:
    # print c

    # build model
    path_analyzer = pa.PathAnalyzer(wc_path_conditions)
    path_analyzer.buildModel()

    t2 = time.time()

    large_scale = int(sys.argv[1])

    [pc, sym_store, arrays] = path_analyzer.genScaleTest(large_scale)
    pc = pc + genInitialConstraints(sym_store, arrays)

    # for c in pc:
    # print c

    # writeSolutionToFile(sol, large_scale)
    input_N = path_analyzer.solve(pc)
    writeSolutionToFile(input_N, large_scale)

    t3 = time.time()

    print "Model build time = ", t2-t1
    print "Prediction  time = ", t3-t2


if __name__ == "__main__":
    main()
