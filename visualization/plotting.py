import matplotlib.pyplot as plt

file = open(r"new_approach/res1.txt")

line = file.readlines()

gen_axis = []

best_gap_axis = []

optimal_sol = 3323

for l in line:
    '''
    if l[4] == 'l':
        gen_axis.append(int(l[30:(l.find(':'))]))
        
    if l[0] == 'b':
        best_sol = float(l[(l.find(':')+2):])
        best_gap_axis.append((best_sol-optimal_sol)/optimal_sol*100)

    '''
    if l[0] == 'E':
        gen_axis.append(int(l[15:(l.find(','))]))
        best_sol = float(l[(l.find('is:')+3):])
        best_gap_axis.append((best_sol-optimal_sol)/optimal_sol*100)

print(len(gen_axis), len(best_gap_axis))

plt.plot(gen_axis, best_gap_axis)

plt.show()
