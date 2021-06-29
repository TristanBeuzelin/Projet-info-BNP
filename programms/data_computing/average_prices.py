import pandas as pd 
import numpy as np 
import os 

file = "./price_computed/price_filled2.csv"

df = pd.read_csv(file, sep = ";")
data = df.to_numpy()

header = df.columns

average_price_dict = {}

for line in data:
    product = line[1].split(' ')[0]

    numbers = np.array([float(i) for i in line[2:]])
    if product not in average_price_dict.keys():
        average_price_dict[product] = [1,numbers]
    else:
        average_price_dict[product] = [average_price_dict[product][0] + 1, average_price_dict[product][1] +numbers]
    
for k in average_price_dict.keys():
    average_price_dict[k] = [average_price_dict[k][0],np.around(average_price_dict[k][1]/average_price_dict[k][0],2)]

average_price = []

for k in average_price_dict.keys():
    average_price.append([k] + list(average_price_dict[k][1]))

pd.DataFrame(average_price).to_csv("./price_computed/average_prices.csv",sep=";",header = header[1:])

