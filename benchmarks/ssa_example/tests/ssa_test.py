from z3 import *


A = [1, -1, -1, -1, -1]
path_cond = []
sym_store = {}

def getSymVariable(var, idx, version):

    var_name = str(var) +"_"+ str(idx)+"_" + str(version)

    if(var_name not in sym_store.keys()):
        sym_store[var_name] = Int(var_name)

    return sym_store[var_name]


# idea is to give every variable a version number when assignment statements are present.
# we define the version number so that easily can be modeled using induction variable.
# we define the version w.r.t. the state of the loop nest. 

def ssa(A):

    for i in range(0, len(A)-1):
        if(A[i]>0):
            path_cond.append(getSymVariable("A", i, i) > 0)
            
            A[i+1] = -1*A[i+1]
            path_cond.append(getSymVariable("A", i+1, i+1) == -1*getSymVariable("A",i+1, i))

        else:
            break



ssa(A)

for c in path_cond:
    print(c)

solve(path_cond)

