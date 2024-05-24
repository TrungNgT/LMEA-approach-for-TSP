n = 14      #number of cities
N = 16      #population / top_N
G = 250     # number of generations

class Point:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x={self.x}, y={self.y})"
    
p0 = Point(-1, -1)
p1 = Point(16.47, 96.10)
p2 = Point(16.47, 94.44) 
p3 = Point(20.09, 92.54) 
p4 = Point(22.39, 93.37) 
p5 = Point(25.23, 97.24) 
p6 = Point(22.00, 96.05)
p7 = Point(20.47, 97.02) 
p8 = Point(17.20, 96.29) 
p9 = Point(16.30, 97.38) 
p10 = Point(14.05, 98.12) 
p11 = Point(16.53, 97.38)
p12 = Point(21.52, 95.59) 
p13 = Point(19.41, 97.13)
p14 = Point(20.09, 94.55)


graph = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14]

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


