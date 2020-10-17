from z3 import *
s = Solver()

in_a0, out_a0, out_a1, out_a2, in_b0, out_b0 = Ints('in_a0 out_a0 out_a1 out_a2 in_b0 out_b0')

phi_a = And ( (out_a0 == in_a0), out_a1 == (out_a0 * in_a0), out_a2 == (out_a1 * in_a0) )
phi_b = out_b0 == (in_b0 * in_b0) * in_b0

phi = Implies (And (in_a0 == in_b0, phi_a, phi_b), out_b0 == out_a2)

s.add(Not(phi))

s.check()