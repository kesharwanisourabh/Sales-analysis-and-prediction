# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:09:30 2020

@author: Sourabh kesharwani 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

#read the csv file in df as dataframe 
df = pd.read_csv('F:\college ppts\data science\dayproductsum.csv')
#extract the required columns here we have taken month,Sales,day
df=df[['month','Sales','day']]
print("\nCorrelation matrix")
print(df.corr())
print("\nNUll Values")
print(df.isnull().sum())
#define the dependent(Y) and independent(X) variable 
X=df[['month','day']]
Y=df['Sales']

#spliting the dataset in 25% (75% to train the model and 25% to test the model)
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 0.25,random_state = 40)

#creating the polynomial model with degree 6
poly = PolynomialFeatures(degree=6)
X_ = poly.fit_transform(X_train)
predict_ = poly.fit_transform(X_test)
clf = linear_model.LinearRegression()
#fitting the model with train dataset
clf.fit(X_, Y_train)
#predicting the value with the trained dataset
Y_predict = clf.predict(predict_) 


#calculating rsq value and the standard error
err = Y_test-Y_predict

est = sm.OLS(Y,X)
est2 = est.fit()
print(est2.summary())

#residue plot with the independent variable
plt.scatter(Y_predict,err,alpha=0.7)
plt.ylabel("Residue")
plt.xlabel("Predicted Value")
plt.title("Residual plot")

'''
print("\nPredict the sale")
predict_ = poly.fit_transform([[12,25]])
Y_predict = clf.predict(predict_) 
print(Y_predict)
'''