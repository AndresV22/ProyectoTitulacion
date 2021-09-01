import xlsxwriter
from techTree import *
import argparse
import logging
import sys
import datetime
from buildOrder import *

#Algoritmo de búsqueda local iterada
def iteratedLocalSearch(techTree, entityId, entityQty, maxTime, perturbations, iterations, iterationsILS, exportXls):
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

    cls()
    print("- Completado -")
    if(exportXls == 1):
        with xlsxwriter.Workbook('results/genScores.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for row_num, data in enumerate(genScores):
                worksheet.write_row(row_num, 0, data)
        
        cleanResult = [["Time", "Entity", "Supply Occupied", "Total Supply", "Minerals", "Vespene"]]
        for row in result:
            cleanResult.append([str(datetime.timedelta(seconds=row[0])), row[1], row[2], row[3], row[4], row[5]])

        with xlsxwriter.Workbook('results/BuildOrder_Solution.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for row_num, data in enumerate(cleanResult):
                worksheet.write_row(row_num, 0, data)
        
        entitiesBuilt = list(result[-1][-1])
        
        with xlsxwriter.Workbook('results/EntitiesBuilt.xlsx') as workbook:
            worksheet = workbook.add_worksheet()

            for row_num, data in enumerate(entitiesBuilt):
                worksheet.write_row(row_num, 0, data)

    return result

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