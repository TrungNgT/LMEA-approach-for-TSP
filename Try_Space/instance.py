n = 14      #number of cities
N = 40      #population 
G = 100     #number of generations

check_var = 0       # variable for checking local stuck


demension_index = 3
start_index = 8
graph = []

class Point:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x={self.x}, y={self.y})"
    
graph.append(Point(-1, -1))

with open('input.txt', 'r') as file:
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

import math

def distance(A: Point, B: Point):
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)


#print(graph[6].x)

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




