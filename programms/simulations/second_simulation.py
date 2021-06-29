import pandas as pd 
import numpy as np 
import os 
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeRegressor
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

DT_model = DecisionTreeRegressor(max_depth=5).fit(prices_learn,IPC_learn)
DT_predict_test = DT_model.predict(price_test.T)
DT_predict = DT_model.predict(prices.T)
DT_predict2 = DT_predict.copy()
DT_predict2[-len(DT_predict_test):] = DT_predict_test

IPC_dict = {} #Dictionnary containing each IPCs (values) for each month (keys)

for [date,ipc] in df_ipc:
    IPC_dict[date] = ipc 

Y_real = [] #IPCs of the month for each day in the month

for j,price in enumerate(prices.T): #Filling of Y_real
    date = header[j+2][:-3]
    if date in IPC_dict.keys():
        Y_real.append(IPC_dict[date])
    

plt.plot(np.arange(len(Y_real)),Y_real, label = "Real IPC")
plt.plot(np.arange(len(DT_predict)),DT_predict, label ="Prediction IPC")
plt.plot(np.arange(len(DT_predict2)),DT_predict2, label ="Second Prediction IPC")
plt.scatter(j_idx ,IPC_learn,c= 'r', label ="Learned IPC")
plt.xticks(np.arange(len(prices.T))[::100], header[2:][::100], rotation = 45)
plt.grid()
plt.legend()
plt.show()