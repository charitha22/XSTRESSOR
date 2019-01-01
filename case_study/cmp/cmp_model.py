import sys, os
from z3 import *
import random
import src.path_analyzer as pa
import time
from src.utils import writeSolutionToFile

path = "./wc_smt2s/"

def split_conditions(expr):
    
    splitted = []

    if(str(expr.decl()) != "And"):
        print("expr root is not AND")
        sys.exit(-1)

    for c in expr.children():
        # hack to simplify And(expr, True)
        if(str(c.decl())=="And" and str(c.children()[1])=="True"):
            splitted.append(c.children()[0])
        else:    

            splitted.append(c)

    return splitted
    
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
    
    return [path+f  for f in files]

def main():
     
    t1 = time.time()
    wc_smt_files = get_smt2_files()
    wc_path_conditions = read_wc_path_constraints(wc_smt_files)
    
    # print wc_path_conditions[0]

    # build model 
    path_analyzer = pa.PathAnalyzer(wc_path_conditions)
    path_analyzer.buildModel()
    t2 = time.time()



    large_scale = int(sys.argv[1])
    
    [pc, sym_store, arrays] = path_analyzer.genScaleTest(large_scale)
    sol = path_analyzer.solve(pc)
    writeSolutionToFile(sol, large_scale)

    t3 = time.time()

    print "Model build time = ", t2-t1
    print "Prediction  time = ", t3-t2


if __name__ == "__main__":
    main()
