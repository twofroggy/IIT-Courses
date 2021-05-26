##########################################
### CS484 Spring 2021
### Assignment 1
### Student ID: A20442087
### Tiffany Wong

##########################################

#load necessary libraries 

from numpy import linalg as LA
from sklearn.neighbors import NearestNeighbors as kNN

#%% question 4a
print("-- QUESTION 4a --")
print("plot of Airport 2 vs Airport 3")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#read in the airport data as a csv file made on my own laptop
df = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 1/airport.csv')

#use seaborn to plot airport 2 vs airport 3
sns.scatterplot(data=df, x='Airport 2', y='Airport 3')

#change title and axis labels 
plt.title('Flights from Airport 2 and Airport 3')
plt.xlabel("Flights from Airport 2")
plt.ylabel("Flights from Airport 3")
plt.show()

#%% question 4b 
print("-- QUESTION 4b --")

#pull out airport 2 and 3 columns from df
a_2 = df['Airport 2'] 
a_3 = df['Airport 3'] 

#combine the two diff airport dfs in an array and then use concat to make a df
combine = [a_2, a_3]
a_2_3 = pd.concat(combine)

#change to dataframe
df_2_3 = a_2_3.to_frame()

#rename column to airport code
df_2_3.columns = ['Airport Code']

#use crosstab function to get a frequency count of each airport code
#freq = pd.crosstab(index=df_2_3['Airport Code'], columns='count')

#frequency count and convert to df and then rename to count 
frequency = df_2_3['Airport Code'].value_counts().to_frame()
frequency.columns = ['Count']

print('frequency table of airport codes in Airport 2 and Airport 3 \n', frequency)

#%% question 4c 
print("-- QUESTION 4c --")

import numpy as np

#get unique airport codes from airport 2 and 3
codes = df_2_3['Airport Code'].unique()

#create an empty vector in the df from the csv file
df['vectors'] = np.empty((len(df),0)).tolist()

#loop thru the len of the df and the codes 
for i in range(len(df)): 
    for code in codes: 
        count = 0
        if df['Airport 2'][i] == code:
            count += 1
        if df['Airport 3'][i] == code:
            count += 1
        df['vectors'][i].append(count)
        
print("Flights and their vectors: ") 
print(df)

#given Cosine function
def CosineD (x, y):
    normX = np.sqrt(np.dot(x, x)) 
    normY = np.sqrt(np.dot(y, y)) 
    if (normX > 0.0 and normY > 0.0):
        outDistance = 1.0 - np.dot(x, y) / normX / normY
    else:
        outDistance = np.NaN 
    return (outDistance) 
            
#create new array for the new flight
new_f = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]

#create a column for cosine values to be put in
df['cosine'] = np.empty((len(df),0)).tolist()

#for loop to calcualte the cosine distance from vector to new_f and store in df
for i in range(len(df)): 
    df['cosine'][i] = CosineD(df['vectors'][i], new_f)

print("Flights and their cosine distance from new flight: ")
print(df)















    


