# %% [markdown]
# 1. Các thông số để lựa chọn với bộ dữ liệu
# 

# %%
n = 15      #number of cities
N = 16      #population 
G = 50     #number of generations

check_var = 0       # variable for checking local stuck

# %%
demension_index = 2
start_index = 5
graph = []

# %% [markdown]
# 2. Các định nghĩa lớp Điểm (Point) và Cá thể (Individual)

# %%
class Point:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x={self.x}, y={self.y})"
    
graph.append(Point(-1, -1))

# %%
class Individual:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, trace, length):
        self.trace = trace
        self.length = length

    def __repr__(self) -> str:
        return f"{type(self).__name__}(trace={self.trace}, length={self.length})"
    
def compIndiv(indiv: Individual) :
    return indiv.length

# %% [markdown]
# 3. Bắt đầu đọc từ file dữ liệu .txt để đưa ra danh sách (graph) các điểm

# %%
with open('C:/Users/MSI/Project2_practices/dataset/rue_15_3.tsp', 'r') as file:
    lines = file.readlines()

    demension_line = lines[demension_index]
    n = int(demension_line[demension_line.find(' '):])

    for idx_line in range(start_index, start_index+n):

        cur_line = lines[idx_line]
        component = cur_line.split(' ')
        
        tt = 0
        x = 0
        y = 0

        for c in component:
            try:
                if tt == 0 and c != '':
                    tt = 1
                else:
                    if tt == 1:
                        x = float(c)
                        tt = 2
                    else:
                        if tt == 2:
                            y = float(c)
                            break
            except:
                continue

        point_idx = Point(x, y)
        graph.append(point_idx)

        del cur_line

# %% [markdown]
# 4. - Hàm tính khoảng cách theo tọa độ Euclid

# %%
import math

def distance(A: Point, B: Point):
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

# %% [markdown]
# 4. - Hàm tính khoảng cách trong trường hợp điểm được cho dữ liệu kinh độ vĩ độ

# %%
import math

PI = 3.141592

def GeoDistance(A: Point, B: Point):
    # first, change degree&minute information to latitude and longtitude in radians
    deg = round(A.x)
    min = A.x - deg
    latitude_A = PI * (deg + 5.0 * min / 3.0) / 180.0
    deg = round(A.y)
    min = A.y - deg
    longtitude_A = PI * (deg + 5.0 * min / 3.0) / 180.0

    deg = round(B.x)
    min = B.x - deg
    latitude_B = PI * (deg + 5.0 * min / 3.0) / 180.0
    deg = round(B.y)
    min = B.y - deg
    longtitude_B = PI * (deg + 5.0 * min / 3.0) / 180.0

    #compute the distance in kilometers
    RRR = 6378.388                      #Radian of Earth
    q1 = math.cos(longtitude_A - longtitude_B)
    q2 = math.cos(latitude_A - latitude_B)
    q3 = math.cos(latitude_A + latitude_B)

    dist = int(RRR * math.acos(0.5 * ((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0)

    return dist


# %% [markdown]
# 5. Biểu diễn ma trận cạnh kề, chú ý lựa chọn hàm tính khoảng cách phù hợp với bộ dữ liệu

# %%
ed_graph = []

for i in range(n+1):
    sub_grp = []

    for j in range(n+1):
        sub_grp.append(distance(graph[i], graph[j]))
    ed_graph.append(sub_grp)
# %% [markdown]
# # Test space
# 

# %%
#print(len(ed_graph))


