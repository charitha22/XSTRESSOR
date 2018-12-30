from z3 import *
import random
import src.path_analyzer as pa
import time
from src.utils import writeSolutionToFile

# targte program 
def isort(A):

    # A is an intvector
    A_sym_ = IntVector("A_sym_", len(A))
    path_cond = [] # path condition + loop boundries

    for i in range(1, len(A)):       
        x = A[i]
        x_ = A_sym_[i]
        j = i -1

        path_cond.append("l1_s")
        
        while(j >= 0 and A[j] > x):
            path_cond.append(A_sym_[j]>x_)    
            
            A[j+1] =  A[j]
            A_sym_[j+1] = A_sym_[j]
            j = j - 1

    
        A[j+1] = x
        A_sym_[j+1] = x_

        path_cond.append("l1_e")
        

    # return the solver
    return [A, path_cond]


# worst case inputs
wc_inputs = [
# [1],
# [2,1],
# [3,2,1],
[4,3,2,1],
[5,4,3,2,1],
[6,5,4,3,2,1],
[7,6,5,4,3,2,1],
[8,7,6,5,4,3,2,1],
[9,8,7,6,5,4,3,2,1]

]

wc_expressions = []

t1 = time.time()
for i in range(0, len(wc_inputs)):

    result = isort(wc_inputs[i])

    wc_expressions.append(result[1])

#print(wc_expressions)

# now process the path conditions and build a model

path_analyzer = pa.PathAnalyzer(wc_expressions)
path_analyzer.buildModel()


t2 = time.time()

large_scale = 100

[pc, sym_store, arrays] = path_analyzer.genScaleTest(large_scale)
sol = path_analyzer.solve(pc)
writeSolutionToFile(sol, large_scale)

t3 = time.time()
print "Model build time = ", t2-t1
print "Prediction  time = ", t3-t2



