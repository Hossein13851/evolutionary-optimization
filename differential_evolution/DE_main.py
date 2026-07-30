import torch
import torch.multiprocessing as mp
import numpy as np
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def objectiveFunction(population):
    pass
    #this part depend on your self

def creatPopulation():
    pass
    #this part depend on your self if you want you can use def create_chromosome() from initial_implementation
     
def getExponentialCrossoverLength(pop_size, D, CR):
    # CR is crossover probability (e.g., 90 -> 0.9)
    p = CR / 100.0  

    i = 0
    L = []
    while i < pop_size:
        l = 1 
        while (p > torch.rand()) and (l < D):
            l += 1
        L.append(l)
    
    return L

def DE1Mutation(x):
    f = 0.1
    pop_size = len(x)
    device = x.device
    target_idx = torch.arange(pop_size, device=device)
    n1 = torch.randint(0, pop_size, (pop_size,), device=device)
    n2 = torch.randint(0, pop_size, (pop_size,), device=device)
    n3 = torch.randint(0, pop_size, (pop_size,), device=device)

    invalid = (n1 == target_idx) | (n2 == target_idx) | (n3 == target_idx)
    invalid = invalid | (n1 == n2) | (n1 == n3) | (n2 == n3)

    while invalid.any():
        idx = invalid.nonzero(as_tuple=True)[0]
        n1[idx] = torch.randint(0, pop_size, (len(idx),), device=device)
        n2[idx] = torch.randint(0, pop_size, (len(idx),), device=device)
        n3[idx] = torch.randint(0, pop_size, (len(idx),), device=device)

        invalid = (n1 == target_idx) | (n2 == target_idx) | (n3 == target_idx)
        invalid = invalid | (n1 == n2) | (n1 == n3) | (n2 == n3)

    random_values = (torch.rand(pop_size, 1, device=device) * 0.2 - 0.1)
    v = x[n1] + f * (x[n2] - x[n3]) + random_values
    return v


def DE1CrossOver(x,v,CR):
    n = torch.randint(0, len(x[0]), (len(x),), device=device)  
    l = getExponentialCrossoverLength(len(x), len(x[0]), CR)  
    l = torch.tensor(l, device=device).unsqueeze(1) 
    q = x.clone()  

    arange = torch.arange(len(x[0]), device=device).unsqueeze(0)  
    indices = (n.unsqueeze(1) + arange) % len(x[0])

    mask = arange < l

    q.scatter_(1, indices, torch.where(mask, v, x))
    


    return q

def DE(population,numOfItration,CR):

    i = 0
    while  i < numOfItration:
        v = DE1Mutation(population)
        q = DE1CrossOver(population,v,CR)
        value_u = objectiveFunction(q)  
        value_x = objectiveFunction(population)    
        update_mask = ((value_u > value_x) )
        population[update_mask, :] = q[update_mask, :].clone()

        i += 1

    population = population.cpu()
    population = population.numpy()
    return population

    pass


if __name__ == "__main__":

    population = creatPopulation()

    y = DE(population , 10, 90)