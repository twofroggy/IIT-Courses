##########################################
### CS484 Spring 2021
### Assignment 5 
### Student ID: A20442087
### Tiffany Wong

########################################## 

#%% import libraries 
import graphviz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.ensemble as ensemble
import sklearn.tree as tree
import sklearn.metrics as metrics 
import treeFit

#%% question 1 - adaptive boosting technique: week 13 

# importing .csv files 

trainData = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 5/WineQuality_Train.csv', delimiter=',')
testData = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 5/WineQuality_Test.csv', delimiter = ',')
nObs = trainData.shape[0]

x_train = trainData[['alcohol','citric_acid','free_sulfur_dioxide','residual_sugar','sulphates']]
y_train = trainData['quality_grp']

x_test = testData[['alcohol','citric_acid','free_sulfur_dioxide','residual_sugar','sulphates']]
y_test = testData['quality_grp']


#%% part a and b
print('PART A & B')

# Build a classification tree on the training partition
w_train = np.full(nObs, 1.0)
accuracy = np.zeros(50)
misclassification = np.zeros(50)
ensemblePredProb = np.zeros((nObs, 2))
for iter in range(30):
    classTree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=20210415)
    treeFit = classTree.fit(x_train, y_train, w_train)
    treePredProb = classTree.predict_proba(x_train)
    accuracy[iter] = classTree.score(x_train, y_train, w_train)
    misclassification[iter] = 1 - accuracy[iter] 
    ensemblePredProb += accuracy[iter] * treePredProb        
    if (accuracy[iter] >= 0.9999999):
        break    
    # Update the weights
    eventError = np.where(y_train == 1, (1 - treePredProb[:,1]), (0 - treePredProb[:,1]))
    predClass = np.where(treePredProb[:,1] >= 0.2, 1, 0)
    w_train = np.where(predClass != y_train, 2 + np.abs(eventError), np.abs(eventError))
    if iter == 0 or iter == 1:
        print('at iter', iter, ', Misclassification Rate = ', misclassification[iter])

#%% part c
print('PART C') 

for iter in range(30):
    print('at iter', iter, ', Misclassification Rate = ', misclassification[iter]) 
    
#%% part d 
print('PART D')

y_score = treeFit.predict_proba(x_test)
AUC = metrics.roc_auc_score(y_test, y_score[:,1])
print('AUC = ', AUC) 

#%% part e 
print('PART E') 

bagPredProb = treeFit.predict_proba(x_test) 
testData['predict_proba_group_0'] = bagPredProb[:, 0] 
testData['predict_proba_group_1'] = bagPredProb[:, 1] 
testData.boxplot(column='predict_proba_group_1', by='quality_grp') 
plt.show() 

