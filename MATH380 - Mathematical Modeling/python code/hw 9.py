###########
# MATH380 
# HW 9

#%% question 11.1.4 

import numpy as np
import math
import pandas as pd 
import matplotlib.pyplot as plt 

# def find_values(z):
#    M = z[0]
#    r = z[1]
#    t_star = z[2]

#    F = np.zeros(3)
#    F[0] = (M/(1+np.exp(-r*M*(1790-t_star))))-3929000
#    F[1] = (M/(1+np.exp(-r*M*(1870-t_star))))-38558000
#    F[2] = (M/(1+np.exp(-r*M*(1950-t_star))))-150697000
#    return F

# z = fsolve(find_values,[1.0,1.0,1.0]) 
# print(z)

# M = z[0] 
# r = z[1] 
# t_star = z[2] 

#%% 
df = pd.read_csv('/Users/tiffwong/Desktop/math380/python code/11.1.4.csv') 

# years from 1790 to 2010
full_x = df['year'] 

# years from 1790 to 1950
x = full_x.head(17) 
# for i in range(17): 
#     x.append(i)  
    
# USA population from 1790 to 2010
full_y = df['observed population'] 

# USA population from 1790 to 1950
y = full_y.head(17) 

# observed data
plt.plot(x, y, 'og')  
plt.title('observed data') 
plt.xlabel('year') 
plt.ylabel('USA population') 
#%% 
# guess a carrying population based on 1950's pop
M = 309000000 

# plug original population values into ln(P/(M-P))
log_y = (np.log(y/(M-y))) 

# get a line of best-fit
rM, C = np.polyfit(x, log_y, 1) 
r = rM/M
print('M =', M, 'r =', r, 'rM =', rM, 'and C =', C)


# graph ln(P/(M-P)) vs t data 
plt.plot(x, log_y, 'ob') 
plt.title('ln(P/(M-P)) vs t') 
plt.xlabel('year') 
plt.ylabel('ln(P/(M-P))')  

#%% 
t_star = -C/rM 
print('t* =', t_star)

pred_y = []
for i in full_x: 
    pred_y.append(M/(1+math.exp(-rM*(i-t_star))))

df['predicted population'] = pred_y

percent_err = [] 
for i in range(len(df)):
    percent_err.append((pred_y[i]-full_y[i])/full_y[i]*100) 
    
df['percent error'] = percent_err 

#%% graph it

ax = plt.gca()

ax.scatter(full_x, df['observed population'], color='b', label='observed population')
ax.scatter(full_x, df['predicted population'], color='r', label='predicted population')
plt.title('observed vs predicted data')
plt.xlabel('year') 
plt.ylabel('US population') 
ax.legend(loc='upper left') 


#%% question 11.1.6 

import numpy as np
import math
import pandas as pd 
import matplotlib.pyplot as plt 

t = [2, 6, 10] 
X = [1887, 4087, 4853] 
ln_X = [-0.5, 1.5, 3.5] 

# observed data
plt.plot(t, X, 'og')  
plt.title('observed data') 
plt.xlabel('time t') 
plt.ylabel('people infected by disease, X') 

#%% 
# polyfit with ln_X vs t 
plt.plot(t, ln_X, 'og')  
plt.title('ln_X vs t') 
plt.xlabel('time t') 
plt.ylabel('people infected by disease, Xln(X/(N-X))') 

# limiting poulation of people that could be infected with disease 
N = 5000
kN, C = np.polyfit(t, ln_X, 1) 
k = kN/N
print('N =', N, 'k =', k, 'kN =', kN, 'and C =', C)

t_star = -C/kN 
print('t* =', t_star)