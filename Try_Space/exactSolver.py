from support import distance
from instance import *

def find_min() :
    global n
    global graph

    min_dis = 999999999.999999

    for i in range (1, n+1):
        for j in range (1, n+1):
            if (i != j) :
                min_dis = min(min_dis, distance(graph[i], graph[j]))
                
    return min_dis

#print(find_min())

solution = [0]*(n+5)

visited = [False]*(n+5)

optimal = 999999999.999999

current_eval = 0

min_dis = find_min()

edge_matr = []


for i in range (1, n+1) :
    row = []
    for j in range (1, n+1) :
        row.append(distance(graph[i], graph[j]))
    edge_matr.append(row)


def Try(k: int):

    global n, edge_matr, solution, optimal, current_eval, min_dis, visited

    for u in range (1, n+1) :
        if not visited[u] :
            visited[u] = True
            solution[k] = u
            if k > 1:
                current_eval += edge_matr[solution[k-1]-1][u-1]

            if k == n:
                optimal = min(optimal, current_eval + edge_matr[u-1][solution[1]-1])
                return

            else :
                if (current_eval + (n-k+1)*min_dis <= optimal) :
                    Try(k+1)


            if k > 1:
                current_eval -= edge_matr[solution[k-1]-1][u-1]
            solution[k] = 0
            visited[u] = False


Try(1)
print(optimal)

def print_all_edge() :
    global n
    for i in range(1, n+1) :
        for j in range(1, n+1):
            print(distance(graph[i], graph[j]), end=' ')
        print('\n')

#print_all_edge()