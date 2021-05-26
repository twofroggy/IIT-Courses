#%% math380 - hw 5
# 7.2.3 and 7.3.3

import numpy as np
import matplotlib.pyplot as plt
from sympy.solvers import solve
from sympy import Symbol

# x vs y = wheat vs corn = w vs c

# the inequalities in terms of w, solved for c 

#%% 7.3.3 - method 2: solving it geometrically

import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.inline

# Construct lines
# W >= 0 
W = np.linspace(0, 40) 
# W + C <= 45
C1 = 45 - W
# 3W + 2C <= 100
C2 = ((100 - 3*W) / 2)
# 2W + 4C <= 120
C3 = ((120 - 2*W) / 4) 


# variable limitations 
# C >= 0
C4 = 0
# W >= 0
C5 = 0

# C >= 0 
C = np.arange(0, 50)
W_2 = np.arange(0,50)

y_buf = [0,0]
x_buf = [0,0]

# Make plot
#plt.plot(W, y, label=r'$W\geq0$') 
plt.plot(W, C1, 'b', label=r'$W + C\leq45$')
plt.plot(W, C2, 'r', label=r'$3W + 2C\leq100$')
plt.plot(W, C3, 'g', label=r'$2W + 4C\geq120$')
#plt.axvline(x=C5, color='k', linestyle='-') 

plt.xlim((0, 35))
plt.ylim((0, 40))
plt.xlabel('Acres of Wheat (W)')
plt.ylabel('Acres of Corn (C)')

# # Fill feasible region
C6 = np.minimum(C2, C3)
C7 = np.maximum(C, W_2)
#C7 = np.minimum()
plt.fill_between(W, C6, C7, where=C6>C7, color='grey', alpha=0.5)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


#%% 7.2.3 - method 1: solving it with a solver 

# 200W + 300C
# W + C <= 45
# 3W + 2C <= 100
# 2W + 4C <= 120 

c = [-200, -300]
A = [[1, 1], [3, 2], [2, 4]]
b = [45, 100, 120]
x0_bounds = (None, None)
x1_bounds = (-3, None)
from scipy.optimize import linprog
res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], 
              method='revised simplex')

print(res)


























