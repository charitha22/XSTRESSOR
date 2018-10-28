import sys
from z3 import *
import src.path_analyzer as pa


def bellmanford(V, graph, src):

    INFINITY = 1000000
    
    

    dist = [INFINITY for i in range(0,V)]
    infinite = [True for i in range(0,V)]
    
    # symbolic init
    path_cond = []
    graph_sym_ = [IntVector("graph_sym_"+str(i)+"_", V) for i in range(0,V)]
    dist_sym_ = IntVector("dist_sym_", len(dist))
    

    dist[src] = 0
    infinite[src] = False

    for k in range(0,V):
        relaxed = False
        for i in range(0, V):
            for j in range(0, V):
                if(i==j):
                    continue
                if(not infinite[i]):
                    if(dist[j] > dist[i]+graph[i][j]):
                        path_cond.append(dist_sym_[j]>dist_sym_[i]+graph_sym_[i][j])
                        
                        dist[j] = dist[i]+graph[i][j]
                        infinite[j] = False
                        relaxed = True
                        
                        path_cond.append([dist_sym_[j],dist_sym_[i]+graph_sym_[i][j]])
                        
        if(not relaxed):
            break
            
            
    return [dist, path_cond]
                    
            
scales = [3,4,5,6]
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
    
    
for input in wc_inputs:
    result = bellmanford(len(input), input, 0)
    
    wc_expressions.append(result[1])
    
    
for c in wc_expressions[2]:
    if(not isinstance(c, list)):
        print(c)
    




