import sys
from z3 import *
import src.path_analyzer as pa

def dijkstra(graph, src, V):
    INFINITY = 1000000

    dist = [INFINITY for i in range(0,V)]
    fixed = [False for i in range(0,V)]

    # symblic init
    path_cond = []
    graph_sym_ = [IntVector("graph_sym_"+str(i)+"_", V) for i in range(0,V)]
    dist_sym_ = IntVector("dist_sym_", len(dist))
    
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
        min_dist_sym_ = Int("min_dist_sym_"+str(k))

        for i in range(0,V):
            if((not fixed[i]) and (dist[i]<min_dist)):
                #path_cond.append(dist_sym_[i] < min_dist_sym_)
                minval = i
                min_dist = dist[i]
                #path_cond.append([min_dist_sym_, dist_sym_[i]])
                #min_dist_sym_ = dist_sym_[i]

        fixed[minval] = True

        path_cond.append("l1_s")

        for i in range(0,V):
            if((not fixed[i]) and (dist[minval]+graph[minval][i]<dist[i])):
                
                # TODO : why k ? we can only predict the induction variable no the relation 
                # between minval vs k
                path_cond.append(dist_sym_[minval]+graph_sym_[minval][i]<dist_sym_[i])

                dist[i] = dist[minval] + graph[minval][i]
                # add lvalue and rvalue
                path_cond.append([dist_sym_[i] ,dist_sym_[minval]+graph_sym_[minval][i]])
                #dist_sym_[i] = dist_sym_[minval]+graph_sym_[minval][i]

        path_cond.append("l1_e")


    return [dist, path_cond]



scales = [3,4,5,6,7,8,9,10]
wc_inputs = []
wc_expressions = []

# read inputs
for scale in scales:
    fname = "../small_scale/input_"+str(scale)+".txt"
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

for wc_input in wc_inputs:



    result = dijkstra(wc_input, 0, len(wc_input))
    wc_expressions.append(result[1])

    # for c in path:
    #     print(c)

final_cond = []
sym_store = {}

def findInSymStore(expr):
    #print(expr)
    #print(expr.children())
    #print(sym_store)
    if(len(expr.children())==0):
        if(str(expr) in sym_store.keys()):
            #print("here")
            return findInSymStore(sym_store[str(expr)])
        else:
            #print("here1")
            return expr

    else:
        node = expr.decl()
        children = []
        for child in expr.children():
            children.append(findInSymStore(child))

        #print(children)
        return node(children)

# for i in range(0,len(wc_expressions)):
#     if(i==1):
#         for c in wc_expressions[i]:
#             if(isinstance(c, list)):
#                 #continue
#                 sym_store[str(c[0])]=c[1]
#                 #final_cond.append(c[0])
#             # elif(isinstance(c, str)):
#             #     continue
#             # else:
#             #     final_cond.append(c)


for i in range(0,len(wc_expressions)):
    if(i==4):
        for c in wc_expressions[i]:
            if(isinstance(c, list)):
                sym_store[str(c[0])]=c[1]
                #c[0]=c[1]
                #final_cond.append(c[0]>0)
            elif(isinstance(c, str)):
                continue
            else:
                #final_cond.append(c)
                final_cond.append(findInSymStore(c))

print(sym_store)

for c in final_cond:
    print(c)
solve(final_cond)




# path_analyzer = pa.PathAnalyzer(wc_expressions, has_initial_cond=True)
# path_analyzer.buildModel() 
# path_analyzer.genScaleTest(8)


    
