import sys
import time
from z3 import *
import src.path_analyzer as pa
from src.utils import writeSolutionToFile

# some programs can have specific intitial conditions
# these conditions should be added seperately


def getInitConditions(sym_store_N, N):
    init_conditions = []

    # add all the graph variables to sym store
    for i in range(0, N):
        for j in range(0, N):
            var_name = "var_mda3_graph__"+str(i+1)+"_"+str(j)+"_0"
            if(var_name not in list(sym_store_N.keys())):
                sym_store_N[var_name] = Int(var_name)

    for var in sym_store_N.keys():
        if "graph" in str(var):
            init_conditions.append(sym_store_N[var] >= 0)

    return init_conditions


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


def dijkstra(graph, src, V):
    INFINITY = 1000000

    dist = [INFINITY for i in range(0, V)]
    fixed = [False for i in range(0, V)]

    # symblic init
    path_cond = []
    sym_store = SymStore()

    dist[src] = 0

    for k in range(0, V):

        minval = -1
        min_dist = INFINITY

        for i in range(0, V):
            if((not fixed[i]) and (dist[i] < min_dist)):

                minval = i
                min_dist = dist[i]

        fixed[minval] = True

        path_cond.append("l1_s")

        for i in range(0, V):
            if((not fixed[i]) and (dist[minval]+graph[minval][i] < dist[i])):

                if(k != 0):
                    path_cond.append(sym_store.getSymVar("dist", [minval], False)+sym_store.getSymVar(
                        "graph", [minval, i], False) < sym_store.getSymVar("dist", [i], False))

                    # add assignment constraint
                    rhs = sym_store.getSymVar(
                        "dist", [minval], False)+sym_store.getSymVar("graph", [minval, i], False)
                    lhs = sym_store.getSymVar("dist", [i], True)
                    path_cond.append(rhs == lhs)

                else:
                    path_cond.append(sym_store.getSymVar("dist", [V], False)+sym_store.getSymVar(
                        "graph", [V, i], False) < sym_store.getSymVar("dist", [i], False))

                    # add assignment constraint
                    rhs = sym_store.getSymVar(
                        "dist", [V], False)+sym_store.getSymVar("graph", [V, i], False)
                    lhs = sym_store.getSymVar("dist", [i], True)
                    path_cond.append(rhs == lhs)

                dist[i] = dist[minval] + graph[minval][i]

                # handle the assignment statement

        path_cond.append("l1_e")

    return [dist, path_cond]


t1 = time.time()

scales = [3, 4, 5, 6, 7, 8, 9, 10]
wc_inputs = []
wc_expressions = []

# read inputs
for scale in scales:
    fname = "small_scale/input_"+str(scale)+".txt"
    inf = open(fname, "r")

    lines = inf.readlines()

    wc_input = [[] for i in range(0, scale)]

    line_count = 0
    for i in range(0, scale):
        for j in range(0, scale):
            val = int(lines[line_count])
            wc_input[i].append(val)
            line_count += 1

    wc_inputs.append(wc_input)

# run program for these inputs
for wc_input in wc_inputs:

    result = dijkstra(wc_input, 0, len(wc_input))

    wc_expressions.append(result[1])


path_analyzer = pa.PathAnalyzer(wc_expressions)
path_analyzer.buildModel()

t2 = time.time()
# prediction
N = int(sys.argv[1])
[pc_N, sym_store_N, arrays] = path_analyzer.genScaleTest(N)

# add initial conditions
pc_N = pc_N + getInitConditions(sym_store_N, N+2)

input_N = path_analyzer.solve(pc_N)
writeSolutionToFile(input_N, N)

t3 = time.time()
print "Model build time = ", t2-t1
print "Prediction  time = ", t3-t2
