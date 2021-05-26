##########################################
### CS484 Spring 2021
### Assignment 1
### Student ID: A20442087
### Tiffany Wong

##########################################

#load necessary libraries 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read in NormalSample.csv into df
df = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 1/NormalSample.csv')

X = df['x']

#%% question 2a 
print('-- Question 2a --')

#these conditionals result in a boolean variable that has T when the group matches its requirement
is_0 = df['group']==0
is_1 = df['group']==1

#use this as a boolean variable to filter the dataframe
df_0 = df[is_0]
df_1 = df[is_1] 

#grab only the x values to do five number summaries on
Y_0 = df_0['x']
Y_1 = df_1['x']

print('five-number summary for when group=0')
print(Y_0.describe())

print('five-number summary for when group=1')
print(Y_1.describe())

IQR_0 = (30.6 - 29.4)
upper_0 = Y_0.quantile([0.75]) + (1.5*IQR_0)
lower_0 = Y_0.quantile([0.25]) - (1.5*IQR_0)

IQR_1 = (32.7 - 31.4)
upper_1 = Y_1.quantile([0.75]) + (1.5*IQR_1)
lower_1 = Y_1.quantile([0.25]) - (1.5*IQR_1)

print('group = 0: upper whisker = ', int(upper_0), ', lower whisker = ', int(lower_0))
print('group = 1: upper whisker = ', int(upper_1), ', lower whisker = ', int(lower_1))

#%% question 2b
print('-- Question 2b --')
print('box plot of original x-values, group=0 x-values, and group=1 x-values')

#convert series to dataframe (commented out because only needed once)
newY_0 = Y_0.to_frame()
newY_1 = Y_1.to_frame()


newY_0 = newY_0.rename(columns = {'x': 'group_0 x'}) 
newY_1 = newY_1.rename(columns = {'x': 'group_1 x'}) 

#concat the array into one dataframe
all_x = pd.concat([X, newY_0, newY_1], axis=1)

all_x.boxplot(column=['x', 'group_0 x', 'group_1 x'], vert=False)
plt.title("Boxplot of All x-values, Group=0 x-values, and Group=1 x-values")
plt.show()


