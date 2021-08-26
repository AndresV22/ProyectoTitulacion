import os
import random
import xlsxwriter
from techTree import *
import argparse
import logging
import sys

#Obtiene un orden de construcción aleatorio acotado por un tiempo gameTime
def getRandomBuildOrder(techTree, entityId, entityQty, maxTime):
    print("Iniciando...")
    #resources = [Minerals, Vespene, Supply] | where Supply = [Units, Total]
    resources = [50, 0, [13, 15]]
    #Cantidad de unidades o de edificios en un determinado momento
    nodeQty = []
    for name in techTree.vs["name"]:
        nodeQty.append([name, 0])
    #Hay 13 probes al inicio y 1 nexus
    nodeQty[15][1] = 13
    nodeQty[0][1] = 1
    #Cola de construcción
    constructionQueue = []
    #Orden de construcción a retornar
    buildOrder = []
    time = 0
    supplyLeft = resources[2][1] - resources[2][0]
    nextTic = True
    while(nextTic):
        #Se verifica si hay alguna unidad, edificio o tecnología que requiera terminar de construirse

        #Traza
        #print(constructionQueue)

        if(len(constructionQueue) > 0):
            node = 0
            while(node < len(constructionQueue)):
                #Si ya pasó el tiempo de construcción se agregará a nodeQty
                if(constructionQueue[node][1] == 0):
                    #Se verifica que queden suministros para agregar la unidad de ser necesario
                    if(supplyLeft >= techTree.vs[constructionQueue[node][0]]["supply"]):
                        if(techTree.vs[constructionQueue[node][0]]["type"] != "Tech"):
                            #Si hay 200 de suministro entonces no se agregarán mas suministros
                            #Si se construye un pylon se aumentan los suministros
                            if(constructionQueue[node][0] == 2):
                                resources[2][1] += 5
                                supplyLeft = resources[2][1] - resources[2][0]
                            #Si se construye un nexus se aumentan los suministros
                            if(constructionQueue[node][0] == 0):
                                resources[2][1] += 15
                                supplyLeft = resources[2][1] - resources[2][0]
                            #Se agrega la unidad a nodeQty
                            nodeQty[constructionQueue[node][0]][1] += 1
                            #Se suman los suministros de unidades
                            resources[2][0] = resources[2][0] + techTree.vs[constructionQueue[node][0]]["supply"]
                            #Se restan los suministros necesarios para construir la entidad en supplyLeft
                            supplyLeft = supplyLeft - techTree.vs[constructionQueue[node][0]]["supply"]
                            #Se elimina de la lista
                            constructionQueue.pop(node)
                        else:
                            if(nodeQty[constructionQueue[node][0]][1] > 0):
                                constructionQueue.pop(node)
                            else:
                                #Se agrega la unidad a nodeQty
                                nodeQty[constructionQueue[node][0]][1] += 1
                #De lo contrario se le restara 1 gameSpeed y se mantendrá en la cola de construcción
                else:
                    constructionQueue[node][1] -= 1
                #Aumenta el contador de la cola
                node+=1
        #Recolección de recursos (fija al numero de probes por el momento, las lines comentadas de abajo era una posible idea)
        probesTotal = nodeQty[15][1]
        resources[0] += probesTotal*0.916
        resources[1] += probesTotal
        ##################################################
        #Gestión de Minerales y Vespeno
        #Se prioriza la extracción de minerales hasta saturar los nexus
        #Los probes restantes se van a sacar vespeno
        #Y los probes que no puedan sacar vespeno se sumarán a los que extraen minerales
            # probesTotal = nodeQty[15][1]
            # nexusTotal = nodeQty[0][1]
            # assimilatorsTotal = nodeQty[1][1]
            # maxProbesInMinerals = 16*nexusTotal
            # maxProbesInVespene = 3*assimilatorsTotal
            # if(probesTotal <= maxProbesInMinerals):
            #     resources[0] += probesTotal*0.916
            # else:
            #     availableProbes = probesTotal - maxProbesInMinerals
            #     resources[0] += maxProbesInMinerals*0.916
            #     if(availableProbes <= maxProbesInVespene):
            #         resources[1] += 3*availableProbes
            #     else:
            #         probesNotWorking = availableProbes - maxProbesInVespene
            #         resources[1] += maxProbesInVespene
            #         resources[0] += probesNotWorking*0.916
        ##################################################
            
        #Se obtiene un numero random para definir el vertice que se construirá
        nodeToBuild = random.randint(0,60)
        #Se obtiene el camino mas corto para llegar a ese vertice
        pathToNode = getPath(techTree, "Nexus", techTree.vs[nodeToBuild]["name"])
        checkPrerequisites = True
        #Se verifica si los prerrequisitos están construidos
        if(len(pathToNode) > 0):
            for vertexId in pathToNode[0]:
                if(nodeQty[vertexId][1] == 0 and vertexId != nodeToBuild):
                    checkPrerequisites = False
        #Se verifica si es una tecnología ya creada o está siendo creada en la cola
        elementId = techTree.vs[nodeToBuild]["code"]
        if(elementId >= 34):
            if(nodeQty[elementId][1] > 0):
                checkPrerequisites = False
            for queueElement in constructionQueue:
                if queueElement[0] == nodeToBuild:
                    checkPrerequisites = False
        #Traza
        #if(techTree.vs[nodeToBuild]["name"] == "Probe"):
        #    print("Probe ", "minerales: ", resources[0], "gas: ", resources[1], "sum ", resources[2][0],"/",resources[2][1], " Estado: ", checkPrerequisites, "SupplyLeft: ", supplyLeft)
        
        #Se verifica que tenga los recursos suficientes para construir el vertice y que cumpla con los prerrequisitos
        if(checkPrerequisites and resources[0] >= techTree.vs[nodeToBuild]["minerals"] and resources[1] >= techTree.vs[nodeToBuild]["gas"] and supplyLeft >= techTree.vs[nodeToBuild]["supply"]):
            #Se agrega a la cola de construcción
            constructionQueue.append([nodeToBuild, techTree.vs[nodeToBuild]["gameSpeed"]])
            resources[0] = resources[0] - techTree.vs[nodeToBuild]["minerals"]
            resources[1] = resources[1] - techTree.vs[nodeToBuild]["gas"]
            nodeQtyToAdd = nodeQty.copy()
            constructionQueueToAdd = constructionQueue.copy()
            #Se agrega al build order en el tiempo en que se ejecuta la acción de empezar a construir el vertice
            buildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), constructionQueueToAdd.copy(), nodeQtyToAdd.copy()])
        #Si se logra la cantidad ingresada por el usuario se detiene la construcción
        if((nodeQty[entityId][1] == entityQty) or time == maxTime):
            nextTic = False
        else: 
            time += 1
    return buildOrder

def printBuildOrder(buildOrder):
    print("")
    print("Tiempo | Unidad | Suministros | Minerales | Vespeno")
    for element in buildOrder:
        print(element[0], " | ", element[1], " | ", element[2], "/", element[3], " | ", element[4], " | ", element[5])
    print("")

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def perturbationFunction(buildOrder, techTree, entityId, entityQty, maxTime):
    #Traza: print("Tiempo final: ", buildOrder[-1][0])
    timeSelected = random.randint(buildOrder[0][0],buildOrder[-1][0])
    #Traza: print("Numero random: ", timeSelected)
    brotherBuildOrder = []
    #Cantidad de unidades o de edificios en un determinado momento
    #Se agrega cada elemento del build order original al nuevo build order, hasta llegar al tiempo seleccionado
    for element in buildOrder:
        if(element[0] <= timeSelected):
            elementToAppend = element
            brotherBuildOrder.append(elementToAppend)

    #Malo, hay que contar cada elemento de la brotherBuildOrder y calcular el nuevo brotherNodeQty
    #brotherNodeQty = list(brotherBuildOrder[-1][7])

    #Se crea nuevo NodeQty desde cero
    brotherNodeQty = []
    for name in techTree.vs["name"]:
        brotherNodeQty.append([name, 0])
    brotherNodeQty[15][1] = 13
    brotherNodeQty[0][1] = 1

    #Se obtienen las unidades y edificios ya creadas y se agregan al nodeQty
    for element in brotherBuildOrder:
        for node in brotherNodeQty:
            if(node[0] == element[1]):
                node[1] += 1
    
    #Traza: print("brotherNodeQty del BO hermano: ", brotherNodeQty[entityId][1], "Cantidad requerida: ", entityQty)
    #resources = [Minerals, Vespene, Supply] | where Supply = [Units, Total]
    resources = []
    minerals = brotherBuildOrder[-1][4]
    vespene = brotherBuildOrder[-1][5]
    actualSupply = brotherBuildOrder[-1][2]
    totalSupply = brotherBuildOrder[-1][3]
    resources.append(minerals)
    resources.append(vespene)
    resources.append([actualSupply, totalSupply])
    
    #Cola de construcción
    constructionQueue = list(brotherBuildOrder[-1][6])
    time = brotherBuildOrder[-1][0]+1
    supplyLeft = brotherBuildOrder[-1][3] - brotherBuildOrder[-1][2]
    nextTic = True
    while(nextTic):
        #Se verifica si hay alguna unidad, edificio o tecnología que requiera terminar de construirse

        #Traza
        #print(constructionQueue)

        if(len(constructionQueue) > 0):
            node = 0
            while(node < len(constructionQueue)):
                #Si ya pasó el tiempo de construcción se agregará a brotherNodeQty
                if(constructionQueue[node][1] == 0):
                    #Se verifica que queden suministros para agregar la unidad de ser necesario
                    if(supplyLeft >= techTree.vs[constructionQueue[node][0]]["supply"]):
                        if(techTree.vs[constructionQueue[node][0]]["type"] != "Tech"):
                            #Si hay 200 de suministro entonces no se agregarán mas suministros
                            #Si se construye un pylon se aumentan los suministros
                            if(constructionQueue[node][0] == 2):
                                resources[2][1] += 5
                                supplyLeft = resources[2][1] - resources[2][0]
                            #Si se construye un nexus se aumentan los suministros
                            if(constructionQueue[node][0] == 0):
                                resources[2][1] += 15
                                supplyLeft = resources[2][1] - resources[2][0]
                            #Se agrega la unidad a brotherNodeQty
                            brotherNodeQty[constructionQueue[node][0]][1] += 1
                            #Se suman los suministros de unidades
                            resources[2][0] = resources[2][0] + techTree.vs[constructionQueue[node][0]]["supply"]
                            #Se restan los suministros necesarios para construir la entidad en supplyLeft
                            supplyLeft = supplyLeft - techTree.vs[constructionQueue[node][0]]["supply"]
                            #Se elimina de la lista
                            constructionQueue.pop(node)
                        else:
                            if(brotherNodeQty[constructionQueue[node][0]][1] > 0):
                                constructionQueue.pop(node)
                            else:
                                #Se agrega la unidad a brotherNodeQty
                                brotherNodeQty[constructionQueue[node][0]][1] += 1
                #De lo contrario se le restara 1 gameSpeed y se mantendrá en la cola de construcción
                else:
                    constructionQueue[node][1] -= 1
                #Aumenta el contador de la cola
                node+=1
        #Recolección de recursos (fija al numero de probes por el momento, las lines comentadas de abajo era una posible idea)
        probesTotal = brotherNodeQty[15][1]
        resources[0] += probesTotal*0.916
        resources[1] += probesTotal
            
        #Se obtiene un numero random para definir el vertice que se construirá
        nodeToBuild = random.randint(0,60)
        #Se obtiene el camino mas corto para llegar a ese vertice
        pathToNode = getPath(techTree, "Nexus", techTree.vs[nodeToBuild]["name"])
        checkPrerequisites = True
        #Se verifica si los prerrequisitos están construidos
        if(len(pathToNode) > 0):
            for vertexId in pathToNode[0]:
                if(brotherNodeQty[vertexId][1] == 0 and vertexId != nodeToBuild):
                    checkPrerequisites = False
        #Se verifica si es una tecnología ya creada o está siendo creada en la cola
        elementId = techTree.vs[nodeToBuild]["code"]
        if(elementId >= 34):
            if(brotherNodeQty[elementId][1] > 0):
                checkPrerequisites = False
            for queueElement in constructionQueue:
                if queueElement[0] == nodeToBuild:
                    checkPrerequisites = False
        #Traza
        #if(techTree.vs[nodeToBuild]["name"] == "Probe"):
        #    print("Probe ", "minerales: ", resources[0], "gas: ", resources[1], "sum ", resources[2][0],"/",resources[2][1], " Estado: ", checkPrerequisites, "SupplyLeft: ", supplyLeft)
        
        #Se verifica que tenga los recursos suficientes para construir el vertice y que cumpla con los prerrequisitos
        if(checkPrerequisites and resources[0] >= techTree.vs[nodeToBuild]["minerals"] and resources[1] >= techTree.vs[nodeToBuild]["gas"] and supplyLeft >= techTree.vs[nodeToBuild]["supply"]):
            #Se agrega a la cola de construcción
            constructionQueue.append([nodeToBuild, techTree.vs[nodeToBuild]["gameSpeed"]])
            resources[0] = resources[0] - techTree.vs[nodeToBuild]["minerals"]
            resources[1] = resources[1] - techTree.vs[nodeToBuild]["gas"]
            brotherNodeQtyToAdd = []
            for element in brotherNodeQty:
                brotherNodeQtyToAdd.append(element)
            constructionQueueToAdd = []
            for element in constructionQueue:
                constructionQueueToAdd.append(element)
            #Se agrega al build order en el tiempo en que se ejecuta la acción de empezar a construir el vertice
            brotherBuildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), list(constructionQueueToAdd), list(brotherNodeQtyToAdd)])
        #Si se logra la cantidad ingresada por el usuario se detiene la construcción
        if((brotherNodeQty[entityId][1] == entityQty) or (time >= maxTime)):
            #Traza: print("Se ha cumplido el requisito o se ha llegado al tiempo máximo...")
            nextTic = False
        else: 
            time += 1
    return brotherBuildOrder

#Entrega un puntaje a la orden de construcción basado en el tiempo logrado y en las unidades restantes por construir
def scoreBuildOrder(techTree, buildOrder, entityId, entityQty, maxTime, minTime):
    time = buildOrder[-1][0]
    nodeQty = buildOrder[-1][7]
    pathToNode = getPath(techTree, "Nexus", techTree.vs[entityId]["name"])
    entitiesToBuild = len(pathToNode[0]) + entityQty #Son las entidades que se deben construir incluyendo prerrequisitos
    maxEntities = len(pathToNode[0]) + entityQty #Total de entidades por construir
    for node in pathToNode[0]:
        if(nodeQty[node][1] >= 1):
            entitiesToBuild-=1 #Se restan los prerrequisitos si es que ya existen
    entitiesBuilt = nodeQty[entityId][1] #Son las entidades solicitadas totales que ya fueron construidas
    entitiesToBuild-=entitiesBuilt #Se restan las entidades solicitadas que ya fueron construidas
    if(entitiesToBuild > 0 and maxTime != minTime):
        print("e>0 - división en tiempo: ", maxTime-minTime)
        print("e>0 - división en entidades: ", maxEntities)
        score = (0.2*((time-minTime)/(maxTime-minTime)) + 0.8*(entitiesToBuild/maxEntities))
    if(entitiesToBuild <= 0 and maxTime != minTime):
        print("e<0 - división en tiempo: ", maxTime-minTime)
        score = (0.2*((time-minTime)/(maxTime-minTime)) + 0.8)
    if(entitiesToBuild > 0 and maxTime == minTime):
        print("e>0 - división en tiempo: ", maxTime-minTime)
        print("e>0 - división en entidades: ", maxEntities)
        score = (0.8*(entitiesToBuild/maxEntities))
    if(entitiesToBuild <= 0 and maxTime == minTime):
        score = 0
    result = [time, maxTime, entitiesBuilt, entitiesToBuild, entityQty, score]
    return(result)

#Algoritmo Greedy, genera una solución después de muchas perturbaciones e iteraciones.
def greedy(techTree, buildOrder, entityId, entityQty, maxTime, perturbations, iterations):
    bestSolution = list(buildOrder)
    bestScore = scoreBuildOrder(techTree, buildOrder, entityId, entityQty, maxTime, 0)
    iteration = 1
    minTimeOfGen = bestSolution[-1][0]
    while(iteration <= iterations):
        perturbation = 1
        perturbedSolutions = []
        while(perturbation <= perturbations):
            perturbedSolutions.append(perturbationFunction(list(bestSolution), techTree, entityId, entityQty, minTimeOfGen))
            perturbation+=1
        for solution in perturbedSolutions:
            if(solution[-1][0] < minTimeOfGen):
                minTimeOfGen = solution[-1][0]
        for solution in perturbedSolutions:
            newScore = scoreBuildOrder(techTree, list(solution), entityId, entityQty, maxTime, minTimeOfGen)
            if(newScore[-1] > bestScore[-1]):
                bestScore = newScore
                bestSolution = list(solution)
        iteration+=1
    return bestSolution

#Algoritmo de búsqueda local iterada
def iteratedLocalSearch(techTree, entityId, entityQty, maxTime, perturbations, iterations, iterationsILS):
    #Se obtiene una orden de construcción aleatoria y se aplica una busqueda local
    buildOrder = getRandomBuildOrder(techTree, entityId, entityQty, maxTime)
    initialSolution = greedy(techTree, list(buildOrder), entityId, entityQty, maxTime, perturbations, iterations)
    initialScore = scoreBuildOrder(techTree, list(initialSolution), entityId, entityQty, maxTime, 0)
    iteration = 1
    progress = 0
    genScores = [["Generación", "Puntaje"]]
    cls()
    print("Calculando, por favor espere...")
    print("Progreso: ", progress, "%")
    #En cada iteración se perturba la solución inicial y se aplica otra búsqueda local
    while(iteration <= iterationsILS):
        cls()
        print("Calculando, por favor espere...")
        print("Progreso: ", progress, "%")
        perturbatedSolution = perturbationFunction(list(initialSolution), techTree, entityId, entityQty, maxTime)
        localSolution = greedy(techTree, list(perturbatedSolution), entityId, entityQty, maxTime, perturbations, iterations)
        score = scoreBuildOrder(techTree, list(localSolution), entityId, entityQty, maxTime, initialSolution[-1][0])
        genScores.append([iteration, score[-1]])
        #Si el puntaje es mejor, se considera que la solución local es la solución inicial
        if(score[-1] > initialScore[-1]):
            initialSolution = []
            initialSolution = list(localSolution)
        progress = (iteration/iterationsILS)*100
        iteration+=1

    result = list(initialSolution)

    # cls()
    # print("- Completado -")
    # generateFiles = input("¿Deseas guardar los resultados en archivos xlsx? (s/n): ")

    # if(generateFiles == 's' or generateFiles == 'S'):
    #     with xlsxwriter.Workbook('genScores.xlsx') as workbook:
    #         worksheet = workbook.add_worksheet()

    #         for row_num, data in enumerate(genScores):
    #             worksheet.write_row(row_num, 0, data)
        
    #     cleanResult = [["Time", "Entity", "Supply Occupied", "Total Supply", "Minerals", "Vespene"]]
    #     for row in result:
    #         cleanResult.append([row[0], row[1], row[2], row[3], row[4], row[5]])

    #     with xlsxwriter.Workbook('BuildOrder_Solution.xlsx') as workbook:
    #         worksheet = workbook.add_worksheet()

    #         for row_num, data in enumerate(cleanResult):
    #             worksheet.write_row(row_num, 0, data)
        
    #     entitiesBuilt = list(result[-1][-1])
        
    #     with xlsxwriter.Workbook('EntitiesBuilt.xlsx') as workbook:
    #         worksheet = workbook.add_worksheet()

    #         for row_num, data in enumerate(entitiesBuilt):
    #             worksheet.write_row(row_num, 0, data)

    return result

def main(PERT, ITER, ITERILS, DATFILE):
    techTree = initTechTree()
    entityId = 16
    entityQty = 10
    maxTime = 2000
    solution = iteratedLocalSearch(techTree, entityId, entityQty, maxTime, PERT, ITER, ITERILS)
    score = scoreBuildOrder(techTree, solution, entityId, entityQty, maxTime, 0)
    
    with open(DATFILE, 'w') as f:
	    f.write(str(score[-1]*100))

if __name__ == "__main__":
    # just check if args are ok
    with open('args.txt', 'w') as f:
        f.write(str(sys.argv))

    # loading example arguments
    ap = argparse.ArgumentParser(description='Build order optimization using iterated local search')
    ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    # 5 args to test values
    ap.add_argument('--pert', dest='pert', type=int, required=True, help='Population size')
    ap.add_argument('--iterils', dest='iterils', type=int, required=True, help='Mutation probability')
    ap.add_argument('--iter', dest='iter', type=int, required=True, help='Crossover probability')
    # 1 arg file name to save and load fo value
    ap.add_argument('--datfile', dest='datfile', type=str, required=True, help='File where it will be save the score (result)')

    args = ap.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    logging.debug(args)
    # call main function passing args
    main(args.pert, args.iter, args.iterils, args.datfile)