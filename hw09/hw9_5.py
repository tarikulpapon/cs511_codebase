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
res = {}
s = Optimize()


def MPE(CPTs, Os):
    dependencies = {}
    for cpt in CPTs:
        dependencies[cpt[0]] = []
        triplet = cpt[1][0]
        for dependent in triplet[0]:
            dependencies[cpt[0]].append(dependent[0])

    for pair in Os:
        if pair[1] == "T":
            res[pair[0]] = 1
        else:
            res[pair[0]] = 0
    for var in dependencies:
        if var not in res.keys():
            res[var] = Int(var)
            s.add(And(Int(var) >= 0, Int(var) <= 1))

    obj = 1.0
    for cpt in CPTs:
        var = cpt[0]
        prob1 = 0
        prob2 = 0
        if len(dependencies[var]) == 0:
            for triplet in cpt[1]:
                if triplet[1][1] == "T":
                    prob1 += (triplet[2] * 100 * res[var])
                else:
                    prob1 += (triplet[2] * 100 * (1-res[var]))
            obj *= prob1
        else:
            for triplet in cpt[1]:
                prob = 1
                for condition in triplet[0]:
                    if condition[1] == "T":
                        prob *= res[condition[0]]
                    else:
                        prob *= (1-res[condition[0]])
                if triplet[1][1] == "T":
                    prob *= (triplet[2] * 100) * res[var]
                else:
                    prob *= (triplet[2] * 100) * (1-res[var])
                prob2 += prob
            obj *= prob2

    s.maximize(obj)
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


MPE(CPTs, Os)
