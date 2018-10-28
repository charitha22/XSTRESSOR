from z3 import *
import src.path_analyzer as pa
import src.model as mdl
import numpy as np
from src.utils import *

print("Test for extracting array indices")
s1 = "y_sym___7"
s2 = "graph_sym_0___1"

print(getArrayIndices(s1))
print(getArrayIndices(s2))


print("======Test end======\n")


print("Test for feature extraction from a z3 expression")


x = IntVector('x_sym_', 10)
y = IntVector('y_sym_',10)
z = IntVector('z_sym_',10)
c = x[0]+y[7] > z[3]
print(c)

print(pa.getPredStrucAndValueVec(c))

# multi deimensional arrays

graph_sym_ = [IntVector("graph_sym_"+str(i)+"_", 10) for i in range(0,10)]
c1 = graph_sym_[0][0] + graph_sym_[0][1] > graph_sym_[1][2]
print(c1)
print(pa.getPredStrucAndValueVec(c1))


print("======Test end======\n")

print("Test for induction variable prediction")

print("\nTest 1 : insertion sort")

A = [5,4,3,2,1,0]
var_i = []
var_j = []

for i in range(1, len(A)):
    x = A[i]
    j = i -1
    var_i.append("l1_s")
    var_j.append("l1_s")
    while(j >= 0 and A[j] > x):
        var_i.append(i)
        var_j.append(j)
        A[j+1] =  A[j]
        j = j - 1

    var_i.append("l1_e")
    var_j.append("l1_e")

    A[j+1] = x
    k = i

print("data : ")
print(mdl.removeTags(var_i))
modeli = mdl.sequenceModel(var_i, None)
resulti = modeli.predictSeq(10)
print("prediction : ")
print(resulti)

print("data : ")
print(mdl.removeTags(var_j))
modelj = mdl.sequenceModel(var_j, None)
resultj = modelj.predictSeq(10)
print("prediction : ")
print(resultj)


print("\nTest 2 : 3 nested loop")
# a 3 level nested loop
var_i = [] 
var_j = []
var_k = []

for i in range(0, 10):
    var_i.append("l1_s")
    var_j.append("l1_s")
    var_k.append("l1_s")
    for j in range(0,i):
        var_i.append("l2_s")
        var_j.append("l2_s")
        var_k.append("l2_s")
        for k in range(0,j):
            var_i.append(i)
            var_j.append(j)
            var_k.append(k)
        var_i.append("l2_e")
        var_j.append("l2_e")
        var_k.append("l2_e")
    var_i.append("l1_e")
    var_j.append("l1_e")
    var_k.append("l1_e")

print("data : ")
print(mdl.removeTags(var_i))
modeli = mdl.sequenceModel(var_i, None)
resulti = modeli.predictSeq(10)
print("prediction : ")
print(resulti)

print("data : ")
print(mdl.removeTags(var_j))
modelj = mdl.sequenceModel(var_j, None)
resultj = modelj.predictSeq(10)
print("prediction : ")
print(resultj)

print("data : ")
print(mdl.removeTags(var_k))
modelk = mdl.sequenceModel(var_k, None)
resultk = modelk.predictSeq(10)
print("prediction : ")
print(resultk)


print("======Test end======\n")