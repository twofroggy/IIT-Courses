# Tiffany Wong
# math380 - hw #3

#%% section 2.2 - question 6

from matplotlib import pyplot as plt 
import numpy as np

#the data given in array form 
y = [3.5, 5, 6, 7, 8]
z = [3, 6, 9, 12, 15]
z_sq = []

for i in range(len(z)):
    z_sq.append(z[i]**(1/2))

#create line of best fit and get slope 
m, b = np.polyfit(z_sq, y, 1)

#multiply z_sq by m 
y_experiment = np.multiply(z_sq, m)

#plot in scatter plot form
plt.plot(z_sq, y, 'o', color='red', label="actual data")
#plot line of best fit
plt.plot(z_sq, y_experiment, "-", color='blue', label="line of best fit")
#title, labels, legend
plt.title('y vs z^(1/2)')
plt.xlabel('z^(1/2)-values')
plt.ylabel('y-values')
plt.legend(loc = "upper left")
plt.show

k = np.divide(y, z_sq)
print('the constant k is: ', k) 

#%% section 2.2 - question 12

import math 

#the data given in array form 
y = [6, 15, 42, 114, 311, 845, 2300, 6250, 17000, 46255]
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
e_to_x = []

for i in range(len(x)):
    e_to_x.append(math.exp(x[i]))

#create line of best fit and get slope 
m, b = np.polyfit(e_to_x, y, 1)
print('the estimated slope is:', m)

#multiply e_to_z by the estimated slope  
y_experiment = np.multiply(e_to_x, m)

#plot in scatter plot form
plt.plot(e_to_x, y, 'o', color='red', label="actual data")
#plot line of best fit
plt.plot(e_to_x, y_experiment, "-", color='blue', label="line of best fit")
#title, labels, legend
plt.title('y vs e^x')
plt.xlabel('e^x values')
plt.ylabel('y-values')
plt.legend(loc = "upper left")
plt.show

k = np.divide(y, e_to_x)
print('the constant k is: ', k) 


#%% section 2.3 - question project 2b 

#given data
W = [20, 300, 341, 658, 110, 2000, 2300, 8750, 71000, 71000]
H = [1000, 185, 378, 300, 190, 312, 240, 193, 60, 70]
new_W = []
average_m = []

# model: H = W^(-1/3)
#take the values of weight to the power of -1/3 
for i in range(len(W)):
    new_W.append(W[i]**(-1/3))
    
    
for j in range(len(new_W)):   
    average_m.append(H[j]/new_W[j])
    
m = sum(average_m)/len(average_m)
    
#create line of best fit and get slope 
#m, b = np.polyfit(new_W, H, 1)
print('the estimated slope is:', m)

#multiply new_H by the estimated slope  
new_H = np.multiply(new_W, m)

#plot actual data scatter plot form
plt.plot(W, H, 'o', color='red', label="actual data") 
plt.plot(W, new_H, "o", color='blue', label="modeled data")


#titles, axes, legend
plt.title('Heart Rate (beat/min) vs Weight (g)')
plt.xlabel('Weight (g)')
plt.ylabel('Heart Rate (beat/min)')
plt.legend(loc = "upper right")
plt.show

#%% section 3.1 - question 5a 

# put given data in arrays 
t = [7, 14, 21, 28, 35, 42]
P = [8, 41, 133, 250, 280, 297]

average_m = []

for j in range(len(P)):   
    average_m.append(P[j]/t[j])
 
#find slope
m = sum(average_m)/len(average_m)
print('the estimated slope is:', m)

# get new_P by multiplying t by the estimated slope  
new_P = np.multiply(t, m)

# plot P vs t
plt.plot(t, P, 'o', color='red', label="actual data") 
plt.plot(t, new_P, 'o', color='blue', label='modeled data')

# titles, axes, legend
plt.title('P vs t')
plt.xlabel('t')
plt.ylabel('P')
plt.legend(loc = "upper left")
plt.show


#%% section 3.1 - question 5b 

import numpy as np 
from matplotlib import pyplot as plt

t = [7, 14, 21, 28, 35, 42]
P = [8, 41, 133, 250, 280, 297]

new_P_2 = []

# take ln(P)
for n in range(len(P)):   
    new_P_2.append(np.log(P[n]))

# create line of best fit and get slope and y-intercept
m, b = np.polyfit(t, new_P_2, 1)
print('the estimated slope is:', m, 'y-int: ', b) 

transformed_P = np.exp((np.multiply(t, m) + np.log(b)))

#plt.plot(t, new_P_2, 'o', color='red', label="lnP = bt + lna") 

# plot P vs t
plt.plot(t, P, 'o', color='red', label="actual data") 
plt.plot(t, transformed_P, '-', color='blue', label='modeled data')

# titles, axes, legend
plt.title('P vs t')
plt.xlabel('t')
plt.ylabel('P')
plt.legend(loc = "upper left")
plt.show

#%% section 3.1 - question 7a 

from matplotlib import pyplot as plt

# given datasets
T = [88, 225, 365, 687, 4329, 10753, 30660, 60150] 
r = [57.9, 108.2, 149.6, 227.9, 778.1, 1428.2, 2837.9, 4488.9] 

# plot T vs r
plt.plot(T, r, 'o', color='red', label="actual data") 

# titles, axes, legend
plt.title('r vs T')
plt.xlabel('Period Time (T)')
plt.ylabel('Mean Distance (r)')
plt.legend(loc = "upper left")
plt.show


#%% section 3.1 - question 7b 

import numpy as np

ln_T  = np.log(T)

ln_r = np.log(r) 

m, b = np.polyfit(ln_T, ln_r, 1)
print('the estimated slope is:', m, 'y-int: ', b) 

new_r = np.exp((np.multiply(ln_T, m) + b))

plt.plot(T, r, 'o', color='red', label="actual data") 

plt.plot(T, new_r, '-', color='blue', label='modeled data')

# axes = plt.gca()
# axes.set_xlim([0,12])
# axes.set_ylim([0,9])

# titles, axes, legend
plt.title('ln(r) vs ln(T)')
plt.xlabel('ln of Period Time (ln(T))')
plt.ylabel('ln of Mean Distance (ln(r))')
plt.legend(loc = "upper left")
plt.show


















