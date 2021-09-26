import sys
from techTree import *
from iteratedLocalSearch import *

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
                print("El puntaje de esta orden de construcción es: ", score[-1])
                print("Se obtuvieron ", score[2], "de ", score[4], "entidades seleccionados.")
                print("")
                perturbation = input("¿Desea aplicar la función de perturbación? (s/n): ")
                if(perturbation == 's' or perturbation == 'S'):
                    perturbatedBuildOrder = perturbationFunction(buildOrder, techTree, entityId, entityQty, maxTime)
                    newScore = scoreBuildOrder(techTree, perturbatedBuildOrder, entityId, entityQty, maxTime, 0)
                    printBuildOrder(perturbatedBuildOrder)   
                    print("")
                    print("El puntaje de esta orden de construcción es: ", newScore[-1])
                    print("Se obtuvieron ", newScore[2], "de ", newScore[4], " ", techTree.vs[entityId]["name"]," seleccionados.")
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
                print("El puntaje de esta orden de construcción es: ", score[-1])
                print("Se obtuvieron ", score[2], "de ", score[4], " ", entityQty, techTree.vs[entityId]["name"], " seleccionados.")
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
                maxTime = int(input("Ingrese el tiempo máximo (en segundos) del build order: "))
                default = input("¿Usar valores por default para el algoritmo de búsqueda local y de búsqueda local iterada? s/n: ")
                if(default == "s" or default == "S"):
                    iterations = 20
                    perturbations = 21
                    iterationsILS = 11
                    print("Iteraciones Búsqueda local: 20")
                    print("Perturbaciónes por iteración: 21")
                    print("Iteraciones Búsqueda local iterada: 11")
                else:
                    if(default != "n" and default != "N"):
                        print("Entrada inválida. Se usarán valores por default.")
                    iterations = int(input("ingrese el número de generaciones del algoritmo greedy: "))
                    perturbations = int(input("Ingrese el número de perturbaciones por generación del algoritmo greedy: "))
                    iterationsILS = int(input("Ingrese el número de iteraciones del algoritmo de búsqueda local iterada: "))
                cls()
                solution = iteratedLocalSearch(techTree, entityId, entityQty, maxTime, perturbations, iterations, iterationsILS, 1)
                printBuildOrder(solution[0])
                print("")
                print("Se han generado archivos .xls con los resutlados.")
                print("")
                print("El puntaje de esta orden de construcción es: ", solution[1][-1])
                print("Se obtuvieron ", solution[0][-1][7][entityId][1], "de ", entityQty, techTree.vs[entityId]["name"], " seleccionados.")
                print("Tiempo pedido: ", maxTime, " | Tiempo final: ", solution[-1][0])
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