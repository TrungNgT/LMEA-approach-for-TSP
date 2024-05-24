from instance import *
import math
import random

def distance(A: Point, B: Point):
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

# hàm này để đưa cái đồ thị về liệt kê các điểm bằng string, ghép vào cái description.
def list2str() :
    global graph
    global n

    out_str = ''
    for index in range(1, n+1) :
        out_str += (str(index) + ' (' + str(graph[index].x) + ', ' + str(graph[index].y) + ')')
        if index != n :
            out_str += ', '

    return out_str

#print(list2str())

# hàm này để dịch 1 cái trace được sinh ra từ LLM (ở dạng string) sang list int (thành 1 cái permutation các chỉ số của điểm trong đồ thị)
def traceStr2list (trace: str) :
    trace = trace.translate({ord('{'):None, ord('}'):None, ord(';'):',', ord('['):None, ord(']'):None})
    L = trace.split(", ")
    for index in range(len(L)):
        L[index] = int(L[index])

    return L 

#print(traceStr2list("{1, 3, 5, 4, 6, 9, 7 "))

# hàm này để tính chi phí đi với mỗi hoán vị được sinh ra. (Bài TSP)
def objective_TSP(permutation: list) :                      # using the L above as the parameter.
    evaluation = 0.0
    x = y = 0
    for ind in range(len(permutation) - 1) :
        x = permutation[ind]
        y = permutation[ind+1]
        evaluation += distance(graph[x], graph[y])
        
    startPoint = permutation[0]
    lastPoint = permutation[-1]
    evaluation += distance(graph[lastPoint], graph[startPoint])

    return evaluation

#print(objective_TSP([1, 2, 3]))

# hàm này tính chi phí bài TRP
def objective_TRP(permutation: list) :
    global N
    evaluation = 0.0
    x = y = 0
    for ind in range(len(permutation) - 1) :
        x = permutation[ind]
        y = permutation[ind+1]
        evaluation += (N-1-ind) * distance(graph[x], graph[y])
    
    return evaluation

#cut cái response ở dạng string ra để lấy thông tin
def cut2parents(llmResponse: str) :
    firstPar = llmResponse[(llmResponse.find("<selection>") + 11):]
    goalPar = firstPar[:firstPar.find("</selection>")]

    return traceStr2list(goalPar)

#cut cái response ở dạng string ra để lấy thông tin
def cutGenTrace(llmResponse: str):
    firstPar = llmResponse[(llmResponse.find("<res>") + 5):]
    goalPar = firstPar[:firstPar.find("</res>")]

    return traceStr2list(goalPar)


#print(cut2tracelist("abcdef db <selection>{1, 3, 5, 4, 6, 9, 7 }</selection> See you tomorrow."))

#generate first population, n: number of city, N: number of individuals in one generation ---- write with chatGPT
def randomFirstN(n: int, N: int):
    listFirstN = []

    while(len(listFirstN) < N) :
        permutation =  list(random.sample(range(1, n + 1), n))
        indiv = Individual(permutation, objective_TSP(permutation))
        listFirstN.append(indiv)

    listFirstN.sort(reverse=True, key=compIndiv)

    return listFirstN

#print(randomFirstN(14, 4))


# step 6 in the paper's paradism
def updatePool(pool: list, newgenN: list, N: int):

    for indiv in newgenN:
        pool.append(indiv)
    
    pool.sort(reverse=True, key=compIndiv)
    L = len(pool)

    return pool[(L-N):]

'''
listA = randomFirstN(14, 4)
listB = randomFirstN(14, 4)
print(listA)
print(listB)
print(updatePool(listA, listB, 4))
'''
# hàm này để đưa các cá thể mẫu (trong pool đang là list các cá thể thuộc lớp Individual) thành xâu liệt kê để ghép vào phần thứ 2 của prompt
def pool2examples(pool: list) :
    outstr = ''
    for index in range(4) :
        outstr += ( str(pool[index].trace) + ' ' + 'length = ' + str(pool[index].length))
        if index != N-1 :
            outstr += '\n'
    return outstr
'''
listA = randomFirstN(14, 4)
print(pool2examples(listA))
'''