
# here the  first method of Investigating the Normalization Procedure of NSGA-III is implemented https://doi.org/10.1007/978-3-030-12598-1_19 
#  if you prefer the other methods can implement the others too 
def normalize(sortedPop,pop):
    eps = 1e-4
    nadirPoint = [0] * len(sortedPop[0][0]) 
    idealPoint = [0] * len(sortedPop[0][0]) 
    flag = 1
    for s in sortedPop[0]:
        i = 0
        while i < len(s):
            if nadirPoint[i] < s[i] or flag == 1:
                nadirPoint[i] = s[i]
            i += 1
        flag = 0

    i = 0
    flag1 = [1] * len(sortedPop[0][0]) 

    while i < len(sortedPop[i]):
        j = 0
        while j < len(sortedPop[i][j]) or flag1[j] == 1:
            if idealPoint[i] > sortedPop[i][j] or flag1[j] == 1:
                idealPoint = sortedPop[i][j]
                flag1[j] = 0
            
            j += 1

        flag = 0
        j = 0
        flag2 = True
        while j < len(idealPoint): 
            if nadirPoint - idealPoint < eps:
                flag[i] = 1
                flag2 = False

        if flag2 :
            break

        i += 1 

        
    i = 0 
    while i < len(pop):
        j = 0
        while j < len(pop[0]):
            pop[i][j] = pop[i][j] - idealPoint[j] / nadirPoint[j] - idealPoint[j] 
            j += 1   

        i += 1





