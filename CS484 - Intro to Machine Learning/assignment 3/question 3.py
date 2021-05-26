##########################################
### CS484 Spring 2021
### Assignment 3
### Student ID: A20442087
### Tiffany Wong

##########################################

#%% question 3a 

import numpy
import pandas
import scipy

import statsmodels.api as stats

df = pandas.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 3/sample_v10.csv')

nObs = df.shape[0]

print('--- QUESTION 3A ---')

# Specify y as a categorical variable
y = df['y'].astype('category')
y_category = y.cat.categories
print(df['y'].value_counts()) 

print(' ')
#%% all the differnt combos of dfs 

all_x = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'] 

x_combos = []

x_combos.append(['x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'])
x_combos.append(['x1', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'])
x_combos.append(['x1', 'x2', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'])
x_combos.append(['x1', 'x2', 'x3', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'])
x_combos.append(['x1', 'x2', 'x3', 'x4', 'x6', 'x7', 'x8', 'x9', 'x10'])
x_combos.append(['x1', 'x2', 'x3', 'x4', 'x5', 'x7', 'x8', 'x9', 'x10'])
x_combos.append(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x8', 'x9', 'x10'])
x_combos.append(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x9', 'x10']) 
x_combos.append(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x10'])
x_combos.append(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9']) 


#%% 
print('--- QUESTION 3B ---')

# Backward Selection
# Consider Model 0 is y = Intercept + all xi's 
DriveTrain = df[['y']].astype('category')
X = pandas.get_dummies(DriveTrain)
X = df[all_x] 
X = stats.add_constant(X, prepend=True)
DF1 = numpy.linalg.matrix_rank(X) * (len(y_category) - 1)

logit = stats.MNLogit(y, X)
thisFit = logit.fit(method='newton', full_output = True, maxiter = 100, tol = 1e-8)
thisParameter = thisFit.params
LLK1 = logit.loglike(thisParameter.values)

#print(thisFit.summary())
print("Model Log-Likelihood Value =", LLK1)
print("Number of Free Parameters =", DF1) 

print(' ')
#%% 
import numpy as np
import pandas as pd
import statsmodels.api as smodel
import time

from itertools import combinations 

AIC = [] 
BIC = []

#%% 

print('--- QUESTION 3C ---')

for i in range(len(x_combos)): 
 
    print("Removed feature:", all_x[i]) 
    y = df[['y']].astype('category')
    X = pandas.get_dummies(y)
    X = df[x_combos[i]]
    X = stats.add_constant(X, prepend=True)
    DF0 = numpy.linalg.matrix_rank(X) * (len(y_category) - 1)
    
    logit = stats.MNLogit(y, X)
    thisFit = logit.fit(method='newton', full_output = True, maxiter = 100, tol = 1e-8)
    thisParameter = thisFit.params
    LLK0 = logit.loglike(thisParameter.values)
    
    Deviance = 2 * (LLK1 - LLK0)
    DF = DF1 - DF0
    pValue = scipy.stats.chi2.sf(Deviance, DF)
    
    AIC.append(2.0 * DF0 - 2.0 * LLK0)
    BIC.append(DF0 * np.log(nObs) - 2.0 * LLK0) 

    print("Model Log-Likelihood Value =", LLK0)
    print("Number of Free Parameters =", DF0)
    print("Deviance =", Deviance) 
    print("Deviance degree of freedom =", DF) 
    print("Deviance significance value =", pValue)
    print(' ')

print(' ')
#%% 
print('--- QUESTION 3E ---')

for i in range(len(x_combos)):
    print('Removed feature:', all_x[i])
    print('Akaike Information Criterion:', AIC[i])
    print('Bayesian Information Criterion', BIC[i])
    print(' ')

print('AIC recommends: model #', AIC.index(min(AIC))+1)
print('BIC recommends: model #', BIC.index(min(BIC))+1) 

