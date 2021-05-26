# 


#%% 12.5.7

x = [0.5] 
y = [1] 
t = [0]

for i in range(5) :
    t.append(t[i] + 1) 
    x.append(x[i] + (x[i] - (x[i]*y[i]) - (0.75*y[i]))) 
    y.append(y[i] + ((x[i]*y[i]) - y[i] - (0.75*x[i])))
    

for i in range(5):
    print('for t =', i, 'x =', x[i], ' and y =', y[i]) 
    
#%% 13.2.6

x = [1] 
y = [1] 
lamb = 1/16 
delta = 1.2 

for i in range(25): 
    x.append(x[i]+(lamb*(x[i]*(1.08-(0.06*x[i])))))
    y.append(y[i]+(lamb*((3.78*y[i])-(0.27*(y[i]**2)))))   
    lamb = lamb*delta
    
for i in range(25): 
    print('for k =', i, 'x =', x[i], ' and y =', y[i]) 
    
    