from z3 import *
import sys
import ast

input = sys.argv[1]
with open(input, 'r') as f:
    line1 = f.readline()
    weight = ast.literal_eval(line1)
    line2 = f.readline()
    capacity = ast.literal_eval(line2)

obj = -1
for i, list in enumerate(capacity):
    for j, c in enumerate(list):
        if j >= i and c > 0:
            temp = c * (Int('v_%s' % (i+1)) * Int('-v_%s' % (j+1)) + Int('-v_%s' % (i+1)) * Int('v_%s' % (j+1)))
            if obj == -1:
                obj = temp
            else:
                obj += temp

constraints = []
for i, v in enumerate(weight):
    constraint1 = Or(Int('v_' + str(i+1)) == 1, Int('v_' + str(i+1)) == 0)
    constraint2 = Or(Int('-v_' + str(i+1)) == 1, Int('-v_' + str(i+1)) == 0)
    constraint3 = Int('v_' + str(i+1)) + Int('-v_' + str(i+1)) == 1
    constraints.append(constraint1)
    constraints.append(constraint2)
    constraints.append(constraint3)


s = Optimize()
s.add(constraints)
s.maximize(obj)
if s.check() == unsat:
    print('false')
else:
    m = s.model()
    sorted_model = sorted([(d, m[d]) for d in m if '-' not in str(d)], key=lambda x: str(x))
    print(sorted_model)
    print(m.evaluate(obj))
