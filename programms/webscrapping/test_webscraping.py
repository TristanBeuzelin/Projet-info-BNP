from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd 
import numpy as np 
import os

urlpage = "https://rnm.franceagrimer.fr/prix?FRUITS-ET-LEGUMES"

page = urllib.request.urlopen(urlpage)

soup = BeautifulSoup(page, 'html.parser')


table = soup.find_all('div', attrs={'class': 'listunproduit'})

urls = []

print("Getting urls...")
for produit in table:
    urls.append("https://rnm.franceagrimer.fr"+produit.find('a',href = True)['href'])
print("Done")
N = len(urls)

produits = []
for i,url in enumerate(urls):
    print("Processing url n°"+str(i+1)+"/"+str(N))
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table',attrs={'id' : 'tabcotmar'})
    
    for line in table.find('tbody').find_all('tr'):
        small = line.find('small')
        if small == None:
            produit = line.find('td',attrs={'class' : 'tdcotl'})
            prix_moy = line.find('td',attrs={'class' : 'tdcotr'})
            prix_min_max = line.find_all('td',attrs={'class' : 'tdcotr minmax'})
            varia = line.find('td',attrs={'class' : 'tdcotc'})
            produits.append([produit.getText(),prix_moy.getText(),varia.getText(),prix_min_max[0].getText(),prix_min_max[1].getText()])

tableau = np.array(produits)

print("Creating csv file")
pd.DataFrame(tableau).to_csv("prix.csv")
print("Done")
