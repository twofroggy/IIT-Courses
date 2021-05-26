##########################################
### CS484 Spring 2021
### Assignment 4 
### Student ID: A20442087
### Tiffany Wong

########################################## 

#%% import libraries 
import graphviz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.metrics as metrics
import sklearn.neighbors as kNN
import sklearn.svm as svm
import sklearn.tree as tree
import statsmodels.api as sm

#%% 
print('---QUESTION 2A---')

# Set some options for printing all the columns
pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)
pd.set_option('precision', 13)
np.set_printoptions(precision = 13)

trainData = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 4/SpiralWithCluster.csv',
                        usecols = ['SpectralCluster', 'x', 'y'])

# y_threshold = trainData['id'].mean() 

# Scatterplot that uses prior information of the grouping variable
carray = ['red', 'green']
plt.figure(dpi=200)
for i in range(2):
    subData = trainData[trainData['SpectralCluster'] == i]
    plt.scatter(x = subData['x'],
                y = subData['y'], c = carray[i], label = i, s = 25)
plt.grid(True)
plt.title('Prior SpectralCluster Information')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(title = 'SpectralCluster', loc = 'best', bbox_to_anchor = (1, 1), fontsize = 14)
plt.show()

# Build Support Vector Machine classifier
xTrain = trainData[['x','y']]
yTrain = trainData['SpectralCluster'] 

svm_Model = svm.SVC(kernel = 'linear', decision_function_shape = 'ovr', 
                    random_state = 20210325, max_iter = -1)
thisFit = svm_Model.fit(xTrain, yTrain)
y_predictClass = thisFit.predict(xTrain) 

print('Mean Accuracy = ', metrics.accuracy_score(yTrain, y_predictClass))
trainData['_PredictedClass_'] = y_predictClass

svm_Mean = trainData.groupby('_PredictedClass_').mean()
print(svm_Mean)

print('Intercept = ', thisFit.intercept_)
print('Coefficients = ', thisFit.coef_)

# get the separating hyperplane
w = thisFit.coef_[0]
bSlope = -w[0] / w[1]
xx = np.linspace(-3, 3)
aIntercept = (thisFit.intercept_[0]) / w[1]
yy = aIntercept + bSlope * xx

# plot the parallels to the separating hyperplane that pass through the
# support vectors
supV = thisFit.support_vectors_
wVect = thisFit.coef_
crit = thisFit.intercept_[0] + np.dot(supV, np.transpose(thisFit.coef_))

b = thisFit.support_vectors_[0]
yy_down = (b[1] - bSlope * b[0]) + bSlope * xx

b = thisFit.support_vectors_[-1]
yy_up = (b[1] - bSlope * b[0]) + bSlope * xx

cc = thisFit.support_vectors_

#%% 
print('---QUESTION 2B---') 

misclass  = 1 - metrics.accuracy_score(yTrain, y_predictClass)
print('Misclassification:', misclass)


#%%
print('---QUESTION 2C---') 

# plot the line, the points, and the nearest vectors to the plane
inter = thisFit.intercept_
co1 = thisFit.coef_[0][0]
co2 = thisFit.coef_[0][1]
x = np.linspace(-5, 5)
y = (-inter - co1*np.linspace(-5, 5))/co2
reds = trainData[trainData['_PredictedClass_'] == 0]
plt.scatter(reds['x'], reds['y'], c="red", label = 0)
blues = trainData[trainData['_PredictedClass_'] == 1]
plt.scatter(blues['x'], blues['y'], c = "blue", label = 1)
plt.plot(x, y, 
         color = 'black', linestyle = 'dotted')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Question 2c - SVM + hyperplane')
plt.grid(True)
plt.legend(title = "_PredictedClass_")
plt.show()


#%% 
print('---QUESTION 2D---')

# Convert to the polar coordinates -- from profs code
trainData['radius'] = np.sqrt(trainData['x']**2 + trainData['y']**2)
trainData['theta'] = np.arctan2(trainData['y'], trainData['x'])
def customArcTan (z):
    theta = np.where(z < 0.0, 2.0*np.pi+z, z)
    return (theta)
trainData['theta'] = trainData['theta'].apply(customArcTan)
reds = trainData[trainData['SpectralCluster'] == 0]
plt.scatter(reds['radius'], reds['theta'], c="red", label = 0)
blues = trainData[trainData['SpectralCluster'] == 1]
plt.scatter(blues['radius'], blues['theta'], c = "blue", label = 1)
plt.xlabel('radius')
plt.ylabel('theta')
plt.title('Question 2d - SVM + Polar')
plt.grid(True)
plt.legend(title = "Class")
plt.show()

#%% 
print('---QUESTION 2E---')

trainData['group'] = 3
trainData.loc[trainData['radius'] <= 2.5, 'group'] = 2
trainData.loc[(trainData['radius'] < 3) & (trainData['theta'] >= 2), 'group'] = 2
trainData.loc[(trainData['radius'] < 3.5) & (trainData['theta'] >= 3), 'group'] = 2
trainData.loc[(trainData['radius'] < 4) & (trainData['theta'] >= 4), 'group'] = 2
trainData.loc[(trainData['radius'] < 2) & (trainData['theta'] >= 3), 'group'] = 1
trainData.loc[(trainData['radius'] < 2.5) & (trainData['theta'] >= 4), 'group'] = 1
trainData.loc[(trainData['radius'] < 3) & (trainData['theta'] >= 5), 'group'] = 1
trainData.loc[(trainData['radius'] < 1.5) & (trainData['theta'] >= 6), 'group'] = 0
reds = trainData[trainData['group'] == 0]
plt.scatter(reds['radius'], reds['theta'], c="red", label = 0)
blues = trainData[trainData['group'] == 1]
plt.scatter(blues['radius'], blues['theta'], c = "blue", label = 1)
green = trainData[trainData['group'] == 2]
plt.scatter(green['radius'], green['theta'], c = "green", label = 2)
black = trainData[trainData['group'] == 3]
plt.scatter(black['radius'], black['theta'], c = "black", label = 3)
plt.xlabel('radius')
plt.ylabel('theta')
plt.title('Part e - SVM + Polar + new Group')
plt.grid(True)
plt.legend(title = "Class")
plt.show()

#%% 
print('---QUESTION 2F---') 

eqs = []
for gr in [(0,1), (1,2), (2,3)]:
    temp_df = trainData[trainData['group'].isin(gr)]
    tx_train = temp_df[['radius', 'theta']]
    ty_train = temp_df["group"]
    svmmodel = svm.SVC(kernel = "linear", 
                       decision_function_shape = "ovr",
                       random_state = 20200408)
    thisfit = svmmodel.fit(tx_train, ty_train)
    y_pred = thisfit.predict(tx_train)
    
    print(f"SVM {gr}")
    print("Intercept:", thisfit.intercept_)
    print("Coefficients:", thisfit.coef_)
    inter = thisfit.intercept_
    co1 = thisfit.coef_[0][0]
    co2 = thisfit.coef_[0][1]
    x = np.linspace(0, 4.5)
    y = (-inter - co1*x)/co2
    eqs.append((x, y))
    print('\n') 
        
#%% 
print('---QUESTION 2G---') 

reds = trainData[trainData['group'] == 0]
plt.scatter(reds['radius'], reds['theta'], c="red", label = 0)
blues = trainData[trainData['group'] == 1]
plt.scatter(blues['radius'], blues['theta'], c = "blue", label = 1)
green = trainData[trainData['group'] == 2]
plt.scatter(green['radius'], green['theta'], c = "green", label = 2)
black = trainData[trainData['group'] == 3]
plt.scatter(black['radius'], black['theta'], c = "black", label = 3)
for eq in eqs:
    plt.plot(eq[0], eq[1], 
         color = 'black', linestyle = 'dotted')
plt.xlabel('radius')
plt.ylabel('theta')
plt.title('Part g - SVM + Polar + new Group + hyperplane')
plt.grid(True)
plt.legend(title = "Class")
plt.show() 


#%% 
print("---QUESTION 2H---") 

ceqs = []
for eq in eqs:
    ceqs.append((eq[0]*np.cos(eq[1]), eq[0]*np.sin(eq[1])))
reds = trainData[trainData['SpectralCluster'] == 0]
plt.scatter(reds['x'], reds['y'], c="red", label = 0)
blues = trainData[trainData['SpectralCluster'] == 1]
plt.scatter(blues['x'], blues['y'], c = "blue", label = 1)
for eq in ceqs:
    plt.plot(eq[0], eq[1], 
         color = 'black', linestyle = 'dotted')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Part h - SVM + Polar-newGroup-hyperplane-cartesian')
plt.grid(True)
plt.legend(title = "Class")
plt.show() 

        
















