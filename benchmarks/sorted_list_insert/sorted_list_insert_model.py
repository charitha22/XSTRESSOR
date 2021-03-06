from z3 import *
import time
import random
import src.path_analyzer as pa
from src.utils import writeSolutionToFile


def sorted_list_insert(array, number):

    number_sym_ = Int("number_sym___0")
    path_cond = []

    for i in range(0, len(array)):
        if(number <= array[i]):
            path_cond.append(number_sym_ <= array[i])
            array.insert(i, number)
            break
        else:
            path_cond.append(number_sym_ > array[i])

    return path_cond


t1 = time.time()

wc_inputs = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10
]

wc_expressions = []

for i in range(0, len(wc_inputs)):
    array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = sorted_list_insert(array, wc_inputs[i])

    wc_expressions.append(result)

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
