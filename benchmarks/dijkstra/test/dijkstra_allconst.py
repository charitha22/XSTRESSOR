import sys
from z3 import *
import src.path_analyzer as pa
import src.model as mdl


def intVectorCopy(vec, name , idx):

    new_name = name+str(idx)
    new_vec = IntVector(new_name, len(vec))

    # for i in range(0, len(vec)):
    #     new_vec[i] = vec[i]
    #print(new_vec)
    return new_vec


# a = IntVector("a", 10)
# a[0] = 10  
# b = intVectorCopy(a, "a", 0)
# print(b)
# sys.exit()



def dijkstra(graph, src, V):
    INFINITY = 1000000
    idx = 0

    dist = [INFINITY for i in range(0,V)]
    fixed = [False for i in range(0,V)]

    # symblic init
    path_cond = []
    graph_sym_ = [IntVector("graph_sym_"+str(i)+"_", V) for i in range(0,V)]
    dist_sym_ = IntVector("dist_sym_", len(dist))
    prev_dist_sym_ = dist_sym_

    for i in range(0,V):
        for j in range(0,V):
            if(i==j):
                continue
            path_cond.append(graph_sym_[i][j]>=0)
    
    dist[src] = 0
    path_cond.append(dist_sym_[0]==0)

    for k in range(0,V):

        minval = -1
        min_dist = INFINITY

        for i in range(0,V):
            if((not fixed[i]) and (dist[i]<min_dist)):
                
                minval = i
                min_dist = dist[i]
                

        fixed[minval] = True

        path_cond.append("l1_s")

        for i in range(0,V):
            if((not fixed[i]) and (dist[minval]+graph[minval][i]<dist[i])):
                path_cond.append(prev_dist_sym_[minval]+graph_sym_[minval][i]<prev_dist_sym_[i])
                dist[i] = dist[minval] + graph[minval][i]

                new_dist_vec = intVectorCopy(prev_dist_sym_, "dist_sym_", idx)
                path_cond.append(new_dist_vec[i]==prev_dist_sym_[minval]+graph_sym_[minval][i])
                idx+=1
                prev_dist_sym_ = new_dist_vec
                # add lvalue and rvalue


        path_cond.append("l1_e")


    return [dist, path_cond]



scales = [3,4,5,6,7,8,9,10]
wc_inputs = []
wc_expressions = []

# read inputs
for scale in scales:
    fname = "small_scale/input_"+str(scale)+".txt"
    inf = open(fname, "r")

    lines = inf.readlines()

    wc_input = [[] for i in range(0,scale)]

    line_count = 0
    for i in range(0,scale):
        for j in range(0,scale):
            val = int(lines[line_count])
            wc_input[i].append(val)
            line_count+=1

    
    wc_inputs.append(wc_input)

# run program for these inputs

for wc_input in wc_inputs:

    result = dijkstra(wc_input, 0, len(wc_input))
    
    wc_expressions.append(result[1])
    

solvable_cond = [] 

for c in wc_expressions[1]:
    if(isinstance(c, str)):
        continue
    solvable_cond.append(c)


print(solvable_cond)

solve(solvable_cond)
# path_analyzer = pa.PathAnalyzer(wc_expressions, has_initial_cond=True)
# path_analyzer.buildModel() 
# path_analyzer.genScaleTest(1)


    