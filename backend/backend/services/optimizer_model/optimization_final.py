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
import copy

#Reading JSON


from itertools import chain, combinations,product,permutations

from scipy.stats import truncnorm 

import gc
import numpy as np
import copy
rnd = np.random
rnd.seed(320)
#from statistics import NormalDist
import json 

def Optimizer(file):
#%% States: For each item we have got a State
    def CreateModel(PlanID):
        #%% Read Json file
        # f = open('EFFRA_ProcessGraph1_precedence.json')
        dataInfra = file   
        AssemblyPlan = dataInfra['AssemblyPlans'][PlanID-1]
        
        #%% Get the information for Tasks
        TaskProcessTime = []
        TaskCost = []
        TaskQulity = []
        ListofTasks = list(range(len(AssemblyPlan['ListOfTaskIDs'])))
        nTask = len(ListofTasks)
        nStation = 0
        nEquipment = 1 # Index 0 of equipment means using no equipment
        equipList = ['None']
        stationList = []
        for _ in range(len(dataInfra['Node'])):
            if dataInfra['Node'][_]['Tasktype'] != 'Feeding' and dataInfra['Node'][_]['Tasktype'] != 'Transport':
                myString = dataInfra['Node'][_]['PRNodeName'].split('+')
                if len(myString)>2 and myString[2] not in equipList:
                    equipList.append(myString[2])
                    nEquipment+=1
                if myString[1] not in stationList:
                    stationList.append(myString[1])
                    nStation+=1
        #%% Get the information of Equipment and Worker
        Process = np.ones((nTask,nStation,nEquipment))*100000000
        Quality = np.zeros((nTask,nStation,nEquipment))
        Cost = np.ones((nTask,nStation,nEquipment))*1000000000
        ListofEquipment = []
        ListofWorkers = []
        for _ in range(len(dataInfra['Node'])):
            if dataInfra['Node'][_]['Tasktype'] != 'Feeding' and dataInfra['Node'][_]['Tasktype'] != 'Transport':
                t =  int(dataInfra['Node'][_]['TaskID'])
                myString = dataInfra['Node'][_]['PRNodeName'].split('+')
                for i in range(nStation):
                    for j in range(nEquipment):
                        if len(myString)>2:
                            if stationList[i] == myString[1] and equipList[j] == myString[2]:
                                Process[t][i][j] = dataInfra['Node'][_]['ProcessTime']
                                Cost[t][i][j] = dataInfra['Node'][_]['Costs']
                                Quality[t][i][j] = dataInfra['Node'][_]['MonitoringEfficiency']
                        else:
                            if stationList[i] == myString[1]:
                                Process[t][i][0] = dataInfra['Node'][_]['ProcessTime']
                                Cost[t][i][0] = dataInfra['Node'][_]['Costs']
                                Quality[t][i][0] = dataInfra['Node'][_]['MonitoringEfficiency']
                                
            
            
            
    
        print(equipList)
        print(stationList)

        return(Process,Quality,Cost)

    ProcessDic,CostDic,QualityDic = CreateModel(4)
    PlanID = 4


    #MOdfication of the input data (from JSON)

    #process time upper/lower bounds 
    ptt = CreateModel(PlanID)
    pt = ptt[0]

    I=len(pt)
    R=len(pt[1])
    T=len(pt[0][0])

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
                    hh[i][r].append(pt[i][r][t] + ((pt[i][r][t]) * 0.3) )
                if pt[i][r][t] == 1000000:
                    hh[i][r].append(pt[i][r][t])

    d=[]
    for i in range(I):
        d.append([])
        for r in range(R):
            d[i].append([])
            for t in range(T):
                d[i][r].append(hh[i][r][t]-h[i][r][t])
    #            if pt[i][r][t] != 1000000:
    #                d[i][r].append(hh[i][r][t]-h[i][r][t])
    #            if pt[i][r][t] == 1000000:
    #                d[i][r].append(hh[i][r][t]-h[i][r][t])
                
                
    #process quality upper/lower bounds            
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
                    alphaalpha[i][r].append(quality[i][r][t] - ((quality[i][r][t]) * 0.1) )
                if quality[i][r][t] == 0:
                    alphaalpha[i][r].append(quality[i][r][t])
                
    f=[]
    for i in range(I):
        f.append([])
        for r in range(R):
            f[i].append([])
            for t in range(T):
                f[i][r].append(alpha[i][r][t]-alphaalpha[i][r][t])
                
                
    #cost
    #process quality upper/lower bounds            
    costt = CreateModel(PlanID)
    cost = qualityy[2]

                
    ee=[]
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
            B=0
            for i in range(I):
                if ee[r][t][i] != 1000000000:
                    B += ee[r][t][i]
            e[r].append(B/I) 

    for r in range(R):
        for t in range(T):
            if e[r][t] == 10000:
                e[r][t] = 10000000000000000000

                
                
    #precedence relationships
    prec = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,12],[12,13]]
    #activation cost
    a = [15000, 13000, 4000, 4000]


    # Run the optimization model 1: Robust

    #uncertain parameters
    landa = 2
    mu = 2

    #precedence relationships
    prec = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,12],[12,13]]
    #activation cost
    #a = [5000, 4000, 2000, 2000]


    #N[t][r](i): is link with NN tasks
    N = [[[0,1],[]],[[1],[]],[[],[1,2,3]],[[],[2,3]]]
    #N = [[[0],[]],[[1],[]],[[],[1,2,3]],[[],[2,3]]]
    #NN[i][r](t): is link with N tools
    NN = [[[0],[]],[[0,1],[2]],[[],[2,3]],[[],[2,3]]]
    #NN = [[[0],[]],[[1],[2]],[[],[2,3]],[[],[2,3]]]

                
    landa = 2
    A = [(i,r,t) for i in range(I) for r in range(R) for t in range(T)]
    B = [(r,t) for r in range(R) for t in range(T) ]
    D = [(i) for i in range(I) ]
    E = [(r) for r in range(R) ]
    F = [(i,r) for i in range(I) for r in range(R)]

    #A = [(i,r,t) for i in I for r in range(R) for t in T]
    #B = [(r,t) for r in range(R) for t in T ]
    #D = [(i) for i in I ]
    #E = [(r) for r in range(R) ]


    opt_model = cpx.Model('MIP Model')
    opt_model.parameters.timelimit.set(1800)

    x  = opt_model.binary_var_dict(A, name="x") 
    y  = opt_model.binary_var_dict(B, name="y")  
    z  = opt_model.binary_var_dict(E, name="z") 
    q  = opt_model.continuous_var_dict(D, name="q")  
    Q  = opt_model.continuous_var(name="Q") 
    C = opt_model.continuous_var(name="C") 

    W = opt_model.continuous_var_dict(E, name="W")
    Z = opt_model.continuous_var_dict(F, name="Z")
    L = opt_model.continuous_var_dict(E, name="L")
    V = opt_model.continuous_var_dict(F, name="V")



    objective1 = (opt_model.sum(e[r][t]*y[r,t] for r in range(R) for t in range(T)) + opt_model.sum(a[r]*z[r] for r in range(R) )) 
    #objective2 = Q
    #objective3 = C  

    #Constraint for objective 1: reconfiguration cost
    #opt_model.add_constraint((opt_model.sum(e[r][t]*y[r,t] for r in range(R) for t in range(T)) + opt_model.sum(a[r]*z[r] for r in range(R) )) <= 22000)

    #Constraint for objective 2: process quality
    opt_model.add_constraint(Q >= 0.65)

    #Constraint for objective 3: cycle time
    opt_model.add_constraint(C <= 50)

    for i in range(I):
        opt_model.add_constraint(Q <= opt_model.sum(alphaalpha[i][r][t] * x[i,r,t] for r in range(R) for t in range(T) ))
        
    for i in range(I):
        opt_model.add_constraint(opt_model.sum(x[i,r,t] for r in range(R) for t in range(T) ) == 1)
        
        
    for r in range(R):
        for t in range(T):
            opt_model.add_constraint(opt_model.sum(x[i,r,t] for i in range(I) ) <= (I*y[r,t]))


    for t in range(T):
        opt_model.add_constraint(opt_model.sum(y[r,t] for r in range(R)) <= 1)
        
        
    for r in range(R):
        opt_model.add_constraint(opt_model.sum(y[r,t] for t in range(T)) <= (T*z[r]))
        
    #modified cycle time constraints
    opt_model.add_constraint(opt_model.sum(x[i,r,t]*h[i][r][t] for t in range(T) for i in range(I) for r in range(2) ) + opt_model.sum(landa*W[r] for r in range(2)) + opt_model.sum(Z[i,r] for i in range(I) for r in range(2)) <=C)

    for r in range(2,R):
        opt_model.add_constraint(opt_model.sum(x[i,r,t]*h[i][r][t] for t in range(T) for i in range(I) ) + landa*W[r] + opt_model.sum(Z[i,r] for i in range(I)) <=C)

    for i in prec:
        opt_model.add_constraint(opt_model.sum((r)*x[i[0],r,t] for r in range(R) for t in range(T))<=opt_model.sum((r)*x[i[1],r,t] for r in range(R) for t in range(T) ))

    for r in range(R):
        for i in range(I):
            opt_model.add_constraint( W[r] + Z[i,r]  >= opt_model.sum(x[i,r,t]*d[i][r][t] for t in range(T) )) 


    opt_model.minimize(objective1)
    #opt_model.maximize(objective2)
    #opt_model.minimize(objective3)

    opt_model.solve(log_output=True)


    obj_value=opt_model.objective_value
    time=opt_model.get_solve_details().time 
    print(obj_value)
    print(time)   

    ##### get output of the optimal solution for JSON


    from itertools import chain, combinations,product,permutations

    from scipy.stats import truncnorm 

    import gc
    import numpy as np
    import copy
    rnd = np.random
    rnd.seed(320)
    #from statistics import NormalDist
    import json 


    #%% States: For each item we have got a State
    def CreateModel(PlanID):
        #%% Read Json file
        # f = open('EFFRA_ProcessGraph1_precedence.json')
        dataInfra = file  
        AssemblyPlan = dataInfra['AssemblyPlans'][PlanID-1]
        
        #%% Get the information for Tasks
        TaskProcessTime = []
        TaskCost = []
        TaskQulity = []
        ListofTasks = list(range(len(AssemblyPlan['ListOfTaskIDs'])))
        nTask = len(ListofTasks)
        nStation = 0
        nEquipment = 1 # Index 0 of equipment means using no equipment
        equipList = ['None']
        stationList = []
        for _ in range(len(dataInfra['Node'])):
            if dataInfra['Node'][_]['Tasktype'] != 'Feeding' and dataInfra['Node'][_]['Tasktype'] != 'Transport':
                myString = dataInfra['Node'][_]['PRNodeName'].split('+')
                if len(myString)>2 and myString[2] not in equipList:
                    equipList.append(myString[2])
                    nEquipment+=1
                if myString[1] not in stationList:
                    stationList.append(myString[1])
                    nStation+=1
        #%% Get the information of Equipment and Worker
        Process = np.ones((nTask,nStation,nEquipment))*100000000
        Quality = np.zeros((nTask,nStation,nEquipment))
        Cost = np.ones((nTask,nStation,nEquipment))*1000000000
        ListofEquipment = []
        ListofWorkers = []
        for _ in range(len(dataInfra['Node'])):
            if dataInfra['Node'][_]['Tasktype'] != 'Feeding' and dataInfra['Node'][_]['Tasktype'] != 'Transport':
                t =  int(dataInfra['Node'][_]['TaskID'])
                myString = dataInfra['Node'][_]['PRNodeName'].split('+')
                for i in range(nStation):
                    for j in range(nEquipment):
                        if len(myString)>2:
                            if stationList[i] == myString[1] and equipList[j] == myString[2]:
                                Process[t][i][j] = dataInfra['Node'][_]['ProcessTime']
                                Cost[t][i][j] = dataInfra['Node'][_]['Costs']
                                Quality[t][i][j] = dataInfra['Node'][_]['MonitoringEfficiency']
                        else:
                            if stationList[i] == myString[1]:
                                Process[t][i][0] = dataInfra['Node'][_]['ProcessTime']
                                Cost[t][i][0] = dataInfra['Node'][_]['Costs']
                                Quality[t][i][0] = dataInfra['Node'][_]['MonitoringEfficiency']
                                
    #    print(equipList)
    #    print(stationList)
        resourcelist = []
        Compatibility = [[1,3], [2,4], [0,5], [0,5]]
        resourceist = []
        for r in range(len(stationList)) :
            for t in Compatibility[r] :
                resourcelist.append(stationList[r]+'+'+equipList[t])
    #    print(resourcelist)

        listoftasks=[]
        listofresources=[]
        
        for i in range(I):
            for r in range(R):
                for t in range(T):
                    if x[i,r,t].solution_value == 1:
                        listoftasks.append(str(i))
                        listofresources.append(stationList[r]+'+'+equipList[t])
                        #print((i,r,t)," : ",x[i,r,t].solution_value)
                        #print(listoftasks)
                        #print(listofresources)
    #######final optimal task list and resource list 
        listofstations=[]
        
        for i in range(I):
            if listofresources[i][:3] == "Sta":
                listofstations.append("0")
            if listofresources[i][:3] == "UR1":
                listofstations.append("1")
            if listofresources[i][:9] == "Operator1":
                listofstations.append("0")
            if listofresources[i][:9] == "Operator2":
                listofstations.append("2")
        
            
        listofstations=[]
        for i in range(I):
            if listofresources[i][:3] == "Sta":
                listofstations.append(0)
            if listofresources[i][:3] == "UR1":
                listofstations.append(1)
            if listofresources[i][:9] == "Operator1":
                listofstations.append(0)
            if listofresources[i][:9] == "Operator2":
                listofstations.append(2)
            
        
        
    #    listoftasks = json.dumps(listoftasks)
    #    listofresources = json.dumps(listofresources)
    #    listofstations = json.dumps(listofstations)
        print(listoftasks)
        print(listofresources)
        print(listofstations) 
        
        
        return(Process,Quality,Cost,listoftasks,listofresources,listofstations)

    ProcessDic,CostDic,QualityDic,listoftasks,listofresources,listofstations = CreateModel(4)
    PlanID = 4
    optimalcost = []
    optimaltime = []
    optimalquality = []
    optimalcost.append(obj_value)
    optimaltime.append(C.solution_value)
    optimalquality.append(Q.solution_value)
    #######final optimal objective function values 
    print(optimalcost)


    #with open("EFFRA_ProcessGraph1_precedence.json", 'r') as f:
    dataInfra = file
        
    print(listoftasks)
    print(listofstations)
    print(listofresources)
    #listoftasks = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
    #nTasks = len(listoftasks)
    #listofstations = list(np.random.randint(0,4,nTasks))
    #listofresources = ["UR1+ParallelGripper2", "UR1+ParallelGripper2", "UR1+ParallelGripper2", "UR1+Screwdriver2", "UR1+Screwdriver2", "UR1+ParallelGripper2", "UR1+Screwdriver2", "UR1+ParallelGripper2", "UR1+Screwdriver2", "UR1+ParallelGripper2", "UR1+Screwdriver2", "UR1+Screwdriver2", "UR1+Screwdriver2", "UR1+Screwdriver2"]
    setofresources = set(listofresources)
    uniquelistofresources = list(setofresources)
    nStations = len(setofresources)
    nTasks = len(listoftasks)
    nNodes = len(dataInfra['Node'])

    # Ehsan I need this information for every assembly node (Station)
    # So if we have 3 stations, your optimalcost will be something like this: [2411, 2212, 4321]
    # So I am modifying the following lists in a way that I will use
    #optimalcost = [8746.46622642857]
    #optimaltime = [400.0]
    #optimalquality = [0.05]



    # =============================================================================
    # # Generate Nodes for the number of the stations we have
    # 
    # for i in range(nStations):
    #     temp = copy.deepcopy(dataInfra['Node'][0])
    #     dataInfra['Node'].append(temp)
    #     dataInfra['Node'][-1]['AssemblyNode'] = 'AN' + str(i)
    #     dataInfra['Node'][-1]['Costs'] = optimalcost[i]
    #     dataInfra['Node'][-1]['MonitoringEfficiency'] = optimalquality[i]
    #     dataInfra['Node'][-1]['NodeID'] = nNodes + i 
    #     dataInfra['Node'][-1]['PRNodeName'] = dataInfra['Node'][-1]['AssemblyNode'] + '+' + uniquelistofresources[i]
    #     dataInfra['Node'][-1]['ProcessTime'] = optimaltime[i]
    # =============================================================================



    temp = copy.deepcopy(dataInfra['AssemblyPlans'][0])
    dataInfra['AssemblyPlans'].append(temp)
    dataInfra['AssemblyPlans'][-1]['AssemblyPlanID'] = 100
    for i in range(nTasks):
        Assmebly_node = listofresources[i]
        flag = 0
        for j in range(len(dataInfra['Node'])):
            if flag ==0:
                if dataInfra['Node'][j]['PRNodeName'][4:] == Assmebly_node:
                    flag = 1
                    dataInfra['AssemblyPlans'][-1]['ListOfPrimaryNodeIDs'][str(i)] = str(j)
                    dataInfra['AssemblyPlans'][-1]['ListOfStationIDs'][i] = str(listofstations[i])
    dataInfra['AssemblyPlans'][-1]['Optimal Cost']= optimalcost[0]
    dataInfra['AssemblyPlans'][-1]['Optimal Time']= optimaltime[0]
    dataInfra['AssemblyPlans'][-1]['Optimal Quality']= optimalquality[0]                
                    
    #with open("EFFRA_ProcessGraph1_precedence_optimized.json", "w") as outfile:
    #    json.dump(dataInfra, outfile)

    return dataInfra
                
        