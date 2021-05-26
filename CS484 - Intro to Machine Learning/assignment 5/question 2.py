##########################################
### CS484 Spring 2021
### Assignment 5 
### Student ID: A20442087
### Tiffany Wong

########################################## 

#%% import libraries 
import graphviz
import matplotlib.pyplot as plt
import scipy
import numpy as np
import pandas as pd
import statsmodels.api as stats
from itertools import combinations
import sklearn.ensemble as ensemble
import sklearn.tree as tree
import sklearn.metrics as metrics 
# import treeFit 
from sklearn.linear_model import LogisticRegression
import random 

#%% question 2 - 95% confidence limits for AUC metric for testing data 

# importing .csv files 

trainData = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 5/WineQuality_Train.csv', delimiter=',')
testData = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 5/WineQuality_Test.csv', delimiter = ',')
nObs = trainData.shape[0]

x_train = trainData[['alcohol','citric_acid','free_sulfur_dioxide','residual_sugar','sulphates']]
y_train = trainData['quality_grp']

x_test = testData[['alcohol','citric_acid','free_sulfur_dioxide','residual_sugar','sulphates']]
y_test = testData['quality_grp']

#%% part a 
print('PART A') 

def SWEEPOperator(pDim, inputM, tol):
    # pDim: dimension of matrix inputM, integer greater than one
    # inputM: a square and symmetric matrix, numpy array
    # tol: singularity tolerance, positive real

    aliasParam = []
    nonAliasParam = []
    
    A = np.copy(inputM)
    diagA = np.diagonal(inputM)

    for k in range(pDim):
        Akk = A[k,k]
        if (Akk >= (tol * diagA[k])):
            nonAliasParam.append(k)
            ANext = A - np.outer(A[:, k], A[k, :]) / Akk
            ANext[:, k] = A[:, k] / Akk
            ANext[k, :] = ANext[:, k]
            ANext[k, k] = -1.0 / Akk
        else:
            aliasParam.append(k)
            ANext[:, k] = 0.0 * A[:, k]
            ANext[k, :] = ANext[:, k]
        A = ANext
    return (A, aliasParam, nonAliasParam)

# A function that find the non-aliased columns, fit a logistic model, and return the full parameter estimates
def build_mnlogit(fullX, y):

    # Find the non-redundant columns in the design matrix fullX
    nFullParam = fullX.shape[1]
    XtX = np.transpose(fullX).dot(fullX)
    invXtX, aliasParam, nonAliasParam = SWEEPOperator(pDim = nFullParam, inputM = XtX, tol = 1e-7)

    # Build a multinomial logistic model
    X = fullX.iloc[:, list(nonAliasParam)]
    logit = stats.MNLogit(y, X)
    thisFit = logit.fit(method = 'newton', maxiter = 1000, gtol = 1e-6, full_output = True, disp = True)
    thisParameter = thisFit.params
    thisLLK = logit.loglike(thisParameter.values)

    # The number of free parameters
    nYCat = thisFit.J
    thisDF = len(nonAliasParam) * (nYCat - 1)

    # Return model statistics
    return (thisLLK, thisDF, thisParameter, thisFit)

chi_dict = {}

# Forward Selection
# Model 0
y = trainData['quality_grp'].astype('category')
# fins the categories of thsi categorival dtype
y_category = y.cat.categories
u = pd.DataFrame()
u = y_train.isnull()
designX = pd.DataFrame(u.where(u, 1)).rename(columns = {'quality_grp': "const"})
LLK0, DF0, fullParams0, thisFit = build_mnlogit(designX, y)
# Model 1
first_model = ['alcohol','citric_acid','free_sulfur_dioxide','residual_sugar','sulphates']
for r in range(5):
    modelTerm = first_model[r]
    trainData2 = trainData[modelTerm].dropna()
    trainData2 = stats.add_constant(trainData2, prepend = True)
    LLK1, DF1, fullParams1, thisFit = build_mnlogit(trainData2, y)
    testDev = 2.0 * (LLK1 - LLK0)
    testDF = DF1 - DF0
    testPValue = scipy.stats.chi2.sf(testDev, testDF)
    if testPValue < 0.05:
        chi_dict[first_model[r]] = testPValue
key_min = min(chi_dict.keys(), key=(lambda k: chi_dict[k]))
print('Model 1 = Intercept +', key_min)
# Model 2
second_model = [('alcohol','citric_acid'),('alcohol','free_sulfur_dioxide'),
                ('alcohol','residual_sugar'),('alcohol','sulphates')]
for r in range(4):
    modelTerm = list(second_model[r])
    trainData2 = trainData[modelTerm].dropna()
    trainData2 = stats.add_constant(trainData2, prepend = True)
    LLK1, DF1, fullParams1, thisFit = build_mnlogit(trainData2, y)
    testDev = 2.0 * (LLK1 - LLK0)
    testDF = DF1 - DF0
    testPValue = scipy.stats.chi2.sf(testDev, testDF)  
    if testPValue < 0.05:
        chi_dict[second_model[r]] = testPValue
key_min = min(chi_dict.keys(), key=(lambda k: chi_dict[k]))
print('Model 2 = Intercept +',' + '.join(''.join(t) for t in key_min))
# Model 3
thrid_model = [('alcohol','free_sulfur_dioxide','citric_acid'),
               ('alcohol','free_sulfur_dioxide','residual_sugar'),
               ('alcohol','free_sulfur_dioxide','sulphates')] 
for r in range(3):
    modelTerm = list(thrid_model[r])
    trainData2 = trainData[modelTerm].dropna()
    trainData2 = stats.add_constant(trainData2, prepend = True)
    LLK1, DF1, fullParams1, thisFit = build_mnlogit(trainData2, y)
    testDev = 2.0 * (LLK1 - LLK0)
    testDF = DF1 - DF0
    testPValue = scipy.stats.chi2.sf(testDev, testDF)
    if testPValue < 0.05:
        chi_dict[thrid_model[r]] = testPValue
key_min = min(chi_dict.keys(), key=(lambda k: chi_dict[k]))
print('Model 3 = Intercept +',' + '.join(''.join(t) for t in key_min))
# Model 4
fourth_model = [('alcohol','free_sulfur_dioxide','sulphates','citric_acid'),
                ('alcohol','free_sulfur_dioxide','sulphates','residual_sugar')]
for r in range(2):
    modelTerm = list(fourth_model[r])
    trainData2 = trainData[modelTerm].dropna()
    trainData2 = stats.add_constant(trainData2, prepend = True)
    LLK1, DF1, fullParams1, thisFit = build_mnlogit(trainData2, y)
    testDev = 2.0 * (LLK1 - LLK0)
    testDF = DF1 - DF0
    testPValue = scipy.stats.chi2.sf(testDev, testDF)
    if testPValue < 0.05:
        chi_dict[fourth_model[r]] = testPValue
key_min = min(chi_dict.keys(), key=(lambda k: chi_dict[k]))
print('Model 4 = Intercept +',' + '.join(''.join(t) for t in key_min))    
# Model 5
fifth_model = [('alcohol','free_sulfur_dioxide','sulphates','citric_acid','residual_sugar')]
for r in range(1):
    modelTerm = list(fifth_model[r])
    trainData2 = trainData[modelTerm].dropna()
    trainData2 = stats.add_constant(trainData2, prepend = True)
    LLK1, DF1, fullParams1, thisFit = build_mnlogit(trainData2, y)
    testDev = 2.0 * (LLK1 - LLK0)
    testDF = DF1 - DF0
    testPValue = scipy.stats.chi2.sf(testDev, testDF)
    if testPValue < 0.05:
        chi_dict[fifth_model[r]] = testPValue
key_min = min(chi_dict.keys(), key=(lambda k: chi_dict[k]))
print('Model 5 = Intercept +',' + '.join(''.join(t) for t in key_min)) 
        

#%% part b 
print('PART B') 

clf = LogisticRegression(random_state=0).fit(x_train, y_train)
y_score = clf.predict_proba(x_test) 
auc = metrics.roc_auc_score(y_test, y_score[:,1])
print("AUC: ", auc) 
    

#%% part c 
print('PART C') 

trainData = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 5/WineQuality_Train.csv', delimiter=',')
testData = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 5/WineQuality_Test.csv', delimiter = ',')
nObs = trainData.shape[0]

x_train = trainData[['alcohol','citric_acid','free_sulfur_dioxide','residual_sugar','sulphates']]
y_train = trainData['quality_grp']

x_test = testData[['alcohol','citric_acid','free_sulfur_dioxide','residual_sugar','sulphates']]
y_test = testData['quality_grp']

train_sample = pd.concat([x_train,y_train],axis=1)
train_sample = train_sample.values

random.seed(20210415)
def sample_wr(inData):
    n = len(inData)
    outData = np.empty((n,6))
    for i in range(n):
        j = int(random.random() * n)
        outData[i] = inData[j]
    return outData

AUC_array = np.zeros(10000)
for i in range(10000):
    bootstrap = sample_wr(train_sample) 
    x_train = bootstrap[:,:5]
    y_train = bootstrap[:,-1]
    logistic = LogisticRegression(random_state = 20210415).fit(x_train,y_train)
    pred_prob = logistic.predict_proba(x_test)
    AUC_array[i] = metrics.roc_auc_score(y_test, pred_prob[:,1])
    
plt.hist(AUC_array, bins=np.arange(min(AUC_array), max(AUC_array)+0.001, 0.001), align='mid') 
plt.show() 

#%% part d
print('PART D') 

print('95% Confidence Interval: {:.7f},{:.7f}'
      .format(np.percentile(AUC_array, (2.5)), np.percentile(AUC_array, (97.5)))) 

