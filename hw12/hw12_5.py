
# To run: python hw12_5.py n
# example
# python hw12_5.py 4
# python hw12_5.py 6
# python hw12_5.py 8

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


s.add(And([Or([Q[i][j] for j in range(n)]) for i in I]))
s.add(And([Or([R[i][j] for j in range(n)]) for i in r]))
s.add(And([And([Implies(Q[i][j], Not(R[i][j])) for j in range(n)]) for i in range(n)]))
s.add(And([And([Implies(Q[i][j], And([And(Not(Q[i][l]), Not(R[i][l])) for l in [x for x in range(n) if x != j]])) for j in range(n)]) for i in range(n)]))
s.add(And([And([Implies(Q[i][j], And([And(Not(Q[k][j]), Not(R[k][j])) for k in [x for x in range(n) if x != i]])) for j in range(n)]) for i in range(n)]))
s.add(And([And([Implies(R[i][j], And([And(Not(Q[i][l]), Not(R[i][l])) for l in [x for x in range(n) if x != j]])) for j in range(n)]) for i in range(n)]))
s.add(And([And([Implies(R[i][j], And([And(Not(Q[k][j]), Not(R[k][j])) for k in [x for x in range(n) if x != i]])) for j in range(n)]) for i in range(n)]))
s.add(And([And([And([And([If(x - y == i - j and x != i, Implies(Q[i][j], And(Not(Q[x][y]), Not(R[x][y]))), True) for y in range(n)]) for x in range(n)]) for j in range(n)]) for i in range(n)]))
s.add(And([And([And([And([If(x + y == i + j and x != i, Implies(Q[i][j], And(Not(Q[x][y]), Not(R[x][y]))), True) for y in range(n)]) for x in range(n)]) for j in range(n)]) for i in range(n)]))

if s.check() == unsat:
    print "unsat"

        
model = s.model()

for i in range(n):
    print "",
    for j in range(n):
        if is_true(model.evaluate(Q[i][j])):
            print "Q",
        elif is_true(model.evaluate(R[i][j])):
            print "R",
        else:
            print "-",
        if j != n - 1:
            print "\t",
    print ""