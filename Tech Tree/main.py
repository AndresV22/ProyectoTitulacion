import igraph as ig
import os
import sys

# Para usar igraph es necesario instalarlo con "pip install python-igraph"


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


def getPath(graph, vertexFrom, vertexTo):
    # getPath(graph: grafo, vertexFrom: Vertice inicio, vertexTo: Vertice destino)
    # Retorna: Arreglo con arreglos de caminos. Ej: [[0,1,2,3], [0,2,3]]
    print(graph.get_all_shortest_paths(
        vertexFrom, to=vertexTo, weights=None, mode='out'))


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


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
        print("5: Salir")
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
            getPath(techTree, vertexFrom, vertexTo)
            input("Presione enter para volver al menú...")
        elif(choice == "5"):
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
