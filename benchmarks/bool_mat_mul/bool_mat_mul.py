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



# input1 = [[False, False],[False, False]]
# input2 = list(input1)

# bool_mat_mul(input1, input2)
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

# print(wc_expressions[0])
# sys.exit(-1)


# now process the path conditions and build a model
stime = time.time()
path_analyzer = pa.PathAnalyzer(wc_expressions)
path_analyzer.buildModel()

large_scale = 10
pc = path_analyzer.genScaleTest(large_scale)
sol = path_analyzer.solve(pc)
writeSolutionToFile(sol, large_scale)


etime = time.time()

print("Time elapsed : "+str(etime-stime))
