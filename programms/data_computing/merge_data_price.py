import os
import numpy as np 
import pandas as pd 
from glob import glob
import collections

paths = glob("./raw_adata_price/*.csv")

data = {}
dates = set()

for file in paths:
    df = pd.read_csv(file, sep=';', engine = 'c',header = 1,usecols= [0,2,5])[:-1]
    df = df.to_numpy()
    n = len(df)
    for i in range(n):
        date = df[i,0]
        libele = df[i,1]
        prix = df[i,2]
        dates.add(date)
        if libele in data.keys():
            data[libele] = data[libele] + [(date,prix)]
        else:
            data[libele] = [(date,prix)]

data = collections.OrderedDict(sorted(data.items()))
dates = list(sorted(dates))

prices = []



for i,(k,v) in enumerate(data.items()):
    l = [' \xa0']*len(dates)
    for x in v:
        j = dates.index(x[0])
        l[j] = x[1].replace(',','.')
    prices.append([k]+l)

pd.DataFrame(prices).to_csv("./price_computed/prices.csv",sep=";",header = ["Produit"] + dates) 