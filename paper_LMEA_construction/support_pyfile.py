# %%
from instance_pyfile import *
import random

# %% [markdown]
# File này gồm các hàm hỗ trợ cho các thao tác soạn prompt, tách kết quả từ câu trả lời của LLM và quản lý quần thể
# 

# %%
# hàm này để đưa đồ thị danh sách điểm về liệt kê các điểm bằng string, ghép vào description của promt.
def list2str() :
    global graph
    global n

    out_str = ''
    for index in range(1, n+1) :
        out_str += (str(index) + ' (' + str(graph[index].x) + ', ' + str(graph[index].y) + ')')
        if index != n :
            out_str += ', '

    return out_str


# %%
# hàm này để dịch 1 cái trace được sinh ra từ LLM (ở dạng string) sang list int (thành 1 cái permutation các chỉ số của điểm trong đồ thị)
def traceStr2list (trace: str) :
    global n
    trace = trace.translate({ord('{'):None, ord('}'):None, ord(';'):',', ord('['):None, ord(']'):None, ord('\n'):None, ord('.'): ', ', ord('*'):None})
    L = trace.split(", ")
    for index in range(len(L)):
        L[index] = int(L[index])

    return L[:n]

# %%
# hàm này để tính chi phí đi với mỗi hoán vị được sinh ra. (Bài TSP)
def objective_TSP(permutation: list) :                      # using the L above as the parameter.
    evaluation = 0.0
    x = y = 0
    for ind in range(len(permutation) - 1) :
        x = permutation[ind]
        y = permutation[ind+1]
        evaluation += ed_graph[x][y]
        
    evaluation += ed_graph[permutation[-1]][permutation[0]]

    return evaluation

# %%
# hàm này tính chi phí bài TRP
def objective_TRP(permutation: list) :
    global N
    evaluation = 0.0
    x = y = 0
    for ind in range(len(permutation) - 1) :
        x = permutation[ind]
        y = permutation[ind+1]
        evaluation += (N-1-ind) * ed_graph[x][y]
    
    return evaluation

# %%
#cut response ở dạng string ra để lấy thông tin các con mới sinh ra
def cutGenTrace(llmResponse: str):

    number = min(llmResponse.count("</res>"), llmResponse.count("<res>"))
    
    tempString = []
    listOffstr = []

    for inte in range(number) :
        tempString.append(str(inte))
        listOffstr.append(str(inte))
    try:
        tempString[0] = llmResponse[(llmResponse.find("<res>") + 5):]

    except:
        return listOffstr 
    
    for index in range(number) :
        tmp = tempString[index]
        listOffstr[index] = tmp[:tmp.find("</res>")]
        
        if index != number-1:
            tempString[index+1] = tmp[(tmp.find("<res>") + 5 ):]

    return listOffstr               #list of strings

# %%
#Khởi tạo quần thể ban đầu với N cá thể từ tập n điểm đã cho
def randomFirstN(n: int, N: int):
    listFirstN = []

    while(len(listFirstN) < N) :
        permutation =  list(random.sample(range(1, n + 1), n))
        indiv = Individual(permutation, objective_TSP(permutation))
        listFirstN.append(indiv)

    listFirstN.sort(reverse=True, key=compIndiv)

    return listFirstN

# %%
# Cập nhật quần thể sau mỗi thế hệ
# step 6 in the paper's paradism
def updatePool(pool: list, newgenN: list, N: int):                  #pool: list of current individuals, newGenN: list of string_offSrping

    # Using set to remain all the individuals are different from each others.

    cur_list = []

    for indiv in pool:
        cur_list.append(str(indiv.trace))
    
    print(f"The cur_0: {cur_list[0]}")
    print(f"On other hand, the new_0: {newgenN[0]}")
    
    cur_set = set(cur_list)
    new_set = set(newgenN)

    total_set = cur_set | new_set

    new_pool = transform(total_set)

    
    new_pool.sort(reverse=True, key=compIndiv)
    L = len(new_pool)

    print(f"The size of pool now is: {L}")

    out_pool = []
    if L >= N :
        out_pool = new_pool[(L-N):]
    else :
        out_pool = new_pool + new_pool[(N-L):]
        out_pool.sort(reverse=True, key=compIndiv)

    del new_pool
    del total_set
    del cur_set
    del new_set
    del cur_list

    return out_pool

# %%
# hàm này để đưa các cá thể mẫu (trong pool đang là list các cá thể thuộc lớp Individual) thành xâu liệt kê để ghép vào phần thứ 2 của prompt
def pool2examples(pool: list) :
    outstr = ''
    for index in range(N) :
        outstr += ( str(pool[index].trace) + ' ' + 'length = ' + str(pool[index].length))
        if index != N-1 :
            outstr += '\n'
    return outstr

# %%
# transform StringList offstring to IndividualList:

def transform(P_temp: list):
    P_sharp = []
    for per in P_temp:
        newOff = traceStr2list(per)
        newIndiv = Individual(newOff, objective_TSP(newOff))
        P_sharp.append(newIndiv)
    
    return P_sharp                  #list Individuals

def checkPermu(permuStr: str, n: int) : 
    try :            
        permu = traceStr2list(permuStr)

        if len(permu) != n:
            return False
    
        else: 
            for inte in range(1, n+1):
                if (inte in permu) == False:
                    return False
    except :
        return False
    return True

# %%
def check_stuck(best_cur: int, best_now: int, K: int) :

    global check_var

    if (best_now >= best_cur) :
        check_var += 1
        print(f"got stuck {check_var} time")
    else :
        check_var = 0
        print("got update!")
    
    if check_var%K == 0 and check_var > 0 :
        
        return True
    
    return False


