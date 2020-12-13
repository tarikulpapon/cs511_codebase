
# To run: python hw12_6.py n
# example
# python hw12_6.py 4
# python hw12_6.py 6
# python hw12_6.py 8

from z3 import *
import sys, random, math

n = int(sys.argv[1])

Q = [[Bool("Q" + str(i+1) + "," + str(j+1)) for j in range(n)] for i in range(n)]
R = [[Bool("R" + str(i+1) + "," + str(j+1)) for j in range(n)] for i in range(n)]

s = Solver()

def genRand(x, n):
    out = list(range(n))
    for j in range(x):
        i = random.randrange(j, n)
        temp = out[j]
        out[j] = out[i]
        out[i] = temp
    return out[:x], out[x:]

I, r = genRand(int(math.ceil(n/3.0)),n)

phi_1 = And([Or([Q[i][j] for j in range(n)]) for i in I])
phi_2 = And([Or([R[i][j] for j in range(n)]) for i in r])
phi_3 = And([And([Implies(Q[i][j], Not(R[i][j])) for j in range(n)]) for i in range(n)])
phi_4 = And([And([Implies(Q[i][j], And([And(Not(Q[i][l]), Not(R[i][l])) for l in [x for x in range(n) if x != j]])) for j in range(n)]) for i in range(n)])
phi_5 = And([And([Implies(Q[i][j], And([And(Not(Q[k][j]), Not(R[k][j])) for k in [x for x in range(n) if x != i]])) for j in range(n)]) for i in range(n)])
phi_6 = And([And([Implies(R[i][j], And([And(Not(Q[i][l]), Not(R[i][l])) for l in [x for x in range(n) if x != j]])) for j in range(n)]) for i in range(n)])
phi_7 = And([And([Implies(R[i][j], And([And(Not(Q[k][j]), Not(R[k][j])) for k in [x for x in range(n) if x != i]])) for j in range(n)]) for i in range(n)])
phi_8 = And([And([And([And([If(x - y == i - j and x != i, Implies(Q[i][j], And(Not(Q[x][y]), Not(R[x][y]))), True) for y in range(n)]) for x in range(n)]) for j in range(n)]) for i in range(n)])
phi_9 = And([And([And([And([If(x + y == i + j and x != i, Implies(Q[i][j], And(Not(Q[x][y]), Not(R[x][y]))), True) for y in range(n)]) for x in range(n)]) for j in range(n)]) for i in range(n)])

constraints = [phi_1, phi_2, phi_3, phi_4, phi_5, phi_6, phi_7, phi_8, phi_9]
test = constraints.pop()

for i in range(9):
	s = Solver()
	
	for c in constraints:
		s.add(c)

	s.add(Not(test))

	if s.check() == unsat:
		print "Constraint " + str(i + 1) + " can be omitted"
	
	constraints.insert(0, test)
	test = constraints.pop()
