##########################################
### CS484 Spring 2021
### Assignment 2
### Student ID: A20442087
### Tiffany Wong

##########################################

#%% question 4 info
# Suppose Cluster 0 contains observations {-2, -1, 1, 2, 3} and Cluster 1 
# contains observations {4, 5, 7, 8}

#%% question 4a (for loop method)
print("---QUESTION 4A---")

# Calculate the Silhouette Width of the observation 2 (i.e., the value -1) 
# in Cluster 0.

import math 
import numpy as np

# a: The mean distance between a sample and all other points in the same class.
# b: The mean distance between a sample and all other points in the next nearest cluster.

X = [-2, -1, 1, 2, 3] 
Y = [4, 5, 7, 8] 

a_all = []
b_all= []

for i in X:
    a_all.append(abs(X[1]-i))
    
a = sum(a_all)/(len(a_all)-1)

for j in Y:
    b_all.append(abs(X[1]-j))
    
b = np.mean(b_all)

silhouette_value = (b-a)/(max(a,b))

print('The Silhouette Width of the observation 2 in Cluster 0 is', silhouette_value)


#%% question 4b (cluster-wise Davies-Bouldin value)
print("---QUESTION 4B---")

# Calculate the cluster-wise Davies-Bouldin value of Cluster 0 (i.e., R_0) and 
# Cluster 1 (i.e., R_1). 

from sklearn.neighbors import NearestCentroid

# intra-cluster is distances between other pts in the same cluster: a_all
# inter-cluster is distances to other pts in diff cluster: b_all 

# array of observations
X = [-2, -1, 1, 2, 3] 
Y = [4, 5, 7, 8] 

# array of distances 
X_distances = []
Y_distances = []

# cluster centroids
# centroid for X is 1
centroid0 = sum(X)/len(X)
# centroid for Y is between 5 and 7
centroid1 = sum(Y)/len(Y)

# distances for X
for i in X: 
    X_distances.append(abs(i-centroid0))

# distances for Y
for i in Y: 
    Y_distances.append(abs(i-centroid1))

# intra cluster dist for X
s_k_x = (1/(len(X)))*(sum(X_distances))

# intra cluster dist for Y 
s_k_Y = (1/(len(Y)))*(sum(Y_distances))

print('cluster 0:', s_k_x, 'cluster 1:', s_k_Y)

#%% question 4c (Davies-Bouldin index)
print("---QUESTION 4C---")

m_kl = abs(centroid0 - centroid1)

r_kl = (s_k_x + s_k_Y) / m_kl 

print('Davies-Bouldin Index:', r_kl / 2) 










































