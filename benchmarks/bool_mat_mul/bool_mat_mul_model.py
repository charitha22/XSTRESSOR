from z3 import *
import random
import src.path_analyzer as pa
import time
import sys
from src.utils import writeSolutionToFile

def bool_mat_mul(A, B):
    
    #print(A)
    #print(B)
    A_sym_ = [BoolVector("A_bool_sym_"+str(i)+"_", len(A)) for i in range(0, len(A))]
    B_sym_ = [BoolVector("B_bool_sym_"+str(i)+"_", len(B)) for i in range(0, len(B))]
    path_cond = []
    #print(A_sym_)

    result = [[False for i in range(0, len(A))] for j in range(0,len(A))]

    for i in range(0,len(A)):
        path_cond.append("l1_s")
        for j in range(0, len(A)):
            path_cond.append("l2_s")

            value = False
            for k in range(0, len(A)):
                value = value or (A[i][k] and B[k][j])
                
                if(value):
                    break
                else:
                    path_cond.append(Not(And(A_sym_[i][k], B_sym_[k][j])))

            result[i][j]  = value
            path_cond.append("l2_e")

        path_cond.append("l1_e")

    #print(result)
    # print(path_cond)
    # solve(path_cond)
    
    return path_cond



t1 = time.time()
# worst case inputs
A = [
[[False, False],[False, False]],
[[False, False, False],[False, False, False],[False, False, False]],
[[False, False, False, False],[False, False, False, False],[False, False, False, False],[False, False, False, False]],
[[False, False, False, False, False],[False, False, False, False, False],[False, False, False, False, False],[False, False, False, False, False],[False, False, False, False, False]],
[[False, False, False, False, False, False],[False, False, False, False, False, False],[False, False, False, False, False, False],[False, False, False, False, False, False],[False, False, False, False, False, False],[False, False, False, False, False, False]],
[[False, False, False, False, False, False, False],[False, False, False, False, False, False, False],[False, False, False, False, False, False, False],[False, False, False, False, False, False, False],[False, False, False, False, False, False, False],[False, False, False, False, False, False, False],[False, False, False, False, False, False, False]]
]

B = list(A)

wc_expressions = []

for i in range(0, len(A)):

    pc = bool_mat_mul(A[i], B[i])

    wc_expressions.append(pc)



# now process the path conditions and build a model
stime = time.time()
path_analyzer = pa.PathAnalyzer(wc_expressions)
path_analyzer.buildModel()

t2 = time.time()

large_scale = int(sys.argv[1])

[pc, sym_store, arrays] = path_analyzer.genScaleTest(large_scale)
sol = path_analyzer.solve(pc)
writeSolutionToFile(sol, large_scale)


t3 = time.time()
print "Model build time = ", t2-t1
print "Prediction  time = ", t3-t2



