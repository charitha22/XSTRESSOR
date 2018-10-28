from z3 import *
import sys
import time
import src.path_analyzer as pa
from src.utils import writeSolutionToFile, SymStore


# idea is to give every variable a version number when assignment statements are present.
# we define the version number so that easily can be modeled using induction variable.
# we define the version w.r.t. the state of the loop nest. 

def ssa(A):

    sym_store = SymStore()
    path_cond = []

    for i in range(0, len(A)-1):
        if(A[i]>0):
            path_cond.append(sym_store.getSymVar("A", [i], [i]) > 0)
            
            A[i+1] = -1*A[i+1]
            path_cond.append(sym_store.getSymVar("A", [i+1], [i+1]) == -1*sym_store.getSymVar("A",[i+1], [i]))

        else:
            break
    
    return path_cond


wc_inputs = [

[1,-1],
[1,-1,-1],
[1,-1,-1,-1],
[1,-1,-1,-1,-1],
[1,-1,-1,-1,-1,-1],
[1,-1,-1,-1,-1,-1,-1]

]

wc_expressions = []

for i in range(0, len(wc_inputs)):

    result = ssa(wc_inputs[i])

    wc_expressions.append(result)


for c in wc_expressions[-1]:
    print(c)


# now process the path conditions and build a model
stime = time.time()

path_analyzer = pa.PathAnalyzer(wc_expressions)
path_analyzer.buildModel()

large_scale = 100

pc = path_analyzer.genScaleTest(large_scale)
sol = path_analyzer.solve(pc)
writeSolutionToFile(sol, large_scale)

etime = time.time()

print("Time elapsed : "+str(etime-stime))
