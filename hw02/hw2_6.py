from z3 import *

# declaring propositional variables
p1, p2, p3, p4 = Bools('p1 p2 p3 p4')

phi = And( Or(Not(p1), Not(p2), Not(p3), p4), Or(Not(p1), Not(p2), p3, Not(p4)), Or(Not(p1), p2, Not(p3), Not(p4)), Or(Not(p1), p2, p3, p4), Or(p1, Not(p2), Not(p3), Not(p4)), Or(p1, Not(p2), p3, p4), Or(p1, p2, Not(p3), p4), Or(p1, p2, p3, Not(p4)))

psi = Or( And(p1,p2,p3,p4), And(p1,p2,Not(p3),Not(p4)), And(p1,Not(p2),p3,Not(p4)), And(p1,Not(p2),Not(p3),p4), And(Not(p1),p2,p3,Not(p4)), And(Not(p1),p2,Not(p3),p4), And(Not(p1),Not(p2),p3,p4), And(Not(p1),Not(p2),Not(p3),Not(p4)))

def bicon(p1, p2):
	return And(Implies(p1, p2), Implies(p2, p1))

theta = bicon(bicon(bicon(p1, p2), p3), p4)

s = Solver()

s.add(phi == psi)
s.add(psi == theta)

print s.check()
