import sys
import os
import math

graph_output_file = open(str(sys.argv[1]), "r")
lines = graph_output_file.readlines()

cnt = 0
index_val_list = []

for l in lines:
    if("graph" in l):
        words = l.split("graph")[1].lstrip(
            "_").split("=")[0].rstrip(" ").split("_")
        indices = []
        for w in words[:-1]:

            indices.append(int(w))

        value = int(l.split("=")[1].lstrip("_"))
        index_val_list.append([indices, value])
        cnt += 1

print(index_val_list)

size_of_graph = int(math.sqrt(cnt))
graph = [[0 for j in range(0, size_of_graph)] for i in range(0, size_of_graph)]

ptr = 0
for index in index_val_list:
    x_cordinate = index[0][0]
    y_cordinate = index[0][1]

    if(x_cordinate == size_of_graph):
        x_cordinate = 0

    graph[x_cordinate][y_cordinate] = index[1]


for row in graph:
    print(row)
