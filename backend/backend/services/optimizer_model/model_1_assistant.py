import time
import docplex.mp.model as cpx
import pandas as pd
import math
import pprint
import itertools
import cplex
import numpy as np
import random
import json

#Reading JSON

from itertools import chain, combinations,product,permutations
from scipy.stats import truncnorm
import gc
import copy
start_time = time.time()

rnd = np.random
rnd.seed(320)


def CreateModel(PlanID):
    # %% Read Json file
    f = open('ProcessGraph1_precedence_fuzzy values.json')
    dataInfra = json.load(f)
    AssemblyPlan = dataInfra['AssemblyPlans'][PlanID - 1]

    # %% Get the information for Tasks
    TaskProcessTime = []
    TaskCost = []
    TaskQulity = []
    ListofTasks = list(range(len(AssemblyPlan['ListOfTaskIDs'])))
    nTask = len(ListofTasks)
    # nStation = 0
    # nEquipment = 1  # Index 0 of equipment means using no equipment
    equipList = ['None']
    stationList = []
    for _ in range(len(dataInfra['Node'])):
        if dataInfra['Node'][_]['Tasktype'] != 'Feeding':
            myString = dataInfra['Node'][_]['PRNodeName'].split('+')
            if len(myString) > 2 and myString[2] not in equipList:
                equipList.append(myString[2])
                # nEquipment += 1
            if myString[1] not in stationList:
                stationList.append(myString[1])
                # nStation += 1
    nStation = len(stationList)
    nEquipment = len(equipList)
    # %% Get the information of Equipment and Worker
    Process = np.ones((nTask, nStation, nEquipment)) * 100000000
    Quality = np.zeros((nTask, nStation, nEquipment))
    Cost = np.ones((nTask, nStation, nEquipment)) * 1000000000
    ListofEquipment = []
    ListofWorkers = []
    for _ in range(len(dataInfra['Node'])):
        if dataInfra['Node'][_]['Tasktype'] != 'Feeding':
            t = int(dataInfra['Node'][_]['TaskID'])
            myString = dataInfra['Node'][_]['PRNodeName'].split('+')
            if len(myString) == 2:
                myString.append('None')
            for i in range(nStation):
                for j in range(nEquipment):
                    # if len(myString) > 2:
                    if stationList[i] == myString[1] and equipList[j] == myString[2]:
                        Process[t][i][j] = dataInfra['Node'][_]['ProcessTime']
                        Cost[t][i][j] = dataInfra['Node'][_]['Costs']
                        Quality[t][i][j] = dataInfra['Node'][_]['MonitoringEfficiency']
                    # else:
                    #     if stationList[i] == myString[1]:
                    #         Process[t][i][0] = dataInfra['Node'][_]['ProcessTime']
                    #         Cost[t][i][0] = dataInfra['Node'][_]['Costs']
                    #         Quality[t][i][0] = dataInfra['Node'][_]['MonitoringEfficiency']

    print(equipList)

    return Process, Quality, Cost


# ProcessDic, CostDic, QualityDic = CreateModel(4)
PlanID = 2

ptt = CreateModel(PlanID)
pt = ptt[0]

I = len(pt)
R = len(pt[0])
T = len(pt[0][0])

for i in range(I):
    for r in range(R):
        for t in range(T):
            if pt[i][r][t] == 1000:
                pt[i][r][t] = 1000000

h = []
for i in range(I):
    h.append([])
    for r in range(R):
        h[i].append([])
        for t in range(T):
            #            if pt[i][r][t] != 1000000:
            #                h[i][r].append(pt[i][r][t] - ((pt[i][r][t]) * 0.3) )
            #            if pt[i][r][t] == 1000000:
            h[i][r].append(pt[i][r][t])

hh = []
for i in range(I):
    hh.append([])
    for r in range(R):
        hh[i].append([])
        for t in range(T):
            if pt[i][r][t] != 1000000:
                hh[i][r].append(pt[i][r][t] + ((pt[i][r][t]) * 0.3))
            if pt[i][r][t] == 1000000:
                hh[i][r].append(pt[i][r][t])

d = []
for i in range(I):
    d.append([])
    for r in range(R):
        d[i].append([])
        for t in range(T):
            d[i][r].append(hh[i][r][t] - h[i][r][t])
#            if pt[i][r][t] != 1000000:
#                d[i][r].append(hh[i][r][t]-h[i][r][t])
#            if pt[i][r][t] == 1000000:
#                d[i][r].append(hh[i][r][t]-h[i][r][t])


# process quality upper/lower bounds
qualityy = CreateModel(PlanID)
quality = qualityy[1]

for i in range(I):
    for r in range(R):
        for t in range(T):
            if r == 2 or r == 3:
                if quality[i][r][t] <= 0.5 and quality[i][r][t] != 0:
                    quality[i][r][t] = random.uniform(0.73, 0.78)

alpha = []
for i in range(I):
    alpha.append([])
    for r in range(R):
        alpha[i].append([])
        for t in range(T):
            #            if quality[i][r][t] != 0:
            #                alpha[i][r].append(quality[i][r][t] - ((quality[i][r][t]) * 0.15) )
            #            if quality[i][r][t] == 0:
            alpha[i][r].append(quality[i][r][t])

alphaalpha = []
for i in range(I):
    alphaalpha.append([])
    for r in range(R):
        alphaalpha[i].append([])
        for t in range(T):
            if quality[i][r][t] != 0:
                alphaalpha[i][r].append(quality[i][r][t] - ((quality[i][r][t]) * 0.1))
            if quality[i][r][t] == 0:
                alphaalpha[i][r].append(quality[i][r][t])

f = []
for i in range(I):
    f.append([])
    for r in range(R):
        f[i].append([])
        for t in range(T):
            f[i][r].append(alpha[i][r][t] - alphaalpha[i][r][t])

# cost
# process quality upper/lower bounds
costt = CreateModel(PlanID)
cost = qualityy[2]

ee = []
for r in range(R):
    ee.append([])
    for t in range(T):
        ee[r].append([])
        for i in range(I):
            ee[r][t].append(cost[i][r][t])

e = []
for r in range(R):
    e.append([])
    for t in range(T):
        B = 0
        for i in range(I):
            if ee[r][t][i] != 1000000000:
                B += ee[r][t][i]
        e[r].append(B / I)

for r in range(R):
    for t in range(T):
        if e[r][t] == 10000:
            e[r][t] = 10000000000000000000

# precedence relationships
prec = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13]]
# activation cost
a = [15000, 13000, 4000, 4000]

# Run the optimization model 1: Robust

# uncertain parameters
landa = 3
mu = 1

# precedence relationships
prec = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13]]
# activation cost
# a = [5000, 4000, 2000, 2000]


# N[t][r](i): is link with NN tasks
N = [[[0, 1], []], [[1], []], [[], [1, 2, 3]], [[], [2, 3]]]
# N = [[[0],[]],[[1],[]],[[],[1,2,3]],[[],[2,3]]]
# NN[i][r](t): is link with N tools
NN = [[[0], []], [[0, 1], [2]], [[], [2, 3]], [[], [2, 3]]]
# NN = [[[0],[]],[[1],[2]],[[],[2,3]],[[],[2,3]]]

A = [(i, r, t) for i in range(I) for r in range(R) for t in range(T)]
B = [(r, t) for r in range(R) for t in range(T)]
D = [(i) for i in range(I)]
E = [(r) for r in range(R)]
F = [(i, r) for i in range(I) for r in range(R)]

# A = [(i,r,t) for i in I for r in range(R) for t in T]
# B = [(r,t) for r in range(R) for t in T ]
# D = [(i) for i in I ]
# E = [(r) for r in range(R) ]


opt_model = cpx.Model('MIP Model')
opt_model.parameters.timelimit.set(1800)

x = opt_model.binary_var_dict(A, name="x")
y = opt_model.binary_var_dict(B, name="y")
z = opt_model.binary_var_dict(E, name="z")
q = opt_model.continuous_var_dict(D, name="q")
Q = opt_model.continuous_var(name="Q")
C = opt_model.continuous_var(name="C")

W = opt_model.continuous_var_dict(E, name="W")
Z = opt_model.continuous_var_dict(F, name="Z")
L = opt_model.continuous_var_dict(E, name="L")
V = opt_model.continuous_var_dict(F, name="V")

objective1 = (opt_model.sum(e[r][t] * y[r, t] for r in range(R) for t in range(T)) + opt_model.sum(
    a[r] * z[r] for r in range(R)))
# objective2 = opt_model(Q)
# objective3 = opt_model.add(C)

# Constraint for objective 1: reconfiguration cost
# opt_model.add_constraint(opt_model.sum(e[r][t]*y[r,t,m] for r in range(R) for t in range(T) for m in range(M)) <= 180)

# Constraint for objective 2: process quality
opt_model.add_constraint(Q >= 0.6)

# Constraint for objective 3: cycle time
opt_model.add_constraint(C <= 1050)

# for i in range(I):
#    opt_model.add_constraint(Q <= q[i] - opt_model.sum(mu*L[r] for r in range(R)) - opt_model.sum(V[i,r] for i in range(I) for r in range(R)))

for i in range(I):
    opt_model.add_constraint(Q <= opt_model.sum(quality[i][r][t] * x[i, r, t] for r in range(R) for t in range(T)))

# for i in range(I):
#    opt_model.add_constraint(q[i] == opt_model.sum(alpha[i][r][t]*y[r,t] for r in range(R) for t in range(T)))

# for i in range(I):
#    opt_model.add_constraint(q[i] == opt_model.sum(alpha[i][r][t]*x[i,r,t] for r in range(R) for t in range(T)))

for i in range(I):
    opt_model.add_constraint(opt_model.sum(x[i, r, t] for r in range(R) for t in range(T)) == 1)

for r in range(R):
    for t in range(T):
        opt_model.add_constraint(opt_model.sum(x[i, r, t] for i in range(I)) <= (I * y[r, t]))

for t in range(T):
    opt_model.add_constraint(opt_model.sum(y[r, t] for r in range(R)) <= 1)

for r in range(R):
    opt_model.add_constraint(opt_model.sum(y[r, t] for t in range(T)) <= (T * z[r]))

# modified cycle time constraints
for r in range(R):
    opt_model.add_constraint(
        opt_model.sum(x[i, r, t] * h[i][r][t] for t in range(T) for i in range(I)) + landa * W[r] + opt_model.sum(
            Z[i, r] for i in range(I)) <= C)

for i in prec:
    opt_model.add_constraint(opt_model.sum((r) * x[i[0], r, t] for r in range(R) for t in range(T)) <= opt_model.sum(
        (r) * x[i[1], r, t] for r in range(R) for t in range(T)))

# dual constraints
# process time
# for r in range(R):
#    opt_model.add_constraint( W[r] + opt_model.sum(Z[i,r] for i in range(I)) >= opt_model.sum(x[i,r,t]*d[i][r][t] for t in range(T) for i in range(I) ))
for r in range(R):
    for i in range(I):
        opt_model.add_constraint(W[r] + Z[i, r] >= opt_model.sum(x[i, r, t] * d[i][r][t] for t in range(T)))

    # process quality
# for r in range(R):
#    opt_model.add_constraint( L[r] + opt_model.sum(V[i,r] for i in range(I)) >= opt_model.sum(x[i,r,t]*f[i][r][t] for t in range(T) for i in range(I) ))
# for r in range(R):
#    for i in range(I):
#        opt_model.add_constraint( L[r] + V[i,r] >= opt_model.sum(x[i,r,t]*f[i][r][t] for t in range(T) ))

opt_model.minimize(objective1)
# opt_model.maximize(objective2)
# opt_model.minimize(objective3)
opt_model.solve(log_output=True)

obj_value = opt_model.objective_value
timer = opt_model.get_solve_details().time
print(obj_value)
print(timer)

print(time.time()-start_time)
