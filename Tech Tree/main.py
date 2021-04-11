import igraph as ig


# Para usar igraph es necesario instalarlo con "pip install python-igraph"

def createTechTree():
    techTree = ig.Graph()
    techTree.add_vertices(15)  # 15 buildings in Protoss Tech Tree
    techTree.add_edges(
        [(0, 3), (0, 4), (3, 5), (4, 6), (5, 7), (5, 8), (5, 9), (5, 10), (8, 11), (8, 12), (9, 13), (10, 14)])
    techTree.vs["name"] = ["Nexus", "Assimilator", "Pylon", "Gateway", "Forge", "Cibernetics Core", "Photon Cannon",
                           "Shield Battery", "Twilight Council", "Stargate", "Robotics Facility", "Templar Archives",
                           "Dark Shrine", "Fleet Beacon", "Robotics Bay"]
    techTree.vs["label"] = techTree.vs["name"]
    techTree.vs["code"] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    techTree.vs["minerals"] = [400, 75, 100, 150, 150, 150, 150, 100, 150, 150, 150, 150, 150, 300, 150]
    techTree.vs["gas"] = [0, 0, 0, 0, 0, 0, 0, 0, 100, 150, 100, 200, 150, 200, 150]
    techTree.vs["gameSpeed"] = [71, 21, 18, 46, 32, 36, 29, 29, 36, 43, 46, 36, 71, 43, 46]
    techTree.vs["initialEnergy"] = [50, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0]
    techTree.vs["maxEnergy"] = [200, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0]
    techTree.vs["unlocks"] = [[3, 4], [], [], [5], [6], [7, 8, 9, 10], [], [], [11, 12], [13], [14], [], [], [], []]
    return techTree


def showBuildingsInfo(techTree):
    i = 0
    while i < 15:
        print("Name: {}".format(techTree.vs[i]["name"]))
        print("    code: {}".format(techTree.vs[i]["code"]))
        print("    minerals: {}".format(techTree.vs[i]["minerals"]))
        print("    gas: {}".format(techTree.vs[i]["gas"]))
        print("    gameSpeed: {}".format(techTree.vs[i]["gameSpeed"]))
        print("    initialEnergy: {}".format(techTree.vs[i]["initialEnergy"]))
        print("    maxEnergy: {}".format(techTree.vs[i]["maxEnergy"]))
        print("    unlocks: {}".format(techTree.vs[i]["unlocks"]))
        i += 1


def showGraph(graph):
    layout = graph.layout_reingold_tilford(root=0)
    ig.plot(graph, layout=layout, bbox=(600, 600), margin=60)


def main():
    print("Edificios: ")
    print("")
    techTree = createTechTree()
    showBuildingsInfo(techTree)
    print("")
    print("Grafo:")
    print("")
    print(techTree)
    showGraph(techTree)


main()
