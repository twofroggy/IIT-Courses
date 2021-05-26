# Tiffany Wong
# math380 - hw #4

#%% section 3.2 - question 2b

from scipy.optimize import linprog 
import numpy as np

# coefficient for r, a, b 
obj = [1, 0, 0]

# python has inequalities as x + y <= 20 so i multiplied both sides by -1 
# to convert how i have it currently, which is r + a + b >= 0
lhs_ineq = np.array([[-1, 29.1, 1], [-1, -29.1, -1], 
                    [-1, 48.2, 1], [-1, -48.2, -1], 
                    [-1, 72.7, 1], [-1, -72.7, -1], 
                    [-1, 92, 1], [-1, -92, -1], 
                    [-1, 118, 1], [-1, -118, -1], 
                    [-1, 140, 1], [-1, -140, -1], 
                    [-1, 165, 1], [-1, -165, -1], 
                    [-1, 199, 1], [-1, -199, -1]]) 

rhs_ineq = np.array([0.0493, -0.0493, 
            0.0821, -0.0821, 
            0.123, -0.123, 
            0.154, -0.154, 
            0.197, -0.197, 
            0.234, -0.234, 
            0.274, -0.274, 
            0.328, -0.328]) 

opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
              method="revised simplex") 

print(opt)

#%% question 2b - least squares method 

x = [29.1, 48.2, 72.7, 92.0, 118, 140, 165, 199]
y = [0.0493, 0.0821, 0.123, 0.154, 0.197, 0.234, 0.274, 0.328]

#find means of x and y datasets
mean_x = np.mean(x)
mean_y = np.mean(y)

#total number of values 
n = len(x)

#use the formula to calculate 'a' and 'b' in y=ax+b
numer = 0
denom = 0
for i in range(n):
    numer += (x[i] - mean_x) * (y[i] - mean_y)
    denom += (x[i] - mean_x) ** 2

a = numer / denom
b = mean_y - (a * mean_x)
 
# Printing coefficients
print('equation of the least squares line is: y=', a, 'x + ', b)

#%% section 3.2 - question 3

from scipy.optimize import linprog 
import numpy as np

# coefficient for r, c1, c2, c3 
obj = [1, 0, 0, 0]

# python has inequalities as x + y <= 0 so i multiplied both sides by -1 
# to convert how i have it currently, which is r + c1 + c2 + c3 >= y
lhs_ineq = [[-1, -0.01, -0.1, -1], [-1, 0.01, 0.1, 1], 
            [-1, -0.04, -0.2, -1], [-1, 0.04, 0.2, 1], 
            [-1, -0.09, -0.3, -1], [-1, 0.09, 0.3, 1], 
            [-1, -0.16, -0.4, -1], [-1, 0.16, 0.4, 1], 
            [-1, -0.25, -0.5, -1], [-1, 0.25, 0.5, 1]]

rhs_ineq = [-0.06, 0.06, 
            -0.12, 0.12, 
            -0.36, 0.36, 
            -0.65, 0.65, 
            -0.95, 0.95]

opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
              method="revised simplex") 

print(opt)

#%% PuLP function / 3.2.3 - chebychevs 

import pulp
from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable, LpContinuous

# create the model 
model = pulp.LpProblem("problem 3.2.3", pulp.LpMinimize)

# initialize the decision variables
r = pulp.LpVariable("r", cat='Continuous')    #r
a = pulp.LpVariable("a", cat='Continuous')    #c1
b = pulp.LpVariable("b", cat='Continuous')    #c2
c = pulp.LpVariable("c", cat='Continuous')    #c3

# objective function
model += 1*r + 0, 'Objective Function'

# constraints
model += r + 0.01*a + 0.1*b + c >= 0.06, "1_constraint_1"
model += r - 0.01*a - 0.1*b - c >= -0.06, "1_constraint_2"

model += r + 0.04*a + 0.2*b + c >= 0.12, "2_constraint_1"
model += r - 0.04*a - 0.2*b - c >= -0.12, "2_constraint_2"

model += r + 0.09*a + 0.3*b + c >= 0.36, "3_constraint_1"
model += r - 0.09*a - 0.3*b - c >= -0.36, "3_constraint_2"

model += r + 0.16*a + 0.4*b + c >= 0.65, "4_constraint_1"
model += r - 0.16*a - 0.4*b - c >= -0.65, "4_constraint_2"

model += r + 0.25*a + 0.5*b + c >= 0.95, "5_constraint_1"
model += r - 0.25*a - 0.5*b - c >= -0.95, "5_constraint_2"


# solve the problem
model.solve() 

pulp.LpStatus[model.status]

for variable in model.variables(): 
    print ("{} = {}".format(variable.name, variable.varValue))


#%% question 3.2.3 - least squares 
import numpy as np

x = [0.1, 0.2, 0.3, 0.4, 0.5]
y = [0.06, 0.12, 0.36, 0.65, 0.95]

sum_x = 0
sum_y = 0
sum_xy = 0 
sum_xsq = 0
sum_xsqy = 0
sum_xfour = 0
    
for i in range(5): 
    sum_x += x[i] 
    sum_y += y[i]
    sum_xy += x[i]*y[i]
    sum_xsq += (x[i]**2)
    sum_xsqy += (x[i]**2)*y[i]
    sum_xfour += x[i]**4

# find c1
a = sum_xsqy/sum_xfour

# find c2
b = ((5*sum_xy) - (sum_x*sum_y)) / ((5*(sum_xsq)) - (sum_x**2))

# find c3
c = ((sum_xsq*sum_y) - (sum_xy*sum_x)) / ((5*(sum_xsq)) - (sum_x**2))

print(a, b, c)


#%% 3.3.4 - finding ln_P

P = [8, 41, 133,250, 280, 297]
ln_P = []

for i in P:
    ln_P.append(np.log(i))
    
print(ln_P)
#%% question 3.3.4 - chebyshev's approx criterion (PuLP)

import numpy as np
import pulp
from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable, LpContinuous

# create the model 
model = pulp.LpProblem("problem 3.3.4", pulp.LpMinimize)

# initialize the decision variables
r = pulp.LpVariable("r", cat='Continuous')    #r
a = pulp.LpVariable("a", cat='Continuous')    # y-intercept
b = pulp.LpVariable("b", cat='Continuous')    # slope!!

# objective function
model += 1*r + 0, 'Objective Function'

# constraints
model += r + 7*b + a >= ln_P[0], "1_constraint_1"
model += r - 7*b - a >= -ln_P[0], "1_constraint_2"

model += r + 14*b + a >= ln_P[1], "2_constraint_1"
model += r - 14*b - a >= -ln_P[1], "2_constraint_2"

model += r + 21*b + a >= ln_P[2], "3_constraint_1"
model += r - 21*b - a >= -ln_P[2], "3_constraint_2"

model += r + 28*b + a >= ln_P[3], "4_constraint_1"
model += r - 28*b - a >= -ln_P[3], "4_constraint_2"

model += r + 35*b + a >= ln_P[4], "5_constraint_1"
model += r - 35*b - a >= -ln_P[4], "5_constraint_2"

model += r + 42*b + a >= ln_P[5], "6_constraint_1"
model += r - 42*b - a >= -ln_P[5], "6_constraint_2"

# solve the problem
model.solve() 

pulp.LpStatus[model.status]

for variable in model.variables(): 
    print ("{} = {}".format(variable.name, variable.varValue))


#%% question 3.3.4 - least squares 

# ln_P array exists from earlier

t = [7, 14, 21, 28, 35, 42] 

m = 6

sum_t = 0
sum_lnP = 0
sum_tlnP = 0 
sum_tsq = 0

    
for i in range(m): 
    sum_t += t[i] 
    sum_lnP += ln_P[i]
    sum_tlnP += t[i]*ln_P[i]
    sum_tsq += (t[i]**2)

# find b, slope in this case
b = ((m*sum_tlnP) - (sum_t*sum_lnP)) / ((m*sum_tsq) - (sum_t**2))

# find a, intecept in this case 
ln_a = ((sum_tsq*sum_lnP) - (sum_tlnP*sum_t)) / ((m*(sum_tsq)) - (sum_t**2))

print('slope:', b, 'intercept:', ln_a)


#%% 3.3.8a - least squares: y=ax

import numpy as np 

x_buf = np.array([5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) 
x = x_buf*(10**-3)

y_buf = np.array([0, 19, 57, 94, 134, 173, 216, 256, 297, 343, 390])
y = y_buf*(10**-5) 

m = 11 

sum_xy = 0
sum_xsq = 0

for i in range(m): 
    sum_xy += x[i]*y[i] 
    sum_xsq += (x[i]**2)
    
a = sum_xy / sum_xsq 

print('slope:', a)

#%% 3.3.8b - least squares: y=ax +b 

sum_x = 0
sum_y = 0
sum_xy = 0 
sum_xsq = 0

    
for i in range(m): 
    sum_x += x[i] 
    sum_y += y[i]
    sum_xy += x[i]*y[i]
    sum_xsq += (x[i]**2)

# find a, slope in this case
a = ((m*sum_xy) - (sum_x*sum_y)) / ((m*sum_xsq) - (sum_x**2))

# find b, intecept in this case 
b = ((sum_xsq*sum_y) - (sum_xy*sum_x)) / ((m*(sum_xsq)) - (sum_x**2))

print('slope:', a, 'intercept:', b)


#%% 3.3.8c - least squares : y = ax^2

sum_xsqy = 0 
sum_xfour = 0 

for i in range(m):
    sum_xsqy += ((x[i]**2)*y[i])
    sum_xfour += (x[i]**4) 
    
# find a, coefficient of quadratic in this case 
a = sum_xsqy / sum_xfour 

print('a coefficient:', a)


#%% 3.4.7a: W = kl^3 - least squares 

# data given 
x = [14.5, 12.5, 17.25, 14.5, 12.625, 17.75, 14.125, 12.625]
z = [27, 17, 41, 26, 17, 49, 23, 16]

# g (inches, girth) given data
y = [9.75, 8.375, 11, 9.75, 8.5, 12.5, 9, 8.5]

m = 8

# summations 
sum_xthreez = 0 
sum_xsix = 0 

# number of data pairs
m = 8

# summation results 
for i in range(m): 
    sum_xthreez += ((x[i]**3)*z[i])
    sum_xsix += (x[i]**6)

a = sum_xthreez / sum_xsix
print('coefficient k:', a)

z_7a = [] 
for i in range(m): 
    z_7a.append(z[i] - (a*(x[i]**3)))


#%% 3.4.7b: W = klg^2 - least squares


# intro to summation 
sum_xysqz = 0 
sum_xsqyfour = 0 

# summation results 
for i in range(m): 
    sum_xysqz += (x[i]*(y[i]**2)*z[i])
    sum_xsqyfour += ((x[i]**2)*(y[i]**4)) 
    
a = sum_xysqz / sum_xsqyfour

print('coefficient k:', a)

z_7b = [] 
for i in range(m): 
    z_7b.append(z[i] - (a*x[i]*(y[i]**2)))

#%% 3.4.8: W=cg^3 - least squares

# z = W
# y = g 
# x = l 

# intro to summation variables 
sum_ycubedz = 0
sum_ysix = 0 

# summation results 
for i in range(m): 
    sum_ycubedz += ((y[i]**3)*z[i])
    sum_ysix += (y[i]**6) 
    
a = sum_ycubedz / sum_ysix 

print ('coefficient c:', a)

z_8a = [] 
for i in range(m): 
    z_8a.append(z[i] - (a*(y[i]**3)))

#%% 3.4.8: W=kgl^2 - least squares

# z = W
# y = g 
# x = l 

# intro to summation variables 
sum_yxsqz = 0
sum_ysqxfour = 0

# summation results
for i in range(m): 
    sum_yxsqz += (y[i]*(x[i]**2)*z[i]) 
    sum_ysqxfour += ((y[i]**2)*(x[i]**4)) 

a = sum_yxsqz / sum_ysqxfour 

print ('coefficient k:', a)

z_8b = [] 
for i in range(m): 
    z_8b.append(z[i] - (a*y[i]*(x[i]**2)))


#%% make table for all values i have 

import pandas as pd 
import numpy as np

buf_array = {'l': x, 
             'g': y, 
             'W': z, 
             'W - kl^3': z_7a, 
             'W - klg^2': z_7b, 
             'W - cg^3': z_8a, 
             'W - kgl^2': z_8b}

df = pd.DataFrame(data=buf_array)
pd.set_option('display.expand_frame_repr', False)


#%% 


sum = 0 

for i in range(8): 
    sum += (z_8b[i]**2) 
    
print(sum)





