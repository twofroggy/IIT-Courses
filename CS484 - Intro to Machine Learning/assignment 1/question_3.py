##########################################
### CS484 Spring 2021
### Assignment 1
### Student ID: A20442087
### Tiffany Wong

##########################################

#load necessary libraries 
import pandas as pd
import numpy as np
from numpy import linalg as LA
from sklearn.neighbors import NearestNeighbors as kNN

#%% question 3a 
print("-- QUESTION 3a --")

#read in Fraud.csv into df
df = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 1/Fraud.csv')

#these conditionals result in a boolean variable that has T when the group matches its requirement
fraud_1 = df['FRAUD']==1

#use this as a boolean variable to filter the dataframe
df_1 = df[fraud_1] 

#print answer after division 
print((len(df_1)/len(df)*100), '% of investigations are found to be frauds')

#%% question 3b 
print("-- QUESTION 3b --")

# Input the matrix X and delete columns CASE_ID and FRAUD, because they aren't interval variables
x = np.matrix(df.iloc[:, 2:].values)

print("Input Matrix = \n", x)

print("Number of Dimensions = ", x.ndim)

xtx = x.transpose() * x
print("t(x) * x = \n", xtx)

# Eigenvalue decomposition
eigen_values, eigen_vectors = LA.eigh(xtx)
print("Eigenvalues of x = \n", eigen_values)
print("Eigenvectors of x = \n", eigen_vectors)

#check if the eigenvalues of all the interval variables are greater than 1
print("checking if eigenvalues are >1:", eigen_values > 1)

# Here is the transformation matrix
dvals = 1.0 / np.sqrt(eigen_values)
transf = eigen_vectors * np.diagflat(dvals)
print("Transformation Matrix = \n", transf)

# Here is the transformed X
transf_x = x * transf;
print("The Transformed x = \n", transf_x)

# Check columns of transformed X
xtx = transf_x.transpose() * transf_x;
print("Expect an Identity Matrix = \n", xtx)

#%% question 3c
print("-- QUESTION 3c --")

from sklearn.neighbors import KNeighborsClassifier as kNC

#specify the target: FRAUD = 1, not FRAUD = 0
target = df['FRAUD']

#use kNN module and specify that neighbors=5
neigh = kNC(n_neighbors = 5, algorithm = 'brute', metric = 'euclidean')

#training the model 
nbrs = neigh.fit(transf_x, target)

print("The score function gives me: ", nbrs.score(transf_x, target))


#%% question 3d
print("-- QUESTION 3d --")

# Find the nearest neighbors of these focal observations       
focal = [[7500, 15, 3, 127, 2, 2]]

#multiply focal matrix by the transformation matrix
t_focal = focal * transf;

##use kNN module and specify that neighbors=5
myNeighbors = nbrs.kneighbors(t_focal, n_neighbors = 5, return_distance = False)
print("My Neighbors = \n", myNeighbors)


#%% question 3e
print("-- QUESTION 3e --")

# See the classification probabilities
class_prob = nbrs.predict_proba(t_focal)
print(class_prob)


















