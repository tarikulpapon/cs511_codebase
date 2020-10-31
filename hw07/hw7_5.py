from z3 import *
import sys
import ast

input = sys.argv[1]
with open(input, 'r') as f:
    line = f.readline()
    L = ast.literal_eval(line)

array = []
array_n = []


obj = -1
for temp in L[0]:
    breakdown = temp[0]
    for vector in temp[1]:
        if vector[0] == 0:
            n = Int('x%s' % vector[1])
        else:
            n = Int('-x%s' % vector[1])
        if n not in array:
            array.append(n)
        if vector[1] not in array_n:
            array_n.append(vector[1])
        breakdown *= n
    if obj == -1:
        obj = breakdown
    else:
        obj += breakdown


constraints = []
for j in range(1, len(L)):
    constraint = -1
    for temp in L[j]:
        breakdown = temp[0]
        for vector in temp[1]:
            if vector[0] == 0:
                n = Int('x%s' % vector[1])
            else:
                n = Int('-x%s' % vector[1])
            if n not in array:
                array.append(n)
            if vector[1] not in array_n:
                array_n.append(vector[1])
            breakdown *= n
        if constraint == -1:
            constraint = breakdown
        else:
            constraint += breakdown
    constraints.append(constraint <= 0)


for i in array_n:
    var_constraint = Or(Int('x'+str(i)) == 1, Int('x'+str(i)) == 0)
    constraints.append(var_constraint)
    var_constraint = Or(Int('-x' + str(i)) == 1, Int('-x' + str(i)) == 0)
    constraints.append(var_constraint)
    var_constraint = Int('x'+str(i)) + Int('-x' + str(i)) == 1
    constraints.append(var_constraint)


s = Optimize()
s.add(constraints)
s.minimize(obj)
if s.check() == unsat:
    print('false')
else:
    print('true')
    m = s.model()
    sorted_model = sorted([(d, m[d]) for d in m], key=lambda x: str(x))
    print(sorted_model)