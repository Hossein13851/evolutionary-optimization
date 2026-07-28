# just for first practice
# second semester code with a some changes 
# NSGA‑III implementation for a two‑objective problem
import random
import math


def create_chromosome():
    t = 0
    x = []
    while t < 100:
        i = 0
        c = []
        while i < 2:
            p = random.randint(-100,100)
            if p != 0:
                c.append(p)
                i = i + 1
            else:
                continue
            

        x.append(c)
        t += 1    
    return x


def ObjectivFunctoin(x):
    #example
    a = []
    i = 0
    j = 0
    while i < len(x):
        b = []
        b.append(1 / pow(x[i][j],2))
        a.append(b)
        i = i + 1
    i = 0
    j = 1
    while i < len(x):
        a[i].append(-pow(x[i][j],3))
        i = i + 1
    return a


def sortFront(x,st):
    frontSets = []
    s = []
    i = 0
    penalty = [0] * len(x)
    dominated_by_me = [[] for _ in range(len(x))]

    while i < len(x):
        j = 0
        dom = 0
        while j < len(x):
            if x[i][0] > x[j][0] and x[i][1] < x[j][1]:
                penalty[i] = penalty[i] + 1
                dom = dom + 1
            elif x[i][0] < x[j][0] and x[i][1] > x[j][1]:
                dominated_by_me[i].append(j)
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
            while k < len(dominated_by_me[idx]):
                dominated_idx = dominated_by_me[idx][k]
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
        result.append([st[idx] for idx in front])
    return result

def SBX(x1,x2):
    while(1):
        Nc = 15
        u = random.random()     
        if u <= 0.5:
            beta = (2 * u) ** (1 / (Nc + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (Nc + 1))
        i = 0
        arr = []
        while i <2:
            y1 = 0.5 * (((1 + beta) * x1[i]) + ((1 - beta) * x2[i]))
            y2 = 0.5 * (((1 - beta) * x1[i]) + ((1 + beta) * x2[i]))
            if y1 < 200 and y1 > -200 and y2 < 200 and y2 > -200 :
                #print(y1)
                arr.append(y1)
                arr.append(y2)
                
            else:
                #print(2)
                break

            i = i + 1
        
        if (len(arr) == 4):
            return arr

        
def normalize(S):   
    min = [110,110] 
    j = 0

    while j < len(S):
        if min[0] > S[j][0]:
            min[0] = S[j][0]
        if min[1] > S[j][1]:
            min[1] = S[j][1]
        j = j + 1
    
    S2 = [vec[:] for vec in S]
    i = 0
    j = 0

    while i < len(S):
        S2[i][0] = S2[i][0] - min[0]
        S2[i][1] = S2[i][1] - min[1] 
        i = i + 1
    
    w1 = [1,pow(10,-6)]
    w2 = [pow(10,-6),1]
    i = 0
    min1 =1000
    Zmax1 = []
    while i < len(S2):
        if S2[i][1] < min1 and S2[i][0] != 0:
            min1 = S2[i][1]
            Zmax1 = S2[i]
        i = i + 1 
    i = 0
    Zmax2 = []
    min2 = 1000
    while i < len(S2):
        if S2[i][0] < min2 and S2[i] != Zmax1 and S2[i][1] != 0:
            min2 = S2[i][0]
            Zmax2 = S2[i]
        i = i + 1 

    Z = []
    Z.append(Zmax2)
    Z.append(Zmax1)
    if Z[0][0] - Z[1][0] ==0:
        print(Z)
    a = (Z[0][1] - Z[1][1]) / ((Z[0][0] - Z[1][0]))
    a1 = Z[0][1] - (a * Z[0][0])
    a2 = ( (-1 * a1) / a )  
    i = 0
    while i < len (S2):
        S2[i][1] = S2[i][1] / a1 
        S2[i][0] = S2[i][0] / a2 
        i = i + 1

    return S2


def associate(S,k,Ps,sl2):
    j = 0
    refreencePo = [[0.2,0.8],[0.09,1],[0.4,0.6],[0.6,0.4],[0.8,0.2],[1,0]]
    a = []
    i = 0
    while i < len(refreencePo):
        a.append(refreencePo[i][1]/refreencePo[i][0])
        i = i + 1
    p = [0,0,0,0,0,0]
    
    i = 0
    while i < len(S)-len(sl2):
        t = []
        j = 0
        while j < len(a):
            t.append(abs((a[j] * S[i][0]) - S[i][1]) / math.sqrt(pow(a[j],2) + pow(1,2)))
            j = j + 1


        j = 0
        min = t[0]
        m = 0
        while j < len(t):
            if min > t[j]:
                m = j
            j = j + 1
        p[m] = p[m] + 1
        i = i + 1

  

    # Niching
    i = 0
    while i < k:
        q = 1000000
        j = 0
        while j < len(p):
            if q > p[j]:
                q = p[j]
                o = j
            j = j + 1
        j = 0
        flag = 1
        min = 0
        while j < len(sl2):
            dis = abs((a[o] * sl2[j][0]) - sl2[j][1]) / math.sqrt(pow(a[o],2) + pow(1,2))
            if dis < min or flag ==1:
                flag = 0
                min = dis
                f = j        
            j = j + 1
        
        Ps.append(sl2[f])
        sl2.pop(f)
        p[o] = p[o] + 1
        i = i + 1    
    return Ps




def NSGA3():
    P = create_chromosome()
    #print("number of iteration:  ")
    numInput = int(input("number of iteration:  "))
    n = 0
    while n < numInput:

        i = 0
        Q = []
        while i < 50:
            ran1 = random.randint(0,99)
            ran2 = random.randint(0,99)
            #print(P)
            flag = SBX(P[ran1],P[ran2]).copy()
            child1 = [flag[0], flag[2]]
            child2 = [flag[1], flag[3]]

            #print(1)
            Q.append(child1)
            Q.append(child2)
            flag = []
            i = i + 1

        Rt = []
        Rt.extend(P)
        Rt.extend(Q)
        x = ObjectivFunctoin(Rt)
        front = sortFront(x,Rt)
        i = 0 
        j = 0
        St = [] 
        #print(3)
        while len(St) < 100:
            j = 0
            while j < len(front[i]):
                St.append(front[i][j])
                j = j + 1 
            i = i + 1
        lastF = i - 1
        P = []
        if len(St) == 100:
            P = St.copy()
        else:
            i = 0
            while i < len(St) - len(front[lastF]):
                P.append(St[i])
                i = i + 1
            
            K = 100 - len(P)
            Fl = front[lastF]
            St1 = normalize(St).copy() 

            P1 = associate(St1,K,P,Fl)
            P = P1.copy()

        print(numInput)
        n =  n + 1



    return P

        


if __name__ == "__main__":
    p = NSGA3()
    print(p)