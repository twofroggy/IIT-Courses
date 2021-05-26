##########################################
### CS484 Spring 2021
### Assignment 2
### Student ID: A20442087
### Tiffany Wong

##########################################

#%% question 5a 
print("---QUESTION 5A---")

import pandas as pd 
from mlxtend.preprocessing import TransactionEncoder 

GroceriesAssoc = pd.read_csv('/Users/tiffwong/Desktop/cs484/assignments/assignment 2/Groceries.csv',
                           delimiter=',')

customers = max(GroceriesAssoc['Customer']) 

# Convert the Groceries data to the Item List format
ListItem = GroceriesAssoc.groupby(['Customer'])['Item'].apply(list).values.tolist()

# Convert the Item List format to the Item Indicator format
te = TransactionEncoder()
te_ary = te.fit(ListItem).transform(ListItem)
ItemIndicator = pd.DataFrame(te_ary, columns=te.columns_)

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Find the frequent itemsets
frequent_itemsets = apriori(ItemIndicator, min_support = 75 / len(ListItem), 
                            max_len = None, use_colnames = True)

itemsets = len(frequent_itemsets) 
print(f"{itemsets} itemsets")
largest_k = len(frequent_itemsets['itemsets'][itemsets - 1])
print(f"Largest k: {largest_k}")

#%% question 5b 
print("---QUESTION 5B---")

# Discover the association rules
assoc_rules = association_rules(frequent_itemsets, metric = "confidence", min_threshold = 0.01)

print(f"{len(assoc_rules)} Association rules")

#%% question 5c 
print("---QUESTION 5C---")

import matplotlib.pyplot as plt

plt.figure(figsize=(6,4))
plt.scatter(assoc_rules['confidence'], assoc_rules['support'], \
            c = assoc_rules['lift'], s = assoc_rules['lift'])
plt.grid(True) 
plt.xlabel("Confidence")
plt.ylabel("Support")
plt.title("Support vs Confidence")
colorgradient = plt.colorbar()
colorgradient.set_label("Lift")
plt.show()

#%% question 5d 
print("---QUESTION 5D---")

assoc_rules2 = association_rules(frequent_itemsets, metric = "confidence", min_threshold = 0.6)

print(assoc_rules2.head)


























