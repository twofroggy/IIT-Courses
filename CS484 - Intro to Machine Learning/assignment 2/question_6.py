##########################################
### CS484 Spring 2021
### Assignment 2
### Student ID: A20442087
### Tiffany Wong

##########################################

#%% question 6 info
# You are asked to discover the optimal clusters in the cars.csv.  
# Here are the specifications.
#   The input interval variables are Weight, Wheelbase, and Length
#   Scale each input interval variable such that the resulting variable has a 
#       range of 0 to 10
#   The distance metric is Manhattan
#   The minimum number of clusters is 2
#   The maximum number of clusters is 10
#   Specify random_state = 60616 in calling the KMeans function in 
#       scikit-learn library


#%% question 6a
print('---QUESTION 6A---')

import pandas as pd
import numpy as np
from sklearn import preprocessing 
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


# List the Elbow values, the Silhouette values, the Calinski-Harabasz Scores, 
# and the Davies-Bouldin Indices for your 2-cluster to 10-cluster solutions. 

# read in csv file
df1 = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 2/cars.csv') 
df = df1[['Weight', 'Wheelbase', 'Length']]

# create an array for the min to max # of clusters 
clusters = np.array(range(2,11))

# # convert df to array
# df = df2.to_numpy()

# scale each input interval variable so that the results are (0,10) 
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,10)) 
df_scaled = min_max_scaler.fit_transform(df) 
# print(df_scaled)

import sklearn.cluster as cluster
import sklearn.metrics as metrics
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

nObs = df_scaled.shape[0]

# Determine the number of clusters
maxNClusters = 10
minNClusters = 2

nClusters = np.zeros(maxNClusters)
Elbow = np.zeros(maxNClusters)
Silhouette = np.zeros(maxNClusters)
Calinski_Harabasz = np.zeros(maxNClusters)
Davies_Bouldin = np.zeros(maxNClusters)
TotalWCSS = np.zeros(maxNClusters)
Inertia = np.zeros(maxNClusters)

for c in range(maxNClusters):
   KClusters = c + 1
   nClusters[c] = KClusters

   kmeans = cluster.KMeans(n_clusters=KClusters, random_state=60616).fit(df_scaled)
   
   unscaled_kmeans = cluster.KMeans(n_clusters=KClusters, random_state=60616).fit(df)
   
   # The Inertia value is the within cluster sum of squares deviation from the centroid
   Inertia[c] = kmeans.inertia_
   
   calinski_harabasz_score
   
   if (1 < KClusters):
       Silhouette[c] = metrics.silhouette_score(df_scaled, kmeans.labels_, metric='manhattan')
       Calinski_Harabasz[c] = metrics.calinski_harabasz_score(df_scaled, kmeans.labels_)
       Davies_Bouldin[c] = metrics.davies_bouldin_score(df_scaled, kmeans.labels_)
   else:
       Silhouette[c] = np.NaN
       Calinski_Harabasz[c] = np.NaN
       Davies_Bouldin[c] = np.NaN

   WCSS = np.zeros(KClusters)
   nC = np.zeros(KClusters)

   for i in range(nObs):
      k = kmeans.labels_[i]
      nC[k] += 1
      diff = df_scaled[i] - kmeans.cluster_centers_[k]
      WCSS[k] += diff.dot(diff)

   Elbow[c] = 0
   for k in range(KClusters):
      Elbow[c] += WCSS[k] / nC[k]
      TotalWCSS[c] += WCSS[k]

   print("Cluster Assignment:", kmeans.labels_)
   for k in range(KClusters):
      print("Cluster ", k)
      print("Centroid = ", kmeans.cluster_centers_[k])
      print("Unscaled Centroid = ", unscaled_kmeans.cluster_centers_[k])
      print("Size = ", nC[k])
      print("Within Sum of Squares = ", WCSS[k])
      print(" ")

# delete row of 0's 
nClusters = np.delete(nClusters, 0) 
Elbow = np.delete(Elbow, 0) 
Silhouette = np.delete(Silhouette, 0) 
Calinski_Harabasz = np.delete(Calinski_Harabasz, 0) 
Davies_Bouldin = np.delete(Davies_Bouldin, 0) 

# List the Elbow values, the Silhouette values, the Calinski-Harabasz Scores, 
# and the Davies-Bouldin Indices for your 2-cluster to 10-cluster solutions. 
print("N Clusters\t Elbow\t Silhouette\t Calinski_Harabasz\t Davies_Bouldin")
for c in range(maxNClusters-1):
   print('{:.0f} \t \t \t {:.4f} \t \t {:.4f} \t \t {:.4f} \t \t {:.4f}'
         .format(nClusters[c], Elbow[c], Silhouette[c], Calinski_Harabasz[c], Davies_Bouldin[c]))

# Elbow plot
plt.plot(nClusters, Elbow, linewidth = 2, marker = 'o')
plt.grid(True)
plt.xlabel("Number of Clusters")
plt.ylabel("Elbow Value")
plt.xticks(np.arange(minNClusters, maxNClusters+1, step = 1))
plt.show()

#Silhouette plot
plt.plot(nClusters, Silhouette, linewidth = 2, marker = 'o')
plt.grid(True)
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Value")
plt.xticks(np.arange(minNClusters, maxNClusters+1, step = 1))
plt.show()  

# Calinski_Harabasz plot
plt.plot(nClusters, Calinski_Harabasz, linewidth = 2, marker = 'o')
plt.grid(True)
plt.xlabel("Number of Clusters")
plt.ylabel("Calinski-Harabasz Score")
plt.xticks(np.arange(minNClusters, maxNClusters+1, step = 1))
plt.show()

# Davies_Bouldin plot
plt.plot(nClusters, Davies_Bouldin, linewidth = 2, marker = 'o')
plt.grid(True)
plt.xlabel("Number of Clusters")
plt.ylabel("Davies-Bouldin Index")
plt.xticks(np.arange(minNClusters, maxNClusters+1, step = 1))
plt.show()   

#%% question 6b
print('---QUESTION 6B---') 

print('Based on the values in (a), my suggested number of clusters is 3 clusters.')