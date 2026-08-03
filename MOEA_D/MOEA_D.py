import math
import numpy as np

# This function depends on your your problem
def objFunction():
    pass


# This function depends on your your problem 
def generatePop():
    pass 


# I implement penalty-based boundary for evaluate the solutions but you can implement the others like Tchebycheff or others
def PBI(wVector,idealP,solution, theta):
    i = 0
    wVector = np.array(wVector)
    idealP = np.array(idealP)
    solution = np.array(solution)
    sqlenwvector = math.sqrt(np.dot(wVector,wVector)) 
    lengthIdealPP = np.dot(wVector,idealP) / sqlenwvector

    

    lengthSP = np.dot(wVector,solution) / sqlenwvector

    d1 = lengthSP - lengthIdealPP 

    vectorI = (np.array(wVector) / sqlenwvector) * lengthIdealPP
    vec1 = vectorI - idealP 
    vectorII = (np.array(wVector) / sqlenwvector) * lengthSP
    vec2 = vectorII - solution
    perp = vec1 - vec2
    d2 = math.sqrt(np.dot(perp, perp))

    d = d1 + theta * d2


    return d


    
def dominance_check(a,b):
    return np.all(a <= b) and np.any(a < b) 

def nonDomnanceSet(pop):
    for i in  range(len(pop)):
        for j in range(len(pop)):
            if i != j  and dominance_check(pop[j],pop[i]):
                break
            elif j == (len(pop) -1 ) :
                EP = np.append(EP , pop[i]) 

    return EP

def findneighbors():
    pass

def findIdealPoint():
    pass

def updateSolution():
    pass

def MOEA_D():
    pass