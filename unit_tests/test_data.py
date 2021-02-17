import os
import sys
import matplotlib.pyplot as plt

var_i = []
var_j = []
var_k = []

for i in range(0, 10):
    for j in range(0,i):
        for k in range(0,j):
            var_i.append(i)
            var_j.append(j)
            var_k.append(k)

plt.scatter([i for i in range(0,len(var_i))], var_i)
plt.grid()
plt.show()
plt.scatter([i for i in range(0,len(var_j))], var_j)
plt.grid()
plt.show()
plt.scatter([i for i in range(0,len(var_k))], var_k)
plt.grid()
plt.show()

