from z3 import *
import random
import src.path_analyzer as pa
import time
from src.utils import writeSolutionToFile

# merging 2 sorted arrays
def sorted_merge(A,B):

    result = []
    A_idx = 0
    B_idx = 0

    A_sym_ = IntVector("A_sym_",len(A))
    B_sym_ = IntVector("B_sym_",len(B))
    path_cond = []

    while(A_idx<len(A) and B_idx<len(B)):

        if(A[A_idx]<B[B_idx]):
            path_cond.append(A_sym_[A_idx]<B_sym_[B_idx])
            result.append(A[A_idx])
            A_idx+=1
        else:
            path_cond.append(A_sym_[A_idx]>=B_sym_[B_idx])
            result.append(B[B_idx])
            B_idx+=1

    while(A_idx<len(A)):
        result.append(A[A_idx])
        A_idx+=1

    while(B_idx<len(B)):
        result.append(B[B_idx])
        B_idx+=1

    return [result,path_cond]


t1 = time.time()
# worst case inputs
wc_inputs = [
[[1],[2]],
[[1,3],[2,4]],
[[1,3,5],[2,4,6]],
[[1,3,5,7],[2,4,6,8]],
[[1,3,5,7,9],[2,4,6,8,10]],
[[1,3,5,7,9,11],[2,4,6,8,10,12]],
[[1,3,5,7,9,11,13],[2,4,6,8,10,12,16]]
]

wc_expressions = []

for i in range(0, len(wc_inputs)):

    result = sorted_merge(wc_inputs[i][0],wc_inputs[i][1])
    wc_expressions.append(result[1])

# now process the path conditions and build a model
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


