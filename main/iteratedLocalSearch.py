import xlsxwriter
from techTree import *
import argparse
import logging
import sys
import os
import datetime
from buildOrder import *
from copy import deepcopy

#Algoritmo de búsqueda local iterada
def iteratedLocalSearch(techTree, entityId, entityQty, maxTime, perturbations, iterations, iterationsILS, exportXls, test, testNumber, experiment):
    #Se crea el directorio para guardar los resultados
    if(exportXls == 1):

        if(test == 0):
            parent_dir = "/home/andres/ProyectoTitulacion/main/results"
            directory = "results_" + str(entityId) + "_" + str(entityQty) + "_" + str(maxTime)
        if(test == 1):
            parent_dir = "/home/andres/ProyectoTitulacion/main/results/test_" + str(testNumber)
            if(not(os.path.exists(parent_dir))):
                os.mkdir(parent_dir)
            directory = "results_" + str(entityId) + "_" + str(entityQty) + "_" + str(maxTime) + "_TEST" + str(experiment)
            # Path
        # Parent Directory path

        path = os.path.join(parent_dir, directory)

        os.mkdir(path)
    
    #Se obtiene una orden de construcción aleatoria y se aplica una busqueda local
    buildOrder = getRandomBuildOrder(techTree, entityId, entityQty, maxTime)
    bestSolution = greedy(techTree, deepcopy(buildOrder), entityId, entityQty, maxTime, perturbations, iterations, 0, testNumber, experiment)
    bestScore = scoreBuildOrder(techTree, deepcopy(bestSolution[0]), entityId, entityQty, maxTime, 0)
    genResults = [["Generación", "Puntaje", "Tiempo", "Entidades construidas"]]
    iteration = 1
    progress = 0
    cls()
    print("Calculando, por favor espere...")
    if(test == 1):
        print("Progreso: ", progress, "%", " | Test N°: ", testNumber + 1, " | Experimento N°: ", experiment + 1)
    else:
        print("Progreso: ", progress, "%")
    #En cada iteración se perturba la solución inicial y se aplica otra búsqueda local
    while(iteration <= iterationsILS):
        cls()
        print("Calculando, por favor espere...")
        if(test == 1):
            print("Progreso: ", progress, "%", " | Test N°: ", testNumber + 1, " | Experimento N°: ", experiment + 1)
        else:
            print("Progreso: ", progress, "%")
        perturbatedSolution = perturbationFunction(deepcopy(bestSolution[0]), techTree, entityId, entityQty, maxTime)
        localSolution = greedy(techTree, deepcopy(perturbatedSolution), entityId, entityQty, maxTime, perturbations, iterations, test, testNumber, experiment)
        score = scoreBuildOrder(techTree, localSolution[0], entityId, entityQty, bestSolution[0][-1][0], 0)
        genResults.append([iteration, score[-1], localSolution[0][-1][0], localSolution[0][-1][7][entityId][1]])
        #Si el puntaje es mejor, se considera que la solución local es la solución inicial
        if(localSolution[0][-1][0] < bestSolution[0][-1][0] and localSolution[0][-1][7][entityId][1] >= bestSolution[0][-1][7][entityId][1]):
            bestSolution = [deepcopy(localSolution[0]), score]
            bestScore = score
        progress = (iteration/iterationsILS)*100
        iteration+=1

    result = [deepcopy(bestSolution), bestScore]

    cls()
    print("- Completado -")
    if(exportXls == 1):
        #Se crea el directorio para guardar los resultados
        if(test == 0):
            parent_dir = "/home/andres/ProyectoTitulacion/main/results"
            directory = "results_" + str(entityId) + "_" + str(entityQty) + "_" + str(maxTime)
        if(test == 1):
            parent_dir = "/home/andres/ProyectoTitulacion/main/results/test_" + str(testNumber)
            if(not(os.path.exists(parent_dir))):
                os.mkdir(parent_dir)
            directory = "results_" + str(entityId) + "_" + str(entityQty) + "_" + str(maxTime) + "_TEST" + str(experiment)
        # Path
        # Parent Directory path
        path = os.path.join(parent_dir, directory)
        if(not(os.path.exists(path))):
            os.mkdir(path)

        with xlsxwriter.Workbook(path + '/' +'Generations_Scores.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for row_num, data in enumerate(genResults):
                worksheet.write_row(row_num, 0, data)
        
        cleanResult = [["Time", "Entity", "Supply Occupied", "Total Supply", "Minerals", "Vespene", "Chronoboost"]]
        for row in result[0][0]:
            cleanResult.append([str(datetime.timedelta(seconds=row[0])), row[1], row[2], row[3], row[4], row[5], row[10]])

        with xlsxwriter.Workbook(path + '/' 'Build_Order.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for row_num, data in enumerate(cleanResult):
                worksheet.write_row(row_num, 0, data)
        
        entitiesBuilt = deepcopy(result[0][0][-1][7])
        with xlsxwriter.Workbook(path + '/' 'Entities_Built.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for row_num, data in enumerate(entitiesBuilt):
                worksheet.write_row(row_num, 0, data)
        
        unitQueue = deepcopy(result[0][0][-1][8])
        resultUnitQueue = [["building", "units being built", "time left"]]
        for building in unitQueue:
            resultUnitQueue.append([building[0], ', '.join([str(item) for item in building[1]]), ',  '.join([str(item) for item in building[2]])])
        
        with xlsxwriter.Workbook(path + '/' 'Unit_Queue.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for row_num, data in enumerate(resultUnitQueue):
                worksheet.write_row(row_num, 0, data)

        archonQueue = deepcopy(result[0][0][-1][9])
        resultArchonQueue = [["Archon", "Qty", "Time left"]]
        for archon in archonQueue:
            resultArchonQueue.append([archon[0], archon[1], archon[2]])
        with xlsxwriter.Workbook(path + '/' 'Archon_Queue.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for row_num, data in enumerate(resultArchonQueue):
                worksheet.write_row(row_num, 0, data)

    return result

#Algoritmo Greedy, genera una solución después de muchas perturbaciones e iteraciones.
def greedy(techTree, buildOrder, entityId, entityQty, maxTime, perturbations, iterations, test, testNumber, experiment):
    bestSolution = deepcopy(buildOrder)
    bestScore = [1]
    iteration = 1
    greedyResults = [["iteracion", "perturbaciones", "tiempo", "entidades"]]
    progress = 0
    while(iteration <= iterations):
        if(test == 1):
            cls()
            print("progreso: ", progress, "%", " Test N°: ", testNumber + 1, " Experimento N°: ", experiment + 1)
        minTimeOfGen = 0
        maxTimeOfGen = 0
        perturbation = 1
        perturbedSolutions = []
        while(perturbation <= perturbations):
            perturbedSolution = perturbationFunction(deepcopy(bestSolution), techTree, entityId, entityQty, minTimeOfGen)
            perturbedSolutions.append(perturbedSolution)
            if(minTimeOfGen == 0):
                minTimeOfGen = perturbedSolution[-1][0]
            elif(minTimeOfGen > perturbedSolution[-1][0]):
                minTimeOfGen = perturbedSolution[-1][0]
            if(perturbedSolution[-1][0] > maxTimeOfGen):
                maxTimeOfGen = perturbedSolution[-1][0]
            perturbation+=1
        for solution in perturbedSolutions:
            newScore = scoreBuildOrder(techTree, deepcopy(solution), entityId, entityQty, maxTimeOfGen, minTimeOfGen)
            if(newScore[-1] < bestScore[-1]):
                bestScore = newScore
                bestSolution = deepcopy(solution)
            greedyResults.append([iteration, perturbations, solution[-1][0], solution[-1][7][entityId][1]])
        iteration+=1
        progress = (iteration/iterations)*100
    greedyResults.append(["Qty", "Best time", "Best score", ""])
    greedyResults.append([bestSolution[-1][7][entityId][1] , bestSolution[-1][0], bestScore[5], ""])
    if(test == 1):
        parent_dir = "/home/andres/ProyectoTitulacion/main/results/"
        directory = "test_" + str(testNumber) + "/results_" + str(entityId) + "_" + str(entityQty) + "_" + str(maxTime) + "_TEST" + str(experiment)
        # Parent Directory path
        path = os.path.join(parent_dir, directory)

        with xlsxwriter.Workbook(path + '/Greedy_results_test' + str(testNumber) + '_exp' + str(experiment) + '.xlsx') as workbook:
                worksheet = workbook.add_worksheet()

                for row_num, data in enumerate(greedyResults):
                    worksheet.write_row(row_num, 0, data)

    return [bestSolution, bestScore]

def obtainTests(techTree):
    test = 0
    #Entity initial Zealot
    entityId = 16
    qtyObj = 5
    timeObj = 1000
    results = [[], [], []]
    while(test<3):
        if(test == 1):
            #Dark Templar
            entityId = 27
            qtyObj = 5
            timeObj = 10000
        if(test == 2):
            #Phoenix
            entityId = 20
            qtyObj = 5
            timeObj = 10000
        experiment = 0
        while(experiment < 11):
            results[test].append(iteratedLocalSearch(techTree, entityId, qtyObj, timeObj, 21, 20, 11, 1, 1, test, experiment))
            experiment+=1
        test+=1
    return results

def obtainTestsGreedy(techTree):
    test = 0
    #Entity initial Zealot
    entityId = 16
    qtyObj = 5
    timeObj = 1000
    results = [[], [], []]
    while(test<3):
        if(test == 1):
            #Dark Templar
            entityId = 27
            qtyObj = 5
            timeObj = 10000
        if(test == 2):
            #Phoenix
            entityId = 20
            qtyObj = 5
            timeObj = 10000
        experiment = 0
        buildOrder = getRandomBuildOrder(techTree, entityId, qtyObj, timeObj)
        while(experiment < 11):
            results[test].append(greedy(techTree, buildOrder, entityId, qtyObj, timeObj, 25, 20, 1, test, experiment))
            experiment+=1
        test+=1
    return results


#Esta función la ejecuta IRACE para paremetrizar los algoritmos de búsqueda local
def main(PERT, ITER, ITERILS, DATFILE):
    techTree = initTechTree()
    entityId = 16
    entityQty = 10
    maxTime = 2000
    solution = iteratedLocalSearch(techTree, entityId, entityQty, maxTime, PERT, ITER, ITERILS, 0)
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