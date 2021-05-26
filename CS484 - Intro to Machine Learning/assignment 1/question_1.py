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

#%% question 1a 
print('-- Question 1a --')

print(df.describe())

#%% question 1b
print('-- Question 1b --')

IQR = 32.4 - 30.4
N = 1001

#equation for Izenman (1991) method of bin width
h = 2*(IQR)*(N**(-1/3))
print('bin width using Izenman method is:', h)

#%% question 1c
print('-- Question 1c --')

Y = df['x']
def calcCD (Y, delta):
   maxY = np.max(Y)
   minY = np.min(Y)
   meanY = np.mean(Y)

   # Round the mean to integral multiples of delta
   middleY = delta * np.round(meanY / delta)

   # Determine the number of bins on both sides of the rounded mean
   nBinRight = np.ceil((maxY - middleY) / delta)
   nBinLeft = np.ceil((middleY - minY) / delta)
   lowY = middleY - nBinLeft * delta

   # Assign observations to bins starting from 0
   m = nBinLeft + nBinRight
   BIN_INDEX = 0;
   boundaryY = lowY
   for iBin in np.arange(m):
      boundaryY = boundaryY + delta
      BIN_INDEX = np.where(Y > boundaryY, iBin+1, BIN_INDEX)

   # Count the number of observations in each bins
   uBin, binFreq = np.unique(BIN_INDEX, return_counts = True)

   # Calculate the average frequency
   meanBinFreq = np.sum(binFreq) / m
   ssDevBinFreq = np.sum((binFreq - meanBinFreq)**2) / m
   CDelta = (2.0 * meanBinFreq - ssDevBinFreq) / (delta * delta)
   return(m, middleY, lowY, CDelta)

result = pd.DataFrame()
deltaList = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0]

for d in deltaList:
   nBin, middleY, lowY, CDelta = calcCD(Y,d)
   highY = lowY + nBin * d
   result = result.append([[d, CDelta, lowY, middleY, highY, nBin]], ignore_index = True)

result = result.rename(columns = {0:'Delta', 1:'C(Delta)', 2:'Low Y', 3:'Middle Y', 
                                  4:'High Y', 5:'N Bin'})
print(result)

#%% question 1d 
print('-- Question 1d --')

#declare variables for bin-width, max, and min
h = 1
mid_point = [e + h/2 for e in np.arange(26,37,h)][:-1]
density = plt.hist(x=Y, bins=np.arange(26,37,h), density=True)
plt.xlabel("x values")
plt.ylabel("Density")
plt.title("Histogram with bin-width: 1")
plt.show()

#store the density values into an array 
den_values = []
for i in range(len(mid_point)):
    den_values.append((np.round(density[0][i], 5)))
    
#combine midppoint array and density array into one dataframe
df = pd.DataFrame({'midpoints': mid_point, 'estimated density function values': den_values})

print(df)





