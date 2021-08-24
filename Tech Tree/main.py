import igraph as ig
import os
import sys
import random
import copy

# Para usar igraph es necesario instalarlo con "pip install python-igraph"

#Funcion que crea el árbol de tecnologías.
def initTechTree():
    techTree = ig.Graph(directed=True)
    techTree.add_vertices(61)  # 15 buildings in Protoss Tech Tree
    techTree.add_edges(
        [(0, 3), (0, 4), (3, 5), (4, 6), (5, 7), (5, 8), (5, 9), (5, 10), (8, 11), (8, 12), (9, 13), (10, 14), (0, 15), (3, 16), (5, 17), (5, 18), (5, 19), (9, 20), (9, 21), (9, 22), (10, 23), (10, 24), (10, 25), (11, 26), (12, 27), (11, 28), (13, 29), (13, 30), (13, 31), (14, 32), (14, 33), (4, 34), (8, 35), (8, 36), (4, 37), (8, 38), (8, 39), (4, 40), (8, 41), (8, 42), (5, 43), (13, 44), (13, 45), (5, 46), (13, 47), (13, 48), (5, 49), (11, 50), (12, 51), (13, 52), (13, 53), (13, 54), (14, 55), (14, 56), (14, 57), (8, 58), (8, 59), (8, 60)])
    techTree.vs["name"] = ["Nexus", "Assimilator", "Pylon", "Gateway", "Forge", "Cibernetics Core", "Photon Cannon",
                           "Shield Battery", "Twilight Council", "Stargate", "Robotics Facility", "Templar Archives",
                           "Dark Shrine", "Fleet Beacon", "Robotics Bay", "Probe", "Zealot", "Stalker", "Sentry",
                           "Adept", "Phoenix", "Oracle", "Void Ray", "Observer", "Warp Prism", "Immortal",
                           "High Templar", "Dark Templar", "Archon", "Tempest", "Carrier", "Mothership", "Colossus",
                           "Disruptor", "Ground Weapons 1", "Ground Weapons 2", "Ground Weapons 3", "Ground Armor 1",
                           "Ground Armor 2", "Ground Armor 3", "Shield Upgrades 1", "Shield Upgrades 2", "Shield Upgrades 3",
                           "Air Weapons 1", "Air Weapons 2", "Air Weapons 3", "Air Armor 1", "Air Armor 2", "Air Armor 3",
                           "Warp Gate", "Psionic Storm", "Shadow Stride", "Anion Pulse-Crystals", "Flux Vanes", "Tectonic Destabilizers",
                           "Gravitic Boosters", "Gravitic Drive", "Extended Thermal Lance", "Charge", "Blink", "Resonating Glaives"]
    techTree.vs["label"] = techTree.vs["name"]
    techTree.vs["code"] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                           31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    techTree.vs["minerals"] = [400, 75, 100, 150, 150, 150, 150, 100, 150, 150, 150, 150, 150, 300, 150, 50, 100, 125, 50, 100, 150, 150, 200, 25,
                               250, 275, 50, 125, 0, 250, 350, 400, 300, 1150, 100, 150, 200, 100, 150, 200, 150, 225, 300, 100, 175, 250, 150,
                               225, 300, 50, 200, 100, 150, 150, 150, 100, 100, 150, 100, 150, 100]
    techTree.vs["gas"] = [0, 0, 0, 0, 0, 0, 0, 0, 100, 150, 100, 200, 150, 200, 150, 0, 0, 50, 100, 25, 100, 150, 150, 75, 0, 100, 150, 125, 0,
                          175, 250, 400, 200, 150, 100, 150, 200, 100, 150, 200, 150, 225, 300, 100, 175, 250, 150, 225, 300, 50, 200, 100, 150,
                          150, 150, 100, 100, 150, 100, 150, 100]
    techTree.vs["gameSpeed"] = [71, 21, 18, 46, 32, 36, 29, 29, 36, 43, 46, 36, 71, 43, 46, 12, 27, 30, 26, 30, 25, 37, 37, 21, 36, 39, 39, 39, 8.67, 43,
                                64, 114, 54, 36, 129, 154, 179, 129, 154, 179, 129, 154, 179, 129, 154, 179, 129, 154, 179, 160, 79, 100, 64, 80, 100, 57, 57, 100, 100, 121, 100]
    techTree.vs["initialEnergy"] = [
        50, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    techTree.vs["maxEnergy"] = [200, 0, 0,
                                0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    techTree.vs["supply"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 1, 2, 2, 2, 2, 2, 3, 4, 1, 2, 4, 2, 2, 4, 5, 6, 8, 6, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    techTree.vs["type"] = ["Building", "Building", "Building", "Building", "Building", "Building", "Building", "Building",
                           "Building", "Building", "Building", "Building", "Building", "Building", "Building", "Unit", "Unit", "Unit", "Unit", "Unit", "Unit", "Unit", "Unit",
                           "Unit", "Unit", "Unit", "Unit", "Unit", "Unit", "Unit", "Unit", "Unit", "Unit", "Unit", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech",
                           "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech", "Tech"]
    return techTree

#Muestra la información de los vértices
def showVertexInfo(techTree):
    i = 0
    while i < 61:
        print("--- {} ---".format(techTree.vs[i]["name"]))
        print("code: {}".format(techTree.vs[i]["code"]))
        print("minerals: {}".format(techTree.vs[i]["minerals"]))
        print("gas: {}".format(techTree.vs[i]["gas"]))
        print("gameSpeed: {}".format(techTree.vs[i]["gameSpeed"]))
        print("initialEnergy: {}".format(techTree.vs[i]["initialEnergy"]))
        print("maxEnergy: {}".format(techTree.vs[i]["maxEnergy"]))
        print("supply: {}".format(techTree.vs[i]["supply"]))
        print("type: {}".format(techTree.vs[i]["type"]))
        print("")
        i += 1

#Obtiene la información de un vértice obtenido por nombre
def getVertexByName(techTree, vertexName):
    i = 0
    found = 0
    while i < 61:
        if(techTree.vs[i]["name"] == vertexName):
            print("")
            print("--- {} ---".format(techTree.vs[i]["name"]))
            print("code: {}".format(techTree.vs[i]["code"]))
            print("minerals: {}".format(techTree.vs[i]["minerals"]))
            print("gas: {}".format(techTree.vs[i]["gas"]))
            print("gameSpeed: {}".format(techTree.vs[i]["gameSpeed"]))
            print("initialEnergy: {}".format(techTree.vs[i]["initialEnergy"]))
            print("maxEnergy: {}".format(techTree.vs[i]["maxEnergy"]))
            print("supply: {}".format(techTree.vs[i]["supply"]))
            print("type: {}".format(techTree.vs[i]["type"]))
            print("")
            i = 62
            found = 1
        i += 1
    if(found == 0):
        print("No existe un vértice con ese nombre.")

#Muestra el árbol de tecnologías en una imágen
def showGraph(graph):
    layout = graph.layout_reingold_tilford(root=0)
    color_dict = {"Building": "red", "Unit": "green", "Tech": "blue"}
    visual_style = {}
    visual_style["vertex_color"] = [color_dict[type]
                                    for type in graph.vs["type"]]
    visual_style["margin"] = 20
    visual_style["layout"] = layout
    visual_style["bbox"] = (2000, 2000)
    ig.plot(graph, **visual_style)

#Imprime el camino mas corto desde un vértice de inicio a otro vértice destino
def printPath(graph, vertexFrom, vertexTo):
    # getPath(graph: grafo, vertexFrom: Vertice inicio, vertexTo: Vertice destino)
    # Retorna: Arreglo con arreglos de caminos. Ej: [[0,1,2,3], [0,2,3]]
    path = graph.get_all_shortest_paths(
        vertexFrom, to=vertexTo, weights=None, mode='out')
    print(path)

#Retorna el camino mas corto desde un vértice de inicio a otro vértice destino
def getPath(graph, vertexFrom, vertexTo):
    # getPath(graph: grafo, vertexFrom: Vertice inicio, vertexTo: Vertice destino)
    # Retorna: Arreglo con arreglos de caminos. Ej: [[0,1,2,3], [0,2,3]]
    path = graph.get_all_shortest_paths(
        vertexFrom, to=vertexTo, weights=None, mode='out')
    return(path)

#Obtiene un orden de construcción aleatorio acotado por un tiempo gameTime
def getRandomBuildOrder(techTree, entityId, entityQty, maxTime):
    print("EntityId: ", entityId, "EntityQty: ", entityQty)
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
    print("- ¿Mostrar tabla de entidades construidas? -")
    print("1: Si")
    print("2: No")
    print("")
    showQties = int(input("Ingrese una opción: "))
    if(showQties == 1):
        print("-- Tabla de unidades construidas --")
        for element in buildOrder[-1][7]:
            print(element[0], " | ", element[1])

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
    if(entitiesToBuild > 0):
        score = (0.2*((time-minTime)/(maxTime-minTime)) + 0.8*(entitiesToBuild/maxEntities))*100
    else:
        score = (0.2*((time-minTime)/(maxTime-minTime)) + 0.8)*100
    result = [[time, maxTime, entitiesBuilt, entitiesToBuild, entityQty, score]]
    return(result)

#Algoritmo Greedy, genera una solución después de muchas perturbaciones e iteraciones.
def greedy(techTree, buildOrder, entityId, entityQty, maxTime, perturbations, iterations):
    bestSolution = list(buildOrder)
    bestScore = scoreBuildOrder(techTree, buildOrder, entityId, entityQty, maxTime, 0)
    iteration = 1
    while(iteration <= iterations):
        perturbation = 1
        perturbedSolutions = []
        while(perturbation <= perturbations):
            perturbedSolutions.append(perturbationFunction(list(bestSolution), techTree, entityId, entityQty, maxTime))
            perturbation+=1
        for solution in perturbedSolutions:
            newScore = scoreBuildOrder(techTree, list(solution), entityId, entityQty, maxTime, 0)
            if(newScore > bestScore):
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
        score = scoreBuildOrder(techTree, list(localSolution), entityId, entityQty, maxTime, 0)
        #Si el puntaje es mejor, se considera que la solución local es la solución inicial
        if(score > initialScore):
            initialSolution = []
            initialSolution = list(localSolution)
        progress = (iteration/iterationsILS)*100
        iteration+=1
    result = list(initialSolution)
    return result

def showMenu(techTree):
    exit = 0
    while(exit == 0):
        cls()
        print("--------INICIO---------")
        print("")
        print("-- Menú --")
        print("1: Mostrar árbol de tecnologías Protoss")
        print("2: Ver detalles todos los vértices")
        print("3: Buscar vértice por nombre")
        print("4: Encontrar el camino más corto")
        print("5: Obtener un orden de construcción aleatorio")
        print("6: Ejecutar algoritmo greedy")
        print("7: Ejecutar algoritmo de búsqueda local iterada")
        print("8: Salir")
        print("")
        choice = input("Ingrese su elección: ")
        if(choice == "1"):
            print("")
            print("-- Mostrar árbol de tecnologías Protoss --")
            print("Cargando...")
            print("(Para volver al menú cierre la ventana de la imágen.)")
            showGraph(techTree)
        elif(choice == "2"):
            print("")
            print("-- Ver detalles de cada vértice -- ")
            print(techTree)
            showVertexInfo(techTree)
            input("Presione enter para volver al menú...")
        elif(choice == "3"):
            print("")
            print("-- Buscar vértice por nombre --")
            vertexName = input(
                "Por favor ingrese el nombre del vértice que desea buscar: ")
            getVertexByName(techTree, vertexName)
            input("Presione enter para volver al menú...")
        elif(choice == "4"):
            print("")
            print("-- Encontrar el camino más corto --")
            vertexFrom = input(
                "Ingrese el nombre del vértice de inicio: ")
            vertexTo = input("Ingrese el nombre del vértice destino: ")
            printPath(techTree, vertexFrom, vertexTo)
            input("Presione enter para volver al menú...")
        elif(choice == "5"):
            print("")
            print("-- Obtener orden de construcción aleatorio --")
            entityName = input("Ingrese el nombre de la entidad que desea obtener en el orden de construcción: ")
            success = False
            for name in techTree.vs["name"]:
                if entityName == name:
                    success = True
            if success == False:
                print("--- ERROR ---")
                print("")
                input("No existe esa entidad. Presione enter para volver al menú...")
            else:
                for id in techTree.vs["code"]:
                    if techTree.vs[id]["name"] == entityName:
                        entityId = id
                entityQty = int(input("Ingrese la cantidad que desea obtener: "))
                maxTime = int(input("Ingrese el tiempo máximo que puede tener el build order: "))
                buildOrder = getRandomBuildOrder(techTree, entityId, entityQty, maxTime)
                score = scoreBuildOrder(techTree, buildOrder, entityId, entityQty, maxTime, 0)
                printBuildOrder(buildOrder)
                print("")
                print("El puntaje de esta orden de construcción es: ", score[0][-1])
                print("Se obtuvieron ", score[0][2], "de ", score[0][4], "entidades seleccionados.")
                print("")
                perturbation = input("¿Desea aplicar la función de perturbación? (s/n): ")
                if(perturbation == 's'):
                    perturbatedBuildOrder = perturbationFunction(buildOrder, techTree, entityId, entityQty, maxTime)
                    newScore = scoreBuildOrder(techTree, perturbatedBuildOrder, entityId, entityQty, maxTime, 0)
                    printBuildOrder(perturbatedBuildOrder)   
                    print("")
                    print("El puntaje de esta orden de construcción es: ", newScore[0][-1])
                    print("Se obtuvieron ", newScore[0][2], "de ", newScore[0][4], "entidades seleccionados.")
                    print("")
                input("Presione enter para volver al menú...")
        elif(choice == "6"):
            print("")
            print("-- Ejecutar algoritmo Greedy --")
            entityName = input("Ingrese el nombre de la entidad que desea obtener en el orden de construcción: ")
            success = False
            for name in techTree.vs["name"]:
                if entityName == name:
                    success = True
            if success == False:
                print("--- ERROR ---")
                print("")
                input("No existe esa entidad. Presione enter para volver al menú...")
            else:
                for id in techTree.vs["code"]:
                    if techTree.vs[id]["name"] == entityName:
                        entityId = id
                entityQty = int(input("Ingrese la cantidad que desea obtener: "))
                maxTime = int(input("Ingrese el tiempo máximo que puede tener el build order: "))
                iterations = int(input("ingrese el número de generaciones: "))
                perturbations = int(input("Ingrese el número de perturbaciones por generación: "))
                buildOrder = getRandomBuildOrder(techTree, entityId, entityQty, maxTime)
                solution = greedy(techTree, buildOrder, entityId, entityQty, maxTime, perturbations, iterations)
                score = scoreBuildOrder(techTree, solution, entityId, entityQty, maxTime, 0)
                printBuildOrder(solution)
                print("")
                print("El puntaje de esta orden de construcción es: ", score[0][-1])
                print("Se obtuvieron ", score[0][2], "de ", score[0][4], "entidades seleccionados.")
                print("")
            input("Presione enter para volver al menú...")
        elif(choice == "7"):
            print("")
            print("-- Ejecutar algoritmo de búsqueda local iterada --")
            entityName = input("Ingrese el nombre de la entidad que desea obtener en el orden de construcción: ")
            success = False
            for name in techTree.vs["name"]:
                if entityName == name:
                    success = True
            if success == False:
                print("--- ERROR ---")
                print("")
                input("No existe esa entidad. Presione enter para volver al menú...")
            else:
                for id in techTree.vs["code"]:
                    if techTree.vs[id]["name"] == entityName:
                        entityId = id
                entityQty = int(input("Ingrese la cantidad que desea obtener: "))
                maxTime = int(input("Ingrese el tiempo máximo que puede tener el build order: "))
                iterations = int(input("ingrese el número de generaciones del algoritmo greedy: "))
                perturbations = int(input("Ingrese el número de perturbaciones por generación del algoritmo greedy: "))
                iterationsILS = int(input("Ingrese el número de iteraciones del algoritmo de búsqueda local iterada: "))
                solution = iteratedLocalSearch(techTree, entityId, entityQty, maxTime, perturbations, iterations, iterationsILS)
                score = scoreBuildOrder(techTree, solution, entityId, entityQty, maxTime, 0)
                printBuildOrder(solution)
                print("")
                print("El puntaje de esta orden de construcción es: ", score[0][-1])
                print("Se obtuvieron ", score[0][2], "de ", score[0][4], "entidades seleccionados.")
                print("")
            input("Presione enter para volver al menú...")
        elif(choice == "8"):
            print("")
            print("Cerrando programa...")
            exit = 1
        else:
            cls()
            print("--- ERROR ---")
            print("")
            input("No existe esa opción. Presione enter para volver al menú...")
    print("")
    print("---------FIN----------")


def main():
    techTree = initTechTree()
    showMenu(techTree)
    sys.exit()


main()