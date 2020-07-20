# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 19:21:23 2020

@author: HP

objectives :
    1.month in which the sell of product is more
    2.which product have selled most
    3.pair of products
    4.time of day when selling is high

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#reading the csv file
df = pd.read_csv('all_data.csv')

#removinf the nan values from the data set
df.dropna(inplace=True)
df.reset_index(drop=True,inplace=True)
i = df[((df.Product == 'product'))].index
df.drop(i,inplace=True)

#print the cleaned data
print(df.head())

#some date fields have the "or" as value hence to remove that part
df = df[df['Order Date'].str[0:2]!="Or"]

#converting object type to required type
df['Order Date']=pd.to_datetime(df['Order Date'])
df['Quantity Ordered']=pd.to_numeric(df['Quantity Ordered'])
df['Price Each']=pd.to_numeric(df['Price Each'])
#Adding sales Column
df['Sales']=df['Quantity Ordered']*df['Price Each']

#describing the dataframe after cahnges
print(df.info())

df['month'] = df['Order Date'].dt.month

#extracting required column of objective 1
df_month = df[['month','Quantity Ordered']]


#grouping the data according to the month
result_month=(df_month.groupby('month').sum())
result_month=result_month.reset_index()

#result of the groupby function
print("\nResult for the month and number of Quantity\n")
print(result_month)

df_day = df[['Sales']]
df_day['month'] = df['Order Date'].dt.month
#grouping the data according to the month
result_day=(df_day.groupby(['month']).sum())
result_day=result_day.reset_index()
result_day.to_csv(r'F:\college ppts\data science\monthproductsum.csv', index = False)

#extracting required column of objective 2
df_product = df[['Product','Quantity Ordered']]
result_product = (df_product.groupby('Product').sum())
result_product=result_product.reset_index()

#result of the groupby function
print("\nResult for the product and number of Quantity\n")
print(result_product)

#calculating the price of each product
df_price = df[['Price Each','Product']]
result_price = (df_price.groupby('Product').mean()) 
result_price=result_price.reset_index()

print("\nResult for the price and Product\n")
print(result_price)



#extracting required column of objective 2
df_time = df[['Quantity Ordered']]

df_time['hour'] = df['Order Date'].dt.hour
result_time = (df_time.groupby('hour').sum())
result_time = result_time.reset_index()

print("\nResult for the Time and number of Quantity\n")
print(result_time.head())

df_pair = df[['Product','Quantity Ordered']]
df_pair['hour'] = df_time['hour']

#top 3 selling products in a day with the time
result_top = df_pair.groupby(['hour','Product']).sum()
result_groups_top = result_top['Quantity Ordered'].groupby(level=0, group_keys=False)
print(result_groups_top.nlargest(3))



#taking the order Id and Product column from dataframe to df_best for getting the best pair
df_best = df[['Order ID','Product']]
#removing the orders with the single products
result_best_pair = df_best[df_best.groupby('Order ID')['Order ID'].transform('size')>1]
result_best_pair.reset_index()

#creating the pair of products
result_best_pair =result_best_pair.groupby('Order ID').agg(' , '.join)

#adding new column count to get the count of the paired order
result_best_pair['Count'] = 1
result_best_pair = result_best_pair[['Product','Count']] 

#grounping the data with Product column to get the pair counts and the sorting and taking the top 10 orders
result_best_pair=result_best_pair.groupby('Product').sum()
result_best_pair=result_best_pair.sort_values('Count',ascending = False).head(10)
result_best_pair.reset_index()
print(result_best_pair)

#printing the bar group of the data for visualization 
x=range(1,13)
y=result_month['Quantity Ordered']
plt.bar(x,y)
plt.xticks(x)
plt.title("Quantity Ordered Vs month")
plt.xlabel("month")
plt.ylabel("Quantity Ordered")
plt.show()

#printing the bar group of the data for visualization 
x=result_product['Product']
y=result_product['Quantity Ordered']
y2=result_price['Price Each']

fig,ax1 = plt.subplots()
ax2=ax1.twinx()
ax1.bar(x,y,color='#7cb342')
ax2.plot(x,y2,color='#455a64')

ax1.set_xticklabels(x,rotation = 'vertical')
ax1.set_title("Quantity Ordered Vs Product")
ax1.set_xlabel("Product")
ax1.set_ylabel("Quantity Ordered")

plt.show()


#printing the bar group of the data for visualization 
x=result_time['hour']
y=result_time['Quantity Ordered']
plt.bar(x,y,color='#ffc107')
plt.xticks(x)
plt.title("Quantity Ordered Vs time")
plt.xlabel("time")
plt.ylabel("Quantity Ordered")
plt.show()

