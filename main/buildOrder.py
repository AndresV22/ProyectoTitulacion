import os
import random
from techTree import *
from copy import deepcopy
import datetime

#Obtiene un orden de construcción aleatorio acotado por un tiempo gameTime
def getRandomBuildOrder(techTree, entityId, entityQty, maxTime):
    print("Iniciando...")
    print("El proceso puede demorar varios minutos en empezar, por favor espere.")
    #resources = [Minerals, Vespene, Supply] | where Supply = [Units, Total]
    resources = [50, 0, [13, 15]]
    #Cantidad de unidades o de edificios en un determinado momento
    nodeQty = []
    #Se crea la cola de construcción por edificio
    #Se crea el arreglo que contiene la cantidad de entidades
    for name in techTree.vs["name"]:
        nodeQty.append([name, 0])
    #Hay 13 probes al inicio y 1 nexus
    nodeQty[15][1] = 13
    nodeQty[0][1] = 1
    #Cola de construcción de edificios
    constructionQueue = []
    #Cola de construcción de arcontes
    archonQueue = []
    #Cola de construccion de unidades: [Nombre edificio construye, codigo unidad, gamespeed, cooldown, duración chronoboost, energía]
    unitQueue = [["Nexus", [], [], [], 0, 50]]
    #Orden de construcción a retornar
    buildOrder = []
    isWarpGateActive = False
    time = 0
    supplyLeft = resources[2][1] - resources[2][0]
    nextTic = True
    while(nextTic):
        #Se verifica si hay alguna unidad, edificio o tecnología que requiera terminar de construirse
        if(len(archonQueue) > 0):
            #print("archonQueue")
            for index, archon in enumerate(archonQueue, start=0):
                #Se construye
                if(archon[1] == 0):
                    nodeQty[28][1] += 1
                    archonQueue.pop(index)
                #Tiempo restante para generar archon
                else:
                    archon[1] -= 1

        if(len(unitQueue) > 0):
            #print("unitQueue")
            for building in unitQueue:
                chrono = False
                if(building[5]>0):
                    chrono = True
                if (len(building[1]) > 0):
                    if(building[2][0] <= 0):
                        #Si se construye el warp gate
                        if(building[1][0] == 49):
                            applyWarpGate(techTree)
                            isWarpGateActive = True
                        #Se agrega cooldown si es un Zealot
                        if(isWarpGateActive and building[1][0] == 16):
                            building[3].append(20)
                        #Se agrega cooldown si es un Stalker
                        if(isWarpGateActive and building[1][0] == 17):
                            building[3].append(30)
                        #Se agrega cooldown si es un Sentry
                        if(isWarpGateActive and building[1][0] == 18):
                            building[3].append(23)
                        #Se agrega cooldown si es un Adept
                        if(isWarpGateActive and building[1][0] == 19):
                            building[3].append(30)
                        #Se agrega cooldown si es un Dark Templar
                        if(isWarpGateActive and building[1][0] == 26):
                            building[3].append(39)
                        #Se agrega cooldown si es un High Templar
                        if(isWarpGateActive and building[1][0] == 27):
                            building[3].append(39)
                        #Se agrega la unidad a nodeQty
                        nodeQty[building[1][0]][1] += 1
                        #Se suman los suministros de unidades
                        resources[2][0] += techTree.vs[building[1][0]]["supply"]
                        #Se restan los suministros necesarios para construir la entidad en supplyLeft
                        supplyLeft = supplyLeft - techTree.vs[building[1][0]]["supply"]
                        #Se elimina de la deepcopya
                        building[1].pop(0)
                        building[2].pop(0)
                    else:
                        if(len(building[3]) > 0):
                            if(building[3][0] <= 0):
                                building[3].pop(0)
                            else:
                                if(chrono == True):
                                    building[3][0]-=1.5
                                else:
                                    building[3][0]-=1
                        else:
                            if(chrono == True):
                                building[2][0]-=1.5
                            else:
                                building[2][0]-=1
                    if(building[4] > 0):
                        building[4]-=1

        if(len(constructionQueue) > 0):
            #print("constructionQueue")
            node = 0
            while(node < len(constructionQueue)):
                #Si ya pasó el tiempo de construcción se agregará a nodeQty
                if(constructionQueue[node][1] == 0):
                    #Si hay 200 de suministro entonces no se agregarán mas suministros
                    #Si se construye un pylon se aumentan los suministros
                    if(constructionQueue[node][0] == 2):
                        if(resources[2][1] >= 195):
                            resources[2][1] = 200
                        else:
                            resources[2][1] += 5
                        supplyLeft = resources[2][1] - resources[2][0]
                    #Si se construye un nexus se aumentan los suministros
                    if(constructionQueue[node][0] == 0):
                        if(resources[2][1] >= 185):
                            resources[2][1] = 200
                        else:
                            resources[2][1] += 15
                        supplyLeft = resources[2][1] - resources[2][0]

                    if(constructionQueue[node][0] != 1 and constructionQueue[node][0] != 2 and constructionQueue[node][0] != 6 and constructionQueue[node][0] != 7):
                        #Se agrega el edificio a unitQueue
                        unitQueue.append([techTree.vs[constructionQueue[node][0]]["name"], [], [], [], 0, techTree.vs[constructionQueue[node][0]]["initialEnergy"]])
                    
                    #Se agrega la unidad a nodeQty
                    nodeQty[constructionQueue[node][0]][1] += 1
                    #Se elimina de la deepcopy
                    constructionQueue.pop(node)
                #De lo contrario se le restara 1 gameSpeed y se mantendrá en la cola de construcción
                else:
                    constructionQueue[node][1] -= 1
                #Aumenta el contador de la cola
                node+=1
        #print("Recoleccion recursos")
        #Recolección de recursos (fija al numero de probes por el momento, las lines comentadas de abajo era una posible idea)
        probesTotal = nodeQty[15][1]
        assimilatorsTotal = nodeQty[1][1]
        maxProbesInVespene = 3*assimilatorsTotal
        probesMiningVesp = 0
        probesMiningMine = 0
        probe = 1
        #Se asignan probes para recolectar recursos dependiendo de la cantidad de assimilators que existan
        while(probe <= probesTotal):
            if(maxProbesInVespene > 0 and probesMiningVesp <= maxProbesInVespene):
                probesMiningVesp += 1
            probesMiningMine += 1
            probe += 1
        resources[0] += probesMiningMine*0.916
        resources[1] += probesMiningVesp

        #Se suma energía a los Nexus
        for building in unitQueue:
            if(building[0] == "Nexus"):
                building[5]+=0.7875

        #Se obtiene un numero random para definir el vertice que se construirá
        nodeToBuild = random.randint(0,60)
        if((nodeToBuild == 2 or nodeToBuild == 0) and resources[2][1] == 200):
            nodeToBuild = random.randint(3,60)
        #print("Nodo a construir: ", nodeToBuild)

        #print("Obtener path")
        #Se obtiene el camino mas corto para llegar a ese vertice
        if(nodeToBuild != 31 and nodeToBuild != 15):
            pathToNode = getPath(techTree, "Pylon", techTree.vs[nodeToBuild]["name"])
        if(nodeToBuild == 31 or nodeToBuild == 15):
            pathToNode = getPath(techTree, "Nexus", techTree.vs[nodeToBuild]["name"])

        #print("check Prerequisites 1")
        checkPrerequisites = True
        #Se verifica si los prerrequisitos están construidos
        if(len(pathToNode) > 0):
            for vertexId in pathToNode[0]:
                if(nodeQty[vertexId][1] == 0 and vertexId != nodeToBuild):
                    checkPrerequisites = False

        #print("check Prerequisites 2")
        #Se verifica si es una tecnología ya creada o está siendo creada en la cola
        elementId = techTree.vs[nodeToBuild]["code"]
        if(elementId >= 34):
            if(nodeQty[elementId][1] > 0):
                checkPrerequisites = False
            for element in unitQueue:
                for unit in element[1]:
                    if unit == nodeToBuild:
                        checkPrerequisites = False

        #print("check Prerequisites 3")
        #Se verifica si es un archonte y si hay templarios para construirlo
        if(nodeToBuild == 28):
            if(nodeQty[26][1] <= 2 and nodeQty[27][1] <= 2):
                checkPrerequisites = False
        
        applyChrono = False
        index = 0
        indexNexus = 0
        while(index < len(unitQueue)):
            building = unitQueue[index]
            if (building[0] == "Nexus"):
                if(building[5] >= 50):
                    applyChrono = True
                    indexNexus = index
            index += 1

        #Traza
        #if(techTree.vs[nodeToBuild]["name"] == "Probe"):
        #    print("Probe ", "minerales: ", resources[0], "gas: ", resources[1], "sum ", resources[2][0],"/",resources[2][1], " Estado: ", checkPrerequisites, "SupplyLeft: ", supplyLeft)
        
        #Se verifica que tenga los recursos suficientes para construir el vertice y que cumpla con los prerrequisitos
        if(checkPrerequisites and resources[0] >= techTree.vs[nodeToBuild]["minerals"] and resources[1] >= techTree.vs[nodeToBuild]["gas"] and supplyLeft >= techTree.vs[nodeToBuild]["supply"]):
            #print("Alocate entity")
            #Se agrega a la cola de construcción de unidad/tecnología
            if(techTree.vs[nodeToBuild]["type"] != "Building"):
                #print("Alocate in unitQueue")
                allocated = False
                #Si el nodo a construir no es un Archon
                if(nodeToBuild != 28):
                    #print("Is not Archon")
                    for building in unitQueue:
                        buildOn = techTree.vs[nodeToBuild]["buildOn"]
                        if(building[0] == techTree.vs[buildOn]["name"] and allocated == False):
                            if(len(building[1]) < 5):
                                if(applyChrono == True):
                                    unitQueue[indexNexus][5]-=50
                                    building[4] = 20
                                building[1].append(techTree.vs[nodeToBuild]["code"])
                                building[2].append(techTree.vs[nodeToBuild]["gameSpeed"])
                                allocated = True
                                if(applyChrono == True):
                                    buildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(nodeQty), deepcopy(unitQueue), deepcopy(archonQueue), "Chronoboost"])
                                else:
                                    buildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(nodeQty), deepcopy(unitQueue), deepcopy(archonQueue), ""])

                else:
                    #print("Is Archon")
                    #Se añade Archon a cola de producción y se restan templarios
                    if(nodeQty[26][1] >= 2):
                        #print("Building Archon with Dark Templars")
                        nodeQty[26][1] -= 2
                        archonQueue.append([techTree.vs[nodeToBuild]["name"], 1, techTree.vs[nodeToBuild]["gameSpeed"]])
                        buildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(nodeQty), deepcopy(unitQueue), deepcopy(archonQueue), ""])

                    elif(nodeQty[27][1] >= 2):
                        #print("Building Archon with High Templars")
                        nodeQty[27][1] -= 2
                        archonQueue.append([techTree.vs[nodeToBuild]["name"], 1, techTree.vs[nodeToBuild]["gameSpeed"]])
                        buildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(nodeQty), deepcopy(unitQueue), deepcopy(archonQueue), ""])
                if((nodeQty[entityId][1] == entityQty) or time >= maxTime or resources[2][0] >= 200):
                    nextTic = False
                    buildOrder[-1][7] = nodeQty
                else:
                    time += 1
            else:
                #print("Alocate in construction queue") 
                #Se agrega a la cola de construcción de edificios
                constructionQueue.append([nodeToBuild, techTree.vs[nodeToBuild]["gameSpeed"]])
                resources[0] = resources[0] - techTree.vs[nodeToBuild]["minerals"]
                resources[1] = resources[1] - techTree.vs[nodeToBuild]["gas"]
                buildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(nodeQty), deepcopy(unitQueue), deepcopy(archonQueue), ""])
                if((nodeQty[entityId][1] == entityQty) or time >= maxTime or resources[2][0] >= 200):
                    nextTic = False
                    buildOrder[-1][7] = nodeQty
                else:
                    time += 1
            #### unitQueueToAdd = deepcopy(unitQueue)
            #Se agrega al build order en el tiempo en que se ejecuta la acción de empezar a construir el vertice
        #Si se logra la cantidad ingresada por el usuario se detiene la construcción
        if((nodeQty[entityId][1] == entityQty) or time >= maxTime or resources[2][0] >= 200):
            nextTic = False
            #Esta asignación se realiza ya que existen casos en que al no agregar nada al orden de costrucción, no se actualiza nodeQty y
            #Y en vez de las X unidades completadas mostraría X-1 unidades completadas.
            buildOrder[-1][7] = nodeQty
        else:
            time += 1
    return buildOrder

def perturbationFunction(buildOrder, techTree, entityId, entityQty, maxTime):
    #Traza: print("Tiempo final: ", buildOrder[-1][0])
    timeSelected = random.randint(buildOrder[0][0],buildOrder[-1][0])
    #Traza: pprint("Numero random: ", timeSelected)
    brotherBuildOrder = deepcopy(buildOrder)
    index = 0
    while(index < len(brotherBuildOrder)):
        if(brotherBuildOrder[index][0] > timeSelected):
            brotherBuildOrder.pop(index)
        else:
            index += 1
    
    brotherNodeQty = deepcopy(brotherBuildOrder[-1][7])
    #Traza: pprint("Entidades construides en BO hermano: ", brotherNodeQty[entityId][1], "Cantidad requerida: ", entityQty)
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
    unitQueue = deepcopy(brotherBuildOrder[-1][8])
    archonQueue = deepcopy(brotherBuildOrder[-1][9])
    constructionQueue = deepcopy(brotherBuildOrder[-1][6])
    time = brotherBuildOrder[-1][0]+1
    supplyLeft = brotherBuildOrder[-1][3] - brotherBuildOrder[-1][2]
    nextTic = True
    if(brotherNodeQty[49][1] == 1):
        isWarpGateActive = True
    else:
        isWarpGateActive = False
    while(nextTic):
        #Se verifica si hay alguna unidad, edificio o tecnología que requiera terminar de construirse

        if(len(archonQueue) > 0):
            for index, archon in enumerate(archonQueue, start=0):
                #Se construye
                if(archon[1] == 0):
                    brotherNodeQty[28][1] += 1
                    archonQueue.pop(index)
                #Tiempo restante para generar archon
                else:
                    archon[1] -= 1

        if(len(unitQueue) > 0):
            for building in unitQueue:
                chrono = False
                if(building[5]>0):
                    chrono = True
                if (len(building[1]) > 0):
                    if(building[2][0] <= 0):
                        #Si se construye el warp gate
                        if(building[1][0] == 49):
                            applyWarpGate(techTree)
                            isWarpGateActive = True
                        #Se agrega cooldown si es un Zealot
                        if(isWarpGateActive and building[1][0] == 16):
                            building[3].append(20)
                        #Se agrega cooldown si es un Stalker
                        if(isWarpGateActive and building[1][0] == 17):
                            building[3].append(30)
                        #Se agrega cooldown si es un Sentry
                        if(isWarpGateActive and building[1][0] == 18):
                            building[3].append(23)
                        #Se agrega cooldown si es un Adept
                        if(isWarpGateActive and building[1][0] == 19):
                            building[3].append(30)
                        #Se agrega cooldown si es un Dark Templar
                        if(isWarpGateActive and building[1][0] == 26):
                            building[3].append(39)
                        #Se agrega cooldown si es un High Templar
                        if(isWarpGateActive and building[1][0] == 27):
                            building[3].append(39)
                        #Se agrega la unidad a brotherNodeQty
                        brotherNodeQty[building[1][0]][1] += 1
                        #Se suman los suministros de unidades
                        resources[2][0] = resources[2][0] + techTree.vs[building[1][0]]["supply"]
                        #Se restan los suministros necesarios para construir la entidad en supplyLeft
                        supplyLeft = supplyLeft - techTree.vs[building[1][0]]["supply"]
                        #Se elimina de la deepcopya
                        building[1].pop(0)
                        building[2].pop(0)
                    else:
                        if(len(building[3]) > 0):
                            if(building[3][0] <= 0):
                                building[3].pop(0)
                            else:
                                if(chrono == True):
                                    building[3][0]-=1.5
                                else:
                                    building[3][0]-=1
                        else:
                            if(chrono == True):
                                building[2][0]-=1.5
                            else:
                                building[2][0]-=1
                    if(building[4] > 0):
                        building[4]-=1

        if(len(constructionQueue) > 0):
            node = 0
            while(node < len(constructionQueue)):
                #Si ya pasó el tiempo de construcción se agregará a nodeQty
                if(constructionQueue[node][1] == 0):
                    #Si hay 200 de suministro entonces no se agregarán mas suministros
                    #Si se construye un pylon se aumentan los suministros
                    if(constructionQueue[node][0] == 2):
                        if(resources[2][1] >= 195):
                            resources[2][1] = 200
                        else:
                            resources[2][1] += 5
                        supplyLeft = resources[2][1] - resources[2][0]
                    #Si se construye un nexus se aumentan los suministros
                    if(constructionQueue[node][0] == 0):
                        if(resources[2][1] >= 185):
                            resources[2][1] = 200
                        else:
                            resources[2][1] += 15
                        supplyLeft = resources[2][1] - resources[2][0]
                    #Si el edificio puede entrenar unidades o investigar tecnologías se agrega al unitQueue
                    if(constructionQueue[node][0] != 1 and constructionQueue[node][0] != 2 and constructionQueue[node][0] != 6 and constructionQueue[node][0] != 7):
                        #Se agrega el edificio a unitQueue
                        unitQueue.append([techTree.vs[constructionQueue[node][0]]["name"], [], [], [], 0, techTree.vs[constructionQueue[node][0]]["initialEnergy"]])
                        
                    #Se agrega el edificio a brotherNodeQty
                    brotherNodeQty[constructionQueue[node][0]][1] += 1
                    #Se elimina de la deepcopya
                    constructionQueue.pop(node)
                #De lo contrario se le restara 1 gameSpeed y se mantendrá en la cola de construcción
                else:
                    constructionQueue[node][1] -= 1
                #Aumenta el contador de la cola
                node+=1
        
        #Recolección de recursos (fija al numero de probes por el momento, las lines comentadas de abajo era una posible idea)
        #Gestión de Minerales y Vespeno
        probesTotal = brotherNodeQty[15][1]
        assimilatorsTotal = brotherNodeQty[1][1]
        maxProbesInVespene = 3*assimilatorsTotal
        probesMiningVesp = 0
        probesMiningMine = 0
        probe = 1
        #Se asignan probes para recolectar recursos dependiendo de la cantidad de assimilators que existan
        while(probe <= probesTotal):
            if(maxProbesInVespene > 0 and probesMiningVesp <= maxProbesInVespene):
                probesMiningVesp += 1
            probesMiningMine += 1
            probe += 1
        resources[0] += probesMiningMine*0.916
        resources[1] += probesMiningVesp

        for building in unitQueue:
            if(building[0] == "Nexus"):
                building[5]+=0.7875
            
        #Se obtiene un numero random para definir el vertice que se construirá
        nodeToBuild = random.randint(0,60)

        #Se obtiene el camino mas corto para llegar a ese vertice
        if(nodeToBuild != 31 and nodeToBuild != 15):
            pathToNode = getPath(techTree, "Pylon", techTree.vs[nodeToBuild]["name"])
        if(nodeToBuild == 31 or nodeToBuild == 15):
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
            for element in unitQueue:
                for unit in element[1]:
                    if unit == nodeToBuild:
                        checkPrerequisites = False

        #Se verifica si es un archonte y si hay templarios para construirlo
        if(nodeToBuild == 28):
            if(brotherNodeQty[26][1] <= 2 and brotherNodeQty[27][1] <= 2):
                checkPrerequisites = False

        applyChrono = False
        index = 0
        indexNexus = 0
        while(index < len(unitQueue)):
            building = unitQueue[index]
            if (building[0] == "Nexus"):
                if(building[5] >= 50):
                    applyChrono = True
                    indexNexus = index
            index += 1
        #Traza
        #if(techTree.vs[nodeToBuild]["name"] == "Probe"):
        #    print("Probe ", "minerales: ", resources[0], "gas: ", resources[1], "sum ", resources[2][0],"/",resources[2][1], " Estado: ", checkPrerequisites, "SupplyLeft: ", supplyLeft)
        
        #Se verifica que tenga los recursos suficientes para construir el vertice y que cumpla con los prerrequisitos
        if(checkPrerequisites and resources[0] >= techTree.vs[nodeToBuild]["minerals"] and resources[1] >= techTree.vs[nodeToBuild]["gas"] and supplyLeft >= techTree.vs[nodeToBuild]["supply"]):
            #Se agrega a la cola de construcción de unidad/tecnología
            if(techTree.vs[nodeToBuild]["type"] != "Building"):
                #Si el nodo a construir no es un Archon
                if(nodeToBuild != 28):
                    index = 0
                    selectedIndex = 100
                    lenBuildingQueue = 0
                    minBuildingQueue = 5
                    while(index < len(unitQueue)):
                        building = unitQueue[index]
                        buildOn = techTree.vs[nodeToBuild]["buildOn"]
                        if(building[0] == techTree.vs[buildOn]["name"]):
                            lenBuildingQueue = len(building[1])
                            if(lenBuildingQueue < minBuildingQueue):
                                minBuildingQueue = lenBuildingQueue
                                selectedIndex = index
                        index+=1
                    if(selectedIndex != 100):
                        if(applyChrono == True):
                            unitQueue[indexNexus][5]-=50
                            unitQueue[selectedIndex][4] = 20
                        unitQueue[selectedIndex][1].append(techTree.vs[nodeToBuild]["code"])
                        unitQueue[selectedIndex][2].append(techTree.vs[nodeToBuild]["gameSpeed"])
                        if(applyChrono == True):
                            brotherBuildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(brotherNodeQty), deepcopy(unitQueue), deepcopy(archonQueue), "Chronoboost"])
                        else:
                            brotherBuildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(brotherNodeQty), deepcopy(unitQueue), deepcopy(archonQueue), ""])
                    # for building in unitQueue:
                    #     buildOn = techTree.vs[nodeToBuild]["buildOn"]
                    #     if(building[0] == techTree.vs[buildOn]["name"] and allocated == False):
                    #         if(len(building[1]) < 5):
                    #             building[1].append(techTree.vs[nodeToBuild]["code"])
                    #             building[2].append(techTree.vs[nodeToBuild]["gameSpeed"])
                    #             allocated = True
                    #             brotherBuildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(brotherNodeQty), deepcopy(unitQueue), deepcopy(archonQueue)])

                else:
                    #Se añade Archon a cola de producción y se restan templarios
                    if(brotherNodeQty[26][1] >= 2):
                        brotherNodeQty[26][1] -= 2
                        archonQueue.append([techTree.vs[nodeToBuild]["name"], 1, techTree.vs[nodeToBuild]["gameSpeed"]])
                        brotherBuildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(brotherNodeQty), deepcopy(unitQueue), deepcopy(archonQueue), ""])

                    elif(brotherNodeQty[27][1] >= 2):
                        brotherNodeQty[27][1] -= 2
                        archonQueue.append([techTree.vs[nodeToBuild]["name"], 1, techTree.vs[nodeToBuild]["gameSpeed"]])
                        brotherBuildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(brotherNodeQty), deepcopy(unitQueue), deepcopy(archonQueue), ""])
                if(brotherNodeQty[entityId][1] == entityQty or time >= maxTime or resources[2][0] >= 200):
                    nextTic = False
                    brotherBuildOrder[-1][7] = brotherNodeQty
                else: 
                    time += 1
             
            else: 
                #Se agrega a la cola de construcción de edificios
                constructionQueue.append([nodeToBuild, techTree.vs[nodeToBuild]["gameSpeed"]])
                resources[0] = resources[0] - techTree.vs[nodeToBuild]["minerals"]
                resources[1] = resources[1] - techTree.vs[nodeToBuild]["gas"]
                brotherBuildOrder.append([time, techTree.vs[nodeToBuild]["name"], resources[2][0], resources[2][1], int(resources[0]), int(resources[1]), deepcopy(constructionQueue), deepcopy(brotherNodeQty), deepcopy(unitQueue), deepcopy(archonQueue), ""])
                if(brotherNodeQty[entityId][1] == entityQty or time >= maxTime or resources[2][0] >= 200):
                    nextTic = False
                    brotherBuildOrder[-1][7] = brotherNodeQty
                else: 
                    time += 1

            #### unitQueueToAdd = deepcopy(unitQueue)
            #Se agrega al build order en el tiempo en que se ejecuta la acción de empezar a construir el vertice
        
        #Si se logra la cantidad ingresada por el usuario se detiene la construcción
        if(brotherNodeQty[entityId][1] == entityQty or time >= maxTime or resources[2][0] >= 200):
            nextTic = False
            #Esta asignación se realiza ya que existen casos en que al no agregar nada al orden de costrucción, no se actualiza nodeQty y
            #Y en vez de las X unidades completadas mostraría X-1 unidades completadas.
            brotherBuildOrder[-1][7] = brotherNodeQty
        else: 
            time += 1
    return brotherBuildOrder

#Al activar el warp gate se disminuyen los tiempos de construcción de las unidades
#Para este efecto, se asume que el jugador seleccionará un pylon cercano a un nexus o a un warp gate
#para transposicionar sus unidades ya que de lo contrario el tiempo no sería 5 seg, sino que de 16 seg.
def applyWarpGate(techTree):
    techTree.vs[16]["gameSpeed"] = 5
    techTree.vs[17]["gameSpeed"] = 5
    techTree.vs[18]["gameSpeed"] = 5
    techTree.vs[19]["gameSpeed"] = 5
    techTree.vs[26]["gameSpeed"] = 5
    techTree.vs[27]["gameSpeed"] = 5

#Entrega un puntaje a la orden de construcción basado en el tiempo logrado y en las unidades restantes por construir
def scoreBuildOrder(techTree, buildOrder, entityId, entityQty, maxTime, minTime):
    time = buildOrder[-1][0]
    nodeQty = buildOrder[-1][7]
    #Se calcula el path desde el nodo inicial
    if(entityId != 31 and entityId != 15):
        pathToNode = getPath(techTree, "Pylon", techTree.vs[entityId]["name"])
    if(entityId == 31 or entityId == 15):
        pathToNode = getPath(techTree, "Nexus", techTree.vs[entityId]["name"])
    entitiesToBuild = len(pathToNode[0]) + entityQty - 1#Son las entidades que se deben construir incluyendo prerrequisitos
    objEntities = len(pathToNode[0]) + entityQty - 1 #Entidades objetivo por construir
    entitiesBuilt = nodeQty[entityId][1] #Son las entidades solicitadas totales que ya fueron construidas
    for node in pathToNode[0]:
        if(nodeQty[node][1] >= 1):
            entitiesToBuild-=1 #Se restan los prerrequisitos si es que ya existen
        if(nodeQty[node][1]>=1 and node != entityId):
            entitiesBuilt+=1
    entitiesToBuild-=nodeQty[entityId][1] #Se restan las entidades solicitadas que ya fueron construidas
    #Se calcula el bonus por cantidad de unidades construidas en total
    #Mientras mas cercano a 200 unidades, mas bonus obtiene
    totalUnits = 0
    index = 0
    while(index < len(nodeQty)):
        if(techTree.vs[index]["type"] == "Unit"):
            totalUnits += nodeQty[index][1]
        index+=1

    score = 0.2 * (timeRate(time, maxTime, minTime)) + 0.8 * ((objEntities - entitiesBuilt)/objEntities)
    
    # if(entitiesToBuild > 0 and maxTime != minTime):
    #     score = (0.20*(timeRate(time, maxTime, minTime)) + 0.80*((objEntities - entitiesBuilt)/objEntities))
    # if(entitiesToBuild <= 0 and maxTime != minTime):
    #     score = (0.2*(timeRate(time, maxTime, minTime)))
    # if(entitiesToBuild > 0 and maxTime == minTime):
    #     score = (0.75*(entitiesToBuild/objEntities))
    # if(entitiesToBuild <= 0 and maxTime == minTime):
    #     score = (0.75*(entitiesToBuild/objEntities))
    # if(entitiesToBuild <= objEntities and maxTime == minTime):
    #     score = 0
    result = [time, maxTime, entitiesBuilt, entitiesToBuild, entityQty, score]
    return(result)

def timeRate(time, maxTime, minTime):
    if(maxTime <= minTime):
        result = 1
    else:
        result = (time-minTime)/(maxTime-minTime)
    return result

def printBuildOrder(buildOrder):
    print("")
    print("Tiempo | Unidad | Suministros | Minerales | Vespeno | Chronoboost")
    for element in buildOrder:
        #print(element[0], " | ", element[1], " | ", element[2], "/", element[3], " | ", element[4], " | ", element[5])
        print(str(datetime.timedelta(seconds=element[0])), " | ", element[1], " | ", element[2], "/", element[3], " | ", element[4], " | ", element[5], " | ", element[10])
    print("")

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')