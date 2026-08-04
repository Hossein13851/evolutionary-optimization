import math
import numpy as np
import random

class wVectorn:
    def __init__(self,wVector1,solution,PBIS):
        self.wVector1 = wVector1
        self.solution = solution
        self.neighbors = []
        self.PBIS = PBIS

    def setSolution(self,solution):
        self.solution = solution

    def setNeighbor(self,wVector1):
        self.neighbors.append(wVector1)

# This function depends on your problem
def objFunction(solution):
    pass

# This function depends on your problem 
def generatePop():
    pass 

#polynomial mutation  
def mutation(x,lb,ub):


    n = x.copy()
    delta = 0
    nm = 15
    child = []
    
    u = random.random()
    if u <= 0.5:
        delta = (2*u) ** (1 / (nm + 1))
    else :
        delta = 1 - ((2*(1-u)) ** (1 / (1 + nm) ))
    i = 0
    while(i<len(n)):
        n[i] += delta * (ub - lb)
        child = n

    return child

def arithmeticCrossover(parent1, parent2, alpha=None):
    if alpha is None:
        alpha = np.random.uniform(0, 1)   
    child = alpha * parent1 + (1 - alpha) * parent2
    return child

# I implement penalty-based boundary for evaluate the solutions but you can implement the others like Tchebycheff or others
def PBI(wVector,idealP,solution, theta):
    i = 0
    wVector = np.array(wVector)
    idealP = np.array(idealP)
    solution = np.array(solution)
    lenwvector = math.sqrt(np.dot(wVector,wVector)) 
    lengthIdealPP = np.dot(wVector,idealP) / lenwvector

    lengthSP = np.dot(wVector,solution) / lenwvector

    d1 = lengthSP - lengthIdealPP 

    vectorI = (np.array(wVector) / lenwvector) * lengthIdealPP
    vec1 = vectorI - idealP 
    vectorII = (np.array(wVector) / lenwvector) * lengthSP
    vec2 = vectorII - solution
    perp = vec1 - vec2
    d2 = math.sqrt(np.dot(perp, perp))

    d = d1 + theta * d2

    return d
    
def dominanceCheck(a,b):
    return np.all(a >= b) and np.any(a > b) 

def nonDomnanceSet(pop):
    for i in  range(len(pop)):
        for j in range(len(pop)):
            if i != j  and dominanceCheck(pop[j],pop[i]):
                break
            elif j == (len(pop) -1 ) :
                EP = np.append(EP , pop[i]) 
    return EP


def findneighbors(wVectors,numNeighbors):
    i = 0 
    
    while i < len(wVectors):
        distanceV = []
        j = 0 
        while j < len(wVectors):
            x = np.dot(wVectors[i].wVector1,wVectors[j].wVector1)
            y =math.sqrt(np.dot(wVectors[j].wVector1,wVectors[j].wVector1))
            v =((x / y) * (wVectors[j].wVector1 / y)) - wVectors[i].wVector1
            dist = math.sqrt(abs(np.dot(v,v))) 
            distanceV.append(dist)
            j += 1
        
        k = 0
        while (k < numNeighbors):
            n = 0
            min = float('inf')
            flag = True
            j = 0
            while j < len(distanceV):
                if distanceV[j] < min or flag:
                    min = distanceV[j]
                    n = j
                    flag = False

                j += 1
            wVectors[i].setNeighbor(wVectors[n])
            distanceV.pop(n)

            k += 1

        
        i += 1


def findIdealPoint(EP):
    i = 0
    z = [0] * len(EP[0])
    flag = True
    while i < len(EP):
        j = 0
        while j < len(EP[0]):
            if EP[i][j] > z[j] or flag:
                z[j] = EP[i][j]
            j += 1

        i += 1
    return z



def updateSolution(wVector,solution):
    i = 0
    if dominanceCheck(solution , wVector.solution ):
        wVector.solution = solution
    else :
        while i < len(wVector.neighbors):
                if dominanceCheck(solution ,wVector.neighbors[i].solution):
                    wVector.solution = solution
                    break
                i += 1 


def MOEA_D(pop,wVectors , numIteration, numNeighbors,CR,MR):

    wVectors = np.array(wVectors)
    pop = np.array(pop)
    EP = []
    arrWVectors = []
    popValue = []
    
    i = 0    
    while i < len(pop):
        popValue.append(objFunction(pop[i]))
        i += 1
    popValue = np.array(popValue)
    EP = nonDomnanceSet(popValue)
    idealpoint = findIdealPoint(EP)
    i = 0
    while i < len(wVectors):
        arrWVectors.append(wVectorn(wVectors[i],popValue[i],PBI(wVectors[i],idealpoint,popValue[i],0.7)))
        i += 1

    findneighbors(arrWVectors,numNeighbors)

    i = 0  
    while i < numIteration:
        j = 0 
        while j < len(pop):
            n = np.random.randint(0 ,numNeighbors - 1)
            m = np.random.randint(0 ,numNeighbors  - 1)
            prob = np.random.rand()
            if prob < CR :
                newSolution = objFunction(arithmeticCrossover(arrWVectors[j].neighbors[n].solution,arrWVectors[j].neighbors[m].solution))
                
                k = 0 
                while k < len(idealpoint):
                    if idealpoint [k] < newSolution[k]:
                        idealpoint[k] = newSolution[k]

                    k += 1


                k = 0 
                while k < numNeighbors:
                    PBVs = PBI(arrWVectors[j].neighbors[k].wVector1,idealpoint,newSolution,0.7)
                    if PBVs < arrWVectors[j].neighbors[k].PBIS:
                        arrWVectors[j].neighbors[k].PBIS = PBVs
                        arrWVectors[j].neighbors[k].solution = newSolution
                        break

                k = 0 
                dom = 0
                while k < len(EP):
                    if dominanceCheck(newSolution,EP[k]):
                        EP.pop(k)
                    if dominanceCheck(EP[k] , newSolution):
                        dom += 1
                    k += 1

                if  dom == 0:
                    EP.append(newSolution)

            j += 1

        i += 1

                    


        
