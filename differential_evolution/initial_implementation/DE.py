import torch
import torch.multiprocessing as mp
import numpy as np
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def mutation(x):
    f = 0.1 

    x = x.to(device='cuda')  

    n1 = torch.randint(0, 100, (100,), device=device) 
    n2 = torch.randint(0, 100, (100,), device= device)  
    n3 = torch.randint(0, 100, (100,), device= device) 

    random_values = (torch.rand(100, 1, device= device ) * 0.2 - 0.1)  

    v = x[n1] + f * (x[n2] - x[n3]) + random_values  
    



    return v 


def check(sum2):
    result = torch.empty_like(sum2)
    result[(sum2 < 0) ] = -1
    result[(sum2 <= 0.1) & (sum2 >= 0)] = 0.1
    result[(sum2 > 0.1) & (sum2 <= 0.2)] = 0.2
    result[(sum2 > 0.2) & (sum2 <= 0.4)] = 0.3
    result[(sum2 > 0.4) & (sum2 <= 0.5)] = 0.4
    result[(sum2 > 0.5) & (sum2 <= 0.6)] = 0.55
    result[(sum2 > 0.6) & (sum2 <= 0.7)] = 0.7
    result[(sum2 > 0.7) & (sum2 <= 0.8)] = 0.85
    result[(sum2 > 0.8) & (sum2 <= 0.9)] = 0.95
    result[(sum2 > 0.9) & (sum2 <= 0.999)] = 1
    result[sum2 >= 0.999] = 0.01

    return result


def create_chromosome():
    x = torch.randint(0, 129, (100,185), device=device) 
    return x

def fitness(x):
    x = torch.tensor(x, device = device)
    
    tav = (129 - x) / 80
   
    tav2 = check(tav)
    
    rows_with_negative = (tav2 < 0).any(dim=1) 
   

    tav2[rows_with_negative] = -1
    
    tav2 = tav2.sum(dim=1) / 185 
    
    return tav2

def chosing(x,tav):
    x1 = []
    y = []
    t = 0
    g = len(x)
    max = 0
    f = 0
    flag = True
    while t < g:
        
        if max < tav[t] or flag:
            
            flag = False
            f = t
            max = tav[t]
            
        t += 1

    y = x[f].copy()

    return y


def cross_over(x, v):
 
    n = torch.randint(0, 185, (100,), device=device)  
    l = torch.randint(1, 185 + 1, (100,), device=device)  
    
    CR = 90  

    q = x.clone()  
    
    
    arange = torch.arange(185, device=device).unsqueeze(0)  
    indices = (n.unsqueeze(1) + arange) % 185

    mask = arange < l.unsqueeze(1)  

    q.scatter_(1, indices, torch.where(mask, v, x))
    
  
    value_u = fitness(q)  
    
    value_x = fitness(x)  

    rand_tensor = torch.rand(100, device=device)  

    update_mask = ((rand_tensor < CR / 100) & (value_u > value_x) )
    #print(update_mask)
    #print(update_mask)
    #print("Before update:")
    #print(x[update_mask])

    x[update_mask, :] = q[update_mask, :].clone() 

    #print("After update:")
    #print(x[update_mask])

  
    return x

    


def DE(sho):
    
    x = create_chromosome().clone()
    x = torch.tensor(x, dtype=torch.float32, device=device)
    
    i = 0
    j = 0

    while i < 1000:
        
        v = mutation(x)
        
        x = cross_over(x,v).clone()
        
        i += 1
        
        

    tav = fitness(x).clone()
    x = x.cpu()
    x = x.numpy()
    tav = tav.cpu()
    tav = tav.numpy()
    x = chosing(x,tav).copy()
    j = 0
    tav2 = []
    print(x)
    c= []
    while j < 185 :
        c.append((129 - x[j]) / 80)         
        j += 1
        
    tav2.append(c)

    i = 0
    sun = 0
    while i < len(tav2[0]):
        sun += tav2[0][i]
        i += 1

    print(sun / 185)

    return tav2


if __name__ == "__main__":

    y = DE(10)
    print(y)
