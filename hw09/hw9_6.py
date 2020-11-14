from z3 import *

CPTs = [
    ["A", [[[], ["A", "T"], 0.8], [[], ["A", "F"], 0.2]]],
    ["B", [[[], ["B", "T"], 0.7], [[], ["B", "F"], 0.3]]],
    ["D", [[[], ["D", "T"], 0.1], [[], ["D", "F"], 0.9]]],
    ["C", [[[["A", "F"], ["B", "F"]], ["C", "F"], 0.9],
           [[["A", "F"], ["B", "F"]], ["C", "T"], 0.1],
           [[["A", "F"], ["B", "T"]], ["C", "F"], 0.2],
           [[["A", "F"], ["B", "T"]], ["C", "T"], 0.8],
           [[["A", "T"], ["B", "F"]], ["C", "F"], 0.3],
           [[["A", "T"], ["B", "F"]], ["C", "T"], 0.7],
           [[["A", "T"], ["B", "T"]], ["C", "F"], 0.4],
           [[["A", "T"], ["B", "T"]], ["C", "T"], 0.6]]],
    ["E", [[[["C", "F"], ["D", "F"]], ["E", "F"], 0.1],
           [[["C", "F"], ["D", "F"]], ["E", "T"], 0.9],
           [[["C", "F"], ["D", "T"]], ["E", "F"], 0.2],
           [[["C", "F"], ["D", "T"]], ["E", "T"], 0.8],
           [[["C", "T"], ["D", "F"]], ["E", "F"], 0.7],
           [[["C", "T"], ["D", "F"]], ["E", "T"], 0.3],
           [[["C", "T"], ["D", "T"]], ["E", "F"], 0.4],
           [[["C", "T"], ["D", "T"]], ["E", "T"], 0.6]]]
]
Os = [["A", "T"]]
Vs = ["E"]

dependencies = {}
res = {}
marginal = {}


def recursive(var):
    if var in marginal.keys():
        return marginal[var]
    triplets = dependencies[var]
    prob1 = 0
    prob0 = 0
    for triplet in triplets:
        if len(triplet[0]) == 0:
            if triplet[1][1] == "T":
                prob1 = triplet[2] * 100
            else:
                prob0 = triplet[2] * 100
        else:
            var_prob = triplet[2] * 100
            for condition in triplet[0]:
                if condition[0] in res.keys():
                    if condition[1] == "T":
                        var_prob *= res[condition[0]]
                    else:
                        var_prob *= (1 - res[condition[0]])
                else:
                    [dependent_t, dependent_f] = recursive(condition[0])
                    if condition[1] == "T":
                        var_prob *= dependent_t
                    else:
                        var_prob *= dependent_f
            if triplet[1][1] == "T":
                prob1 += var_prob
            else:
                prob0 += var_prob
    marginal[var] = [prob1, prob0]
    return [prob1, prob0]


def MAP(CPTs, Os, Vs):
    for cpt in CPTs:
        dependencies[cpt[0]] = cpt[1]

    vars1 = []
    for pair in Os:
        vars1.append(pair[0])
        if pair[1] == "T":
            res[pair[0]] = 1
        else:
            res[pair[0]] = 0

    obj_func = 1.0
    s = Optimize()

    for var in Vs:
        res[var] = Int(var)
        [t_prob, f_prob] = recursive(var)
        obj_func *= (Int(var) * t_prob + (1 - Int(var)) * f_prob)
        s.add(And(Int(var) >= 0, Int(var) <= 1))

    s.maximize(obj_func)
    if s.check() == sat:
        m = s.model()
        results = []
        for var in m:
            if m[var] == 1:
                results.append([var, "T"])
            else:
                results.append([var, "F"])
        print(results)
    else:
        print("false")


MAP(CPTs, Os, Vs)

