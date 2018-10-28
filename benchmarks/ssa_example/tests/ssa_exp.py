from z3 import *

A_version = [0, 0, 0, 0, 0]
A = [1, -1, -1, -1, -1]
path_cond = []
sym_store = {}

def getSymVariable(var, idx, version):

    var_name = str(var) +"_"+ str(idx)+"_v" + str(version)

    if(var_name not in sym_store.keys()):
        sym_store[var_name] = Int(var_name)

    return sym_store[var_name]


def ssa(A):

    for i in range(0, len(A)-1):
        if(A[i]>0):
            path_cond.append(getSymVariable("A", i, A_version[i])>0)
            A[i+1] = -1*A[i+1]
            path_cond.append(getSymVariable("A", i+1, A_version[i+1]+1) == -1*getSymVariable("A", i+1, A_version[i+1]))
            A_version[i+1]+=1



        else:
            break



ssa(A)

for i in range(0, len(path_cond)):
    print(path_cond[i])



solve(path_cond)

