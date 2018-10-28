import sys

def dijkstra(array1d, src, V):

    int_max =  2147483647
    # empty 2d array
    graph = [[0 for i in range(0,10)] for j in range(0,10)]

    count = 0

    for i in range(0,V):
        for j in range(i,V):
            if(i==j):
                graph[i][j] = 0
                continue
            graph[i][j] = array1d[count]
            graph[j][i] = array1d[count]

            count+=1

    dist = [int_max for i in range(0,V)]
    spt_set = [False for i in range(0,V)]

    dist[src] = 0

    dumpGraph(graph,V)

    # iterate over V-1 vertices
    for i in range(0, V-1):
        # find min distance vertice
        u = 0
        min_val = int_max
        for j in range(0,V):
            if(spt_set[j] == False and dist[j]<=min_val):
                min_val = dist[j]
                u = j

        # mark this as visited
        spt_set[u] = True 

        # update the adjacent vertices
        for v in range(0,V):
            if((spt_set[v]==False) and (graph[u][v] > 0) and (dist[u]!=int_max) and (dist[u] + graph[u][v] < dist[v])):
                dist[v] = dist[u]+graph[u][v]



    printSolution(dist, V)


def printSolution(dist, V):

    for i in range(0, V):
        print("Vertex : "+str(i)+" Distance : "+str(dist[i]))

def dumpGraph(graph, V):

    for i in range(0,V):
        print(graph[i][0:V])



array1d = [4, 0, 0, 0, 0, 0, 8, 0,\
            8, 0, 0, 0, 0, 11, 0,\
            7, 0, 4, 0, 0, 2,\
            9, 14, 0, 0, 0,\
            10, 0, 0, 0,\
            2, 0, 0,\
            1, 6,\
            7] 
src = 0

dijkstra(array1d, src, 9)
