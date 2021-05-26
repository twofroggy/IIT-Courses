##########################################
### CS484 Spring 2021
### Assignment 3
### Student ID: A20442087
### Tiffany Wong

########################################## 
#%% 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math

from sklearn import metrics

from itertools import combinations

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt


#%% 

df = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 3/claim_history.csv') 

from sklearn.model_selection import train_test_split
features = df[["CAR_TYPE","OCCUPATION","EDUCATION"]]

#Split for training and testing data
features_train, features_test, labels_train, labels_test = train_test_split(features, 
                                                                            df["CAR_USE"], 
                                                                            test_size = 0.3, 
                                                                            random_state=27513, 
                                                                            stratify = df["CAR_USE"]) 


#%% 

cross_Table_Train = pd.crosstab(labels_train, columns =  ["Count"], 
                                margins=True, dropna=True)
cross_Table_Train["Proportions"] = (cross_Table_Train["Count"] / 
                                    len(labels_train)) * 100
print(cross_Table_Train) 

cross_Table_test = pd.crosstab(labels_test, columns =  ["Count"], 
                               margins=True, dropna=True)
cross_Table_test["Proportions"] = (cross_Table_test["Count"] / 
                                   len(labels_test)) * 100
print(cross_Table_test)



#%% P ( Train | Car Use = Commercial )

c=0

#Probability of the observation in Training set
prob_train = len(features_train) / len(df["CAR_USE"]) 

for i in df["CAR_USE"]: 
    #Probability of the observation being Commercial 
    if i == "Commercial":
        c+=1        
        
#Probability that observation is in the Training partition given that CAR_USE = Commercial
(prob_train * c / len(df["CAR_USE"])) / (c / len(df["CAR_USE"]))   

print("The probability that an observation is in the Training partition given that CAR_USE = Commercial is",(prob_train*c/10302)/(c/10302))


#%% P ( Test | Car Use = Private ) 

count=0

#Probability of the observation in Testing set
prob_test = len(features_test) / len(df["CAR_USE"]) 

for i in df["CAR_USE"]:
    if i == "Private":
        #Probability of the observation being Private
        count+=1        
(prob_test*count/10302) / (count/10302)   #Probability that observation is in the Testing partition given that CAR_USE = Private

print("The probability that an observation is in the Testing partition given that CAR_USE = Private is", (prob_test*count/10302)/(count/10302))


#%% 

features_train["Labels"] = labels_train 

#%% Entropy of Root Node


cnt = 0
for i in df["CAR_USE"]:
    if i == "Commercial":
        cnt+=1
proba_commercial = cnt/len(df["CAR_USE"])

proba_private = (len(df["CAR_USE"])-cnt)/len(df["CAR_USE"])

ans = -((proba_commercial * np.log2(proba_commercial) + proba_private * np.log2(proba_private)))
print("Entropy for root node is given as",ans) 


#%% All possible combinations for occupation 

occupation_column = df["OCCUPATION"].unique()
occupation_combinations = []
for i in range(1,math.ceil(len(occupation_column)/2)):
    occupation_combinations+=list(combinations(occupation_column,i))


#%% All possible combinations for car type

car_type_column = df["CAR_TYPE"].unique()
car_type_combinations = []

for i in range(1,math.ceil(len(car_type_column)/2)+1):
    x = list(combinations(car_type_column,i))
    if i == 3:
        x = x[:10]
    car_type_combinations.extend(x) 


#%% All possible combinations for education

education_combinations = [("Below High School",), 
                          ("Below High School","High School",), 
                          ("Below High School","High School","Bachelors",), 
                          ("Below High School","High School","Bachelors","Masters",)] 

#%% entropy interval split function 

def EntropyIntervalSplit (
   inData,          # input data frame (predictor in column 0 and target in column 1)
   split):          # split value

   #print(split)
   dataTable = inData
   dataTable['LE_Split'] = False
   for k in dataTable.index:
       if dataTable.iloc[:,0][k] in split:
           dataTable['LE_Split'][k] = True
   #print(dataTable['LE_Split'])
   crossTable = pd.crosstab(index = dataTable['LE_Split'], columns = dataTable.iloc[:,1], margins = True, dropna = True)   
   #print(crossTable)

   nRows = crossTable.shape[0]
   nColumns = crossTable.shape[1]
   
   tableEntropy = 0
   for iRow in range(nRows-1):
      rowEntropy = 0
      for iColumn in range(nColumns):
         proportion = crossTable.iloc[iRow,iColumn] / crossTable.iloc[iRow,(nColumns-1)]
         if (proportion > 0):
            rowEntropy -= proportion * np.log2(proportion)
      #print('Row = ', iRow, 'Entropy =', rowEntropy)
      #print(' ')
      tableEntropy += rowEntropy *  crossTable.iloc[iRow,(nColumns-1)]
   tableEntropy = tableEntropy /  crossTable.iloc[(nRows-1),(nColumns-1)]
  
   return(tableEntropy)

#%% min_entropy function 

def calculate_min_entropy(df,variable,combinations):
    inData1 = df[[variable,"Labels"]]
    entropies = []
    for i in combinations:
        EV = EntropyIntervalSplit(inData1, list(i))
        entropies.append((EV,i))
    return min(entropies)

#%% find best split for occupation 

print('OCCUPATION optimal split')

entropy_occupation = calculate_min_entropy(features_train, 
                                           "OCCUPATION", 
                                           occupation_combinations)

print(entropy_occupation)

#%% values for occupation

df_1_left = features_train[(features_train["OCCUPATION"] == "Blue Collar") | 
                           (features_train["OCCUPATION"] == "Unknown") | 
                           (features_train["OCCUPATION"] == "Student")]

df_1_right =  features_train[(features_train["OCCUPATION"] != "Blue Collar") &
                             (features_train["OCCUPATION"] != "Unknown") & 
                             (features_train["OCCUPATION"] != "Student")]


print('values = [', len(df_1_right), ',', len(df_1_left), ']') 

#%% best split for car type 

print('CAR_TYPE optimal split')

entropy_cartype = calculate_min_entropy(features_train, 
                                        "CAR_TYPE", 
                                        car_type_combinations)

print(entropy_cartype) 

#%% values for car_type

df_ct1_left = features_train[(features_train["CAR_TYPE"] == "Minivan") | 
                           (features_train["CAR_TYPE"] == "SUV") | 
                           (features_train["CAR_TYPE"] == "Sports Car")]

df_ct1_right =  features_train[(features_train["CAR_TYPE"] != "Minivan") &
                             (features_train["CAR_TYPE"] != "SUV") & 
                             (features_train["CAR_TYPE"] != "Sports Car")]


print('values = [', len(df_ct1_right), ',', len(df_ct1_left), ']') 

#%% best split for education 

print('EDUCATION optimal split')

entropy_education = calculate_min_entropy(features_train, 
                                          "EDUCATION", 
                                          education_combinations)

print(entropy_education)

#%% values for education

df_edu1_left = features_train[(features_train["EDUCATION"] == "Below High School")]

df_edu1_right =  features_train[(features_train["EDUCATION"] != "Below High School")] 

print('values = [', len(df_edu1_right), ',', len(df_edu1_left), ']') 

#%% entropy calculations for left split if OCCUPATION picked 

left_edu_entropy = calculate_min_entropy(df_1_left, 
                                         "EDUCATION", 
                                         education_combinations)

print(left_edu_entropy)

left_ct_entropy = calculate_min_entropy(df_1_left, 
                                        "CAR_TYPE", 
                                        car_type_combinations)

print(left_ct_entropy) 

#%% entropy calculations for left split if CAR_TYPE picked 

# leftct1_edu_entropy = calculate_min_entropy(df_ct1_left, 
#                                          "EDUCATION", 
#                                          education_combinations)

# print(leftct1_edu_entropy)

# leftct1_occu_entropy = calculate_min_entropy(df_ct1_left, 
#                                         "OCCUPATION", 
#                                         occupation_combinations)

# print(leftct1_occu_entropy) 

#%% entropy calculations for left split if EDUCATION picked 

# leftedu1_ct_entropy = calculate_min_entropy(df_edu1_left, 
#                                          "CAR_TYPE", 
#                                          car_type_combinations)

# print(leftedu1_ct_entropy)

# leftedu1_occu_entropy = calculate_min_entropy(df_edu1_left, 
#                                         "OCCUPATION", 
#                                         occupation_combinations)

# print(leftedu1_occu_entropy) 


#%% get new combinations 

occupation_column = ['Blue Collar', 'Unknown', 'Student'] 

occupation_combinations = [] 

for i in range(1,math.ceil(len(occupation_column)/2)):
    occupation_combinations+=list(combinations(occupation_column,i))

left_occupation_entropy = calculate_min_entropy(df_1_left,"OCCUPATION",occupation_combinations)

print(occupation_combinations)


#%% entropy calculations for right split

occupation_column = ['Professional', 'Manager', 'Clerical', 'Doctor','Lawyer','Home Maker']
occupation_combinations = []
for i in range(1,math.ceil(len(occupation_column)/2)):
    occupation_combinations+=list(combinations(occupation_column,i))
right_occupation_entropy = calculate_min_entropy(df_1_right,"OCCUPATION",occupation_combinations)


right_edu_entropy = calculate_min_entropy(df_1_right,"EDUCATION",education_combinations)
right_ct_entropy = calculate_min_entropy(df_1_right,"CAR_TYPE",car_type_combinations)

print(right_ct_entropy , right_edu_entropy , right_occupation_entropy) 


#%% values for the diff nodes in the first level nodes 

df_2_left_left = df_1_left[(features_train["EDUCATION"] == "Below High School")]
df_2_left_right = df_1_left[(features_train["EDUCATION"] != "Below High School")]

print('Left branch') 
print('samples =', len(df_2_left_left)+len(df_2_left_left)) 
print('values = [', len(df_2_left_left), ',', len(df_2_left_right), ']')  

#%% second level of nodes started 

cnt = 0
for i in df_2_left_left["Labels"]:
    if i == "Commercial":
        cnt+=1
proba_commercial = cnt/len(df_2_left_left["Labels"])
print("Count of commercial and private is",cnt, 
      (len(df_2_left_left)-cnt), 
      "respectively and probability of the event", 
      proba_commercial, 1-proba_commercial)


#%% 

cnt = 0
for i in df_2_left_right["Labels"]:
    if i == "Commercial":
        cnt+=1
proba_commercial = cnt/len(df_2_left_right["Labels"])
print("Count of commercial and private is",cnt, 
      (len(df_2_left_right)-cnt), 
      "respectively and probability of the event", 
      proba_commercial, 1-proba_commercial)


#%% 

df_2_right_left = df_1_right[(features_train["CAR_TYPE"] == "Minivan") | 
                             (features_train["CAR_TYPE"] == "Sports Car") | 
                             (features_train["CAR_TYPE"] == "SUV")]

df_2_right_right = df_1_right[(features_train["CAR_TYPE"] != "Minivan") & 
                              (features_train["CAR_TYPE"] != "Sports Car") & 
                              (features_train["CAR_TYPE"] != "SUV")] 

print('values = [', len(df_2_right_left), ',', len(df_2_right_right), ']') 

#%% 

cnt = 0
for i in df_2_right_left["Labels"]:
    if i == "Commercial":
        cnt+=1
proba_commercial = cnt/len(df_2_right_left["Labels"])
1-proba_commercial
print("Count of commercial and private is",cnt, 
      (len(df_2_right_left)-cnt), 
      "respectively and probability of the event", 
      proba_commercial, 1-proba_commercial)


#%% 

cnt = 0
for i in df_2_right_right["Labels"]:
    if i == "Commercial":
        cnt+=1
proba_commercial = cnt/len(df_2_right_right["Labels"])
proba_commercial
print("Count of commercial and private is",cnt, 
      (len(df_2_right_right)-cnt), 
      "respectively and probability of the event", 
      proba_commercial, 1-proba_commercial)














