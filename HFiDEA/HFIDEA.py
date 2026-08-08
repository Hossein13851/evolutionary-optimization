import numpy as np
import math
class refereneV:
    def __init__(self,ref):
        self.ref = ref
        self.associatedS = []
        self.distances = []


def objFunction():
    pass

def generateInitialSolutions():
    pass

def checkDominatesd(a,b):
    return np.all(a <= b) and np.any(a < b)


def selectEnvironment(pop,referenceVectors):
    S = []
    D = []
    min = math.inf
    pop = np.arrat(pop)
    referenceVectors = np.arrat(referenceVectors)

    for x in pop:
        disL = []
        min = math.inf
        for ref in referenceVectors:
            n = np.dot(ref.ref,x)
            m = np.dot(ref.ref,ref.ref)
            projX = (n / m) *  ref.ref
            distance = math.sqrt(np.dot(x -projX,x -projX))
            disL.append(distance)
            if min > distance:
                associatdV = ref
                min =distance
        associatdV.associateS.apeend(x)
        associatdV.distances.apeend(min)
        
        D.append(disL)

    for ref in referenceVectors:
        solutions = ref.associatedS
        distanceS = ref.distances
        if len(solutions) > 0:
            i = 0 
            while i < len(solutions):
                j = 0
                while j  < len(solutions):
                    if checkDominatesd (solutions[i],solutions[j]):
                        solutions.pop(i)
                        distance.pop(i)
                    j += 1
                i += 1
    min = math.inf
    i = 0
    selecredsolution = np.array([])
    while i < len(solutions):
        if min > solutions[i]:
            selecredsolution = solutions[i]
            min = distance[i]
    
    
                        

    
            
def checkStabalization():
    pass


#As the Investigating the Normalization Procedure of NSGA-III from DR.Deb mentioned the problems of finding hyperplane i implement the solution that they proposed at there  
def updateNadirP(pop):
    eps = 1e-4
    extremePoints = []
    extremePoint = [] 
    nadirP = [- math.inf] * len(pop[0])
    i = 0
    while i < len(pop[0]):
        min = math.inf
        for x in pop:
            j = 0
            while j < len(x):
                if j != i :
                    if min > x[j]:
                        min = x[j] 
                        extremePoint = x
                j += 1
        extremePoints.append(extremePoint)
        i = i + 1

    flag = True
    extremePoints = np.array(extremePoints)
    rankExtreme = np.linalg.matrix_rank(extremePoints)
    numOfRow = extremePoints.shape[0]
    i = 0
    while i < len(extremePoints):
        if extremePoints[i][i] < eps:
            flag = False
            
    if rankExtreme < numOfRow:
        flag = False

    if flag:
        ones = np.ones(extremePoints.shape[0])
        coefficients = np.linalg.solve(extremePoints, ones)
        if np.any(np.isclose(coefficients, 0)):
            print("One or more coefficients are zero. The hyperplane is parallel to an axis.")
            flag = False
        else :
            intercepts = 1.0 / coefficients
            if np.all(intercepts > 0):
                nadirP = intercepts
            else :
                flag = False    

    if flag == False:
        flag1 = 1 
        j = 0
        while j < len(pop) :
            k = 0
            while k < len(nadirP):
                if nadirP[k] < pop[i][j][k] or flag1 == 1:
                    nadirP[k] = pop[i][j][k]
            flag1 = 0
            j += 1

    return nadirP


def HFIDEA():
    pass    

