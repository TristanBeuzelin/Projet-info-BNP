import pandas as pd 
import numpy as np 
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt 

df_price = pd.read_csv("../../price_computed/average_prices.csv",sep = ";") 
header = df_price.columns
np_price = df_price.to_numpy()

prices = np_price[:,2:].astype(np.float64) #Conversion from string to float

df_ipc = pd.read_csv("ipc2014-21.csv", sep = ";").to_numpy() #IPC

IPC = df_ipc[:,1:].astype(np.float64) #Conversion from string to float

IPC = IPC[::-1] #Reading IPCs backward to get them chronogically

IPC_learn = IPC[:len(prices)] #IPCs used to learn
IPC_test = IPC[len(prices):]  #IPCs used to test the model



j_idx = [] #Index of first price release of each month

months_viewed = [] #List of month viewed

i = 2
while len(j_idx) < len(IPC_learn):
    date = header[i].split('-')[:2]
    
    i+= 1
    if date  not in months_viewed:
        months_viewed.append(date)
        j_idx.append(i)




prices_learn = df_price[[header[j] for j in j_idx]].to_numpy().T #Prices used to teach the model
price_test = df_price[[header[j+2] for j in range(len(header[2:])) if j+2 not in j_idx ]].to_numpy() #Prices to test the model
"""
# Random Forest Regression
Model = RandomForestRegressor()
N_list = np.arange(1, 40, 1)
tuned_parameters = {'n_estimators': N_list}
nb_folds = 5
grid = GridSearchCV(Model, tuned_parameters, cv=nb_folds, refit=True, verbose=3, scoring='r2')
grid.fit(prices_learn, IPC_learn.ravel())
print(grid.best_estimator_)
scores = grid.cv_results_['mean_test_score']
scores_std = grid.cv_results_['std_test_score']
Predict_test = grid.best_estimator_.predict(price_test.T)
Predict = grid.best_estimator_.predict(prices.T)
Predict2 = Predict.copy()
Predict2[-len(Predict_test):] = Predict_test
"""
"""
# Decision Tree Regression
Model = DecisionTreeRegressor()
depth_list = np.arange(5, 100, 1)
tuned_parameters = {'max_depth': depth_list}
nb_folds = 5
grid = GridSearchCV(Model, tuned_parameters, cv=nb_folds, refit=True, verbose=3, scoring='r2')
grid.fit(prices_learn, IPC_learn.ravel())
scores = grid.cv_results_['mean_test_score']
scores_std = grid.cv_results_['std_test_score']
Predict_test = grid.best_estimator_.predict(price_test.T)
Predict = grid.best_estimator_.predict(prices.T)
Predict2 = Predict.copy()
Predict2[-len(Predict_test):] = Predict_test
"""
"""
# Multi Layer Perceptron Regression
Model = MLPRegressor()
sizes_list = np.arange(50, 100, 5)
tuned_parameters = {'hidden_layer_sizes': sizes_list}
nb_folds = 5
grid = GridSearchCV(Model, tuned_parameters, cv=nb_folds, refit=True, verbose=3, scoring='r2')
grid.fit(prices_learn, IPC_learn.ravel())
print(grid.best_estimator_)
Predict_test = grid.best_estimator_.predict(price_test.T)
Predict = grid.best_estimator_.predict(prices.T)
Predict2 = Predict.copy()
Predict2[-len(Predict_test):] = Predict_test
"""
"""
# K Neighbors Regression
Model = KNeighborsRegressor()
n_list = np.arange(1, 31, 1)
tuned_parameters = {'n_neighbors': n_list}
nb_folds = 5
grid = GridSearchCV(Model, tuned_parameters, cv=nb_folds, refit=True, verbose=3, scoring='r2')
grid.fit(prices_learn, IPC_learn.ravel())
print(grid.best_estimator_)
Predict_test = grid.best_estimator_.predict(price_test.T)
Predict = grid.best_estimator_.predict(prices.T)
Predict2 = Predict.copy()
Predict2[-len(Predict_test):] = Predict_test
"""

# Gradient Boosting Regression
Model = GradientBoostingRegressor(learning_rate=0.65, n_estimators=15, max_depth=4, alpha=0.6, tol=0.07)
n_list = np.arange(0.1, 1, 0.1)
tuned_parameters = {'validation_fraction': n_list}
nb_folds = 5
grid = GridSearchCV(Model, tuned_parameters, cv=nb_folds, refit=True, verbose=3, scoring='r2')
grid.fit(prices_learn, IPC_learn.ravel())
print(grid.best_estimator_)
Predict_test = grid.best_estimator_.predict(price_test.T)
Predict = grid.best_estimator_.predict(prices.T)
Predict2 = Predict.copy()
Predict2[-len(Predict_test):] = Predict_test

IPC_dict = {} #Dictionnary containing each IPCs (values) for each month (keys)
for [date,ipc] in df_ipc:
    IPC_dict[date] = ipc 

Y_real = [] #IPCs of the month for each day in the month

for j,price in enumerate(prices.T): #Filling of Y_real
    date = header[j+2][:-3]
    if date in IPC_dict.keys():
        Y_real.append(IPC_dict[date])
    

plt.plot(np.arange(len(Y_real)),Y_real, label = "Real IPC")
plt.plot(np.arange(len(Predict)),Predict, label ="Prediction IPC")
plt.plot(np.arange(len(Predict2)),Predict2, label ="Second Prediction IPC")
plt.scatter(j_idx ,IPC_learn,c= 'r', label ="Learned IPC")
plt.xticks(np.arange(len(prices.T))[::100], header[2:][::100], rotation = 45)
plt.grid()
plt.legend()
plt.show()