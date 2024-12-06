from backend.backend.utils.imports import import_json
import numpy as np


class AssistantModel:
    def __init__(self, json_file):
        json_dict = json_file if type(json_file) is dict else import_json(json_file)

    def CreateModel(PlanID):
        # %% Read Json file
        f = open('ProcessGraph1_precedence_fuzzy values.json')
        dataInfra = json.load(f)
        AssemblyPlan = dataInfra['AssemblyPlans'][PlanID - 1]

        # %% Get the information for Tasks
        # TaskProcessTime = []
        # TaskCost = []
        # TaskQulity = []
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
        ListofTasks = list(range(len(AssemblyPlan['ListOfTaskIDs'])))
        nStation = len(stationList)
        nEquipment = len(equipList)  # Index 0 of equipment means using no equipment
        nTask = len(ListofTasks)
        # %% Get the information of Equipment and Worker
        Process = np.ones((nTask, nStation, nEquipment)) * 100000000
        Quality = np.zeros((nTask, nStation, nEquipment))
        Cost = np.ones((nTask, nStation, nEquipment)) * 1000000000
        # ListofEquipment = []
        # ListofWorkers = []
        for _ in range(len(dataInfra['Node'])):
            if dataInfra['Node'][_]['Tasktype'] != 'Feeding':
                t = int(dataInfra['Node'][_]['TaskID'])
                myString = dataInfra['Node'][_]['PRNodeName'].split('+')
                if len(myString) == 2:
                    myString.append('None')
                for i in range(nStation):
                    for j in range(nEquipment):
                        if stationList[i] == myString[1] and equipList[j] == myString[2]:
                            Process[t][i][j] = dataInfra['Node'][_]['ProcessTime']
                            Cost[t][i][j] = dataInfra['Node'][_]['Costs']
                            Quality[t][i][j] = dataInfra['Node'][_]['MonitoringEfficiency']

        return Process, Quality, Cost



if __name__ == '__main__':
    model = AssistantModel('ProcessGraph1_precedence_fuzzy values.json')
    kpi = model.CreateModel(4)
