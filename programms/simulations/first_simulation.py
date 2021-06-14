import pandas as pd 
import numpy as np 
import os 
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt 


df_price = pd.read_csv("./price_computed/average_prices.csv",sep = ";") 
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




prices_learn = df_price[[header[j] for j in j_idx]].to_numpy() #Prices used to teach the model
price_test = df_price[[header[j+2] for j in range(len(header[2:])) if j+2 not in j_idx ]].to_numpy() #Prices to test the model


coeffs = np.matmul(np.linalg.inv(prices_learn.T),IPC_learn) #Coefficient of the matrix of the linear system



IPC_dict = {} #Dictionnary containing each IPCs (values) for each month (keys)

for [date,ipc] in df_ipc:
    IPC_dict[date] = ipc 


Y_real = [] #IPCs of the month for each day in the month
Y_test = np.matmul(prices.T,coeffs) #The same but the ones we calculated
Y_learn = np.matmul(prices_learn.T,coeffs) #The verification of the calcul

for j,price in enumerate(prices.T): #Filling of Y_real
    date = header[j+2][:-3]
    if date in IPC_dict.keys():
        Y_real.append(IPC_dict[date])
    

Y_test_month_average_dict = {}
for j,index in enumerate(Y_test): #Filling of Y_real
    date = header[j+2][:-3]
    if date in Y_test_month_average_dict.keys():
        Y_test_month_average_dict[date].append(float(index))
    else:
        Y_test_month_average_dict[date] = [float(index)]


for key in Y_test_month_average_dict.keys():
    Y_test_month_average_dict[key] = sum(Y_test_month_average_dict[key])/len(Y_test_month_average_dict[key])

Y_test_month_average = []
for j,price in enumerate(prices.T): #Filling of Y_real
    date = header[j+2][:-3]
    if date in IPC_dict.keys():
        Y_test_month_average.append(Y_test_month_average_dict[date])


#Plotting the values 
plt.subplot(211)
plt.plot(np.arange(len(Y_real)),Y_real, label = "Real IPC")
plt.plot(np.arange(len(Y_test)),Y_test, label ="Prediction IPC")
plt.scatter(j_idx ,IPC_learn,c= 'r', label ="Learned IPC")
plt.xticks(np.arange(len(Y_test))[::100], header[2:][::100], rotation = 45)
plt.grid()
plt.legend()

plt.subplot(212)
plt.plot(np.arange(len(Y_real)),Y_real, label = "Real IPC")
plt.plot(np.arange(len(Y_test_month_average)),Y_test_month_average, label ="Prediction IPC monthly averaged")
plt.xticks(np.arange(len(Y_test))[::100], header[2:][::100], rotation = 45)
plt.grid()
plt.legend()

plt.show()
