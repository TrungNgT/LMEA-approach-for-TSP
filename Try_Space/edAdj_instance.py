from instance import *

ed_graph = []

for i in range (n+1):
    sub_grp = []                                                
    for j in range (n+1):
        sub_grp.append(distance(graph[i], graph[j]))            
    ed_graph.append(sub_grp)


#print(graph)


#for i in range (n+1):
#    print(new_graph[i])
