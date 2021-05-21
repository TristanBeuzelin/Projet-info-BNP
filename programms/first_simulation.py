import pandas as pd 
import numpy as np 
import os 
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt 

df_price = pd.read_csv("./price_computed/average_prices.csv",sep = ";")
header = df_price.columns
np_price = df_price.to_numpy()

prices = np_price[:,2:].astype(np.float64)

df_ipc = pd.read_csv("ipc2014-21.csv", sep = ";").to_numpy()
IPC = df_ipc[:,1:].astype(np.float64)
IPC = IPC[::-1]
IPC_learn = IPC[:len(prices)]
IPC_test = IPC[len(prices):]



j_idx = []
months_viewed = []
i = 2
while len(j_idx) < len(IPC_learn):
    date = header[i].split('-')[:2]
    
    i+= 1
    if date  not in months_viewed:
        months_viewed.append(date)
        j_idx.append(i)




prices_learn = df_price[[header[j] for j in j_idx]].to_numpy()
price_test = df_price[[header[j+2] for j in range(len(header[2:])) if j+2 not in j_idx ]].to_numpy()


coeffs = np.matmul(np.linalg.inv(prices_learn.T),IPC_learn)



IPC_dict = {}

for [date,ipc] in df_ipc:
    IPC_dict[date] = ipc



Y_real = []
Y_test = np.matmul(prices.T,coeffs)
Y_learn = np.matmul(prices_learn.T,coeffs)

for j,price in enumerate(prices.T):
    date = header[j+2][:-3]
    if date in IPC_dict.keys():
        Y_real.append(IPC_dict[date])
    

plt.plot(np.arange(len(Y_real)),Y_real, label = "Real IPC")
plt.plot(np.arange(len(Y_test)),Y_test, label ="Prediction IPC")

plt.scatter(j_idx ,IPC_learn,c= 'r', label ="Learned IPC")
plt.xticks(np.arange(len(Y_test))[::100], header[2:][::100], rotation = 45)
plt.grid()
plt.legend()
plt.show()
