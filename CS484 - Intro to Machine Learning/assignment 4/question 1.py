##########################################
### CS484 Spring 2021
### Assignment 4 
### Student ID: A20442087
### Tiffany Wong

########################################## 

#%% 
import numpy as np
import pandas as pd

from sklearn import preprocessing, naive_bayes

import scipy 
import itertools
#%% question 1 

df = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 4/Purchase_Likelihood.csv')

# Define a function to visualize the percent of a particular target category by a nominal predictor
def RowWithColumn (
   rowVar,          # Row variable
   columnVar,       # Column predictor
   show = 'ROW'):   # Show ROW fraction, COLUMN fraction, or BOTH table

   countTable = pd.crosstab(index = rowVar, columns = columnVar, margins = False, dropna = True)
   print("Frequency Table: \n", countTable)
   print( )

   if (show == 'ROW' or show == 'BOTH'):
       rowFraction = countTable.div(countTable.sum(1), axis='index')
       print("Row Fraction Table: \n", rowFraction)
       print( )

   if (show == 'COLUMN' or show == 'BOTH'):
       columnFraction = countTable.div(countTable.sum(0), axis='columns')
       print("Column Fraction Table: \n", columnFraction)
       print( )

   return

# EBilling -> CreditCard, Gender, JobCategory
subData = df[['group_size', 'homeowner', 'married_couple', 'insurance']].dropna()

catGroup_Size = subData['group_size'].unique()
catHomeowner = subData['homeowner'].unique()
catMarried_Couple = subData['married_couple'].unique()
catInsurance = subData['insurance'].unique()

# print('Unique Values of group_size: \n', catGroup_Size)
# print('Unique Values of homeowner: \n', catHomeowner)`
# print('Unique Values of married_couple: \n', catMarried_Couple)
# print('Unique Values of insurance: \n', catInsurance)

print('---QUESTION 1A---')

subData = subData.astype('category')
xTrain = pd.get_dummies(subData[['group_size', 'homeowner', 'married_couple']])

yTrain = np.where(subData['insurance'] == '0', 1, 0)

# Correctly Use sklearn.naive_bayes.CategoricalNB
feature = ['group_size', 'homeowner', 'married_couple']

labelEnc = preprocessing.LabelEncoder()
yTrain = labelEnc.fit_transform(subData['insurance'])
yLabel = labelEnc.inverse_transform([0, 1])

uGroup_Size = np.unique(subData['group_size'])
uHomeowner = np.unique(subData['homeowner'])
uMarried_Couple = np.unique(subData['married_couple'])

featureCategory = [uGroup_Size, uHomeowner, uMarried_Couple]
print(featureCategory)

featureEnc = preprocessing.OrdinalEncoder(categories = featureCategory)
xTrain = featureEnc.fit_transform(subData[['group_size', 'homeowner', 'married_couple']])

_objNB = naive_bayes.CategoricalNB(alpha = 1.0e-10)
thisModel = _objNB.fit(xTrain, yTrain)

print('Number of samples encountered for each class during fitting')
print(yLabel)
print(_objNB.class_count_)
print('\n')

print('Probability of each class:')
print(yLabel)
print(np.exp(_objNB.class_log_prior_))
print('\n')

#%%
print('---QUESTION 1B---')
RowWithColumn(rowVar = subData['insurance'], columnVar = subData['group_size'], show = 'ROW') 

#%%
print('---QUESTION 1C---')
RowWithColumn(rowVar = subData['insurance'], columnVar = subData['homeowner'], show = 'ROW') 

#%%
print('---QUESTION 1D---')
RowWithColumn(rowVar = subData['insurance'], columnVar = subData['married_couple'], show = 'ROW') 

#%% 
print('---QUESTION 1E---')

# Define a function that performs the Chi-square test
def PearsonChiSquareTest (
    xCat,           # input categorical feature
    yCat,           # input categorical target variable
    debug = 'N'     # debugging flag (Y/N) 
    ):

    obsCount = pd.crosstab(index = xCat, columns = yCat, margins = False, dropna = True)
    cTotal = obsCount.sum(axis = 1)
    rTotal = obsCount.sum(axis = 0)
    nTotal = np.sum(rTotal)
    expCount = np.outer(cTotal, (rTotal / nTotal))
    print("CROSSTAB")
    print(obsCount)
    if (debug == 'Y'):
        print('Observed Count:\n', obsCount)
        print('Column Total:\n', cTotal)
        print('Row Total:\n', rTotal)
        print('Overall Total:\n', nTotal)
        print('Expected Count:\n', expCount)
        print('\n')
       
    chiSqStat = ((obsCount - expCount)**2 / expCount).to_numpy().sum()
    chiSqDf = (obsCount.shape[0] - 1.0) * (obsCount.shape[1] - 1.0)
    chiSqSig = scipy.stats.chi2.sf(chiSqStat, chiSqDf)

    cramerV = chiSqStat / nTotal
    if (cTotal.size > rTotal.size):
        cramerV = cramerV / (rTotal.size - 1.0)
    else:
        cramerV = cramerV / (cTotal.size - 1.0)
    cramerV = np.sqrt(cramerV)

    return(chiSqStat, chiSqDf, chiSqSig, cramerV)

catPred = ['group_size', 'homeowner', 'married_couple'] 

for pred in catPred: 
    chisqstat, chisqdf, chisqsig, cramerV = PearsonChiSquareTest(df[pred], df['insurance']) 
    print('Cramer for', pred, cramerV) 

#%%
print('---QUESTION 1F---')  

# Create the all possible combinations of the features' values
xTest = []
num = len(catGroup_Size)*len(catHomeowner)*len(catMarried_Couple) 
for j in catGroup_Size: 
    for k in catHomeowner: 
        for p in catMarried_Couple: 
            xTest.append([j,k,p]) 

xTest = pd.DataFrame(xTest, columns = ['group_size', 'homeowner', 'married_couple'])
xTest = xTest[['group_size', 'homeowner', 'married_couple']].astype('category')

x = df[['group_size', 'homeowner', 'married_couple']].astype('category')
y = df['insurance'].astype('category') 
classifier = naive_bayes.MultinomialNB(alpha = 1.0e-10).fit(x, y)

# Score the xTest and append the predicted probabilities to the xTest
yTest = classifier.predict_proba(xTest)
yTest = pd.DataFrame(yTest, columns = ['P(insurance=0)',
                                       'P(insurance=1)',
                                       'P(insurance=2)'])

yTest_score = pd.concat([xTest, yTest], axis = 1)
print(yTest_score)

#%%
print('---QUESTION 1G---')
yTest_score['1g'] =  yTest_score['P(insurance=1)']/yTest_score['P(insurance=2)']

print(yTest_score)



