import random
import math
import normalization
# pop = population 

def creatPopulation():
    pass
    #this part depend on your self if you want you can use def create_chromosome() from initial_implementation

def objectiveFunction(population):
    #this part depend on your problem 
    pass

def sortFront(popObejectiveValue,pop):
    frontSets = []
    s = []
    i = 0
    penalty = [0] * len(popObejectiveValue)
    dominatedByMe = [[] for _ in range(len(popObejectiveValue))]

    while i < len(popObejectiveValue):
        j = 0
        dom = 0
        while j < len(popObejectiveValue):
            if popObejectiveValue[i][0] > popObejectiveValue[j][0] and popObejectiveValue[i][1] < popObejectiveValue[j][1]:
                penalty[i] = penalty[i] + 1
                dom = dom + 1
            elif popObejectiveValue[i][0] < popObejectiveValue[j][0] and popObejectiveValue[i][1] > popObejectiveValue[j][1]:
                dominatedByMe[i].append(j)
            j = j + 1

        if dom == 0:
            s.append(i)
            
        i = i + 1
    frontSets.append(s)
    i = 0
    while i < len(frontSets) and len(frontSets[i]) > 0:
        q = []
        j = 0
        while j < len(frontSets[i]):
            idx = frontSets[i][j]
            k = 0
            while k < len(dominatedByMe[idx]):
                dominated_idx = dominatedByMe[idx][k]
                penalty[dominated_idx] = penalty[dominated_idx] - 1
                if penalty[dominated_idx] == 0:
                    q.append(dominated_idx)
                k = k + 1
            j = j + 1

        i = i + 1
        if q:
            frontSets.append(q)
        else:
            break

    result = []
    for front in frontSets:
        result.append([pop[idx] for idx in front])
    return result

# you can implement any mutation you want to   
# I implement polynomial mutation  
def mutation(x,MR,lb,ub):


    a = random.random()  
    n = x.copy()
    MR = MR / 100
    delta = 0
    nm = 15
    chiild = []
    if a < MR :
        u = random.random()
        if u <= 0.5:
            delta = (2*u) ^ (1 / nm + 1)
        else :
            delta = 1 - ((2(1-u)) ^ (1 / 1 + nm ))
        i = 0
        while(i<len(n)):
            n[i] += delta * (ub - lb)

        chiild = n

    return chiild
    
# you can implement any Crossover you want to 
# I implemented SBX

def crossOver(x1,x2,CR):
    Nc = 15
    CR = CR / 100

    u = random.random()     
    a = random.random() 
    arr = []
    if a < CR:    
        if u <= 0.5:
            beta = (2 * u) ** (1 / (Nc + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (Nc + 1))
        i = 0
        arr = []
        while i <len(x1):
            y1 = 0.5 * (((1 + beta) * x1[i]) + ((1 - beta) * x2[i]))
            y2 = 0.5 * (((1 - beta) * x1[i]) + ((1 + beta) * x2[i]))
            arr.append(y1)
            arr.append(y2)
            i = i + 1

            
    
    return arr

import math

def associate(S, k, Ps, sl2, referencePo):
    
    p = [0] * len(referencePo)
    
    i = 0
    while i < len(S) - len(sl2):
        t = []
        s = S[i] 
        for ref in referencePo:  
            
            dot = sum(s[j] * ref[j] for j in range(len(s)))
            ref_norm_sq = sum(ref[j] * ref[j] for j in range(len(ref)))
            if ref_norm_sq == 0:
                continue
            factor = dot / ref_norm_sq
            proj = [factor * ref[j] for j in range(len(ref))]
            dist = math.sqrt(sum((s[j] - proj[j]) ** 2 for j in range(len(s))))
            t.append(dist)
        
       
        min_val = t[0]
        m = 0
        for j in range(1, len(t)):
            if t[j] < min_val:
                min_val = t[j]
                m = j
        p[m] += 1
        i += 1
    
    return p  

def Niching(p,k,sl):
    pass





def NSGAIII(pop,numOfIteration,referencePo):
    pass
