from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd 
import numpy as np 
import os
import threading

urlpage = "https://rnm.franceagrimer.fr/prix?FRUITS-ET-LEGUMES"

page = urllib.request.urlopen(urlpage)

soup = BeautifulSoup(page, 'html.parser')


table = soup.find_all('div', attrs={'class': 'listunproduit'})

urls = []

print("Getting urls...")
for produit in table:
    urls.append("https://rnm.franceagrimer.fr"+produit.find('a',href = True)['href']+'&12MOIS')
print("Done")
N = len(urls)

produits = []

n_thread = 4
def getPrice(tid):
    i_start = int(i*N/n_thread)
    i_end = min(N,int((i+1)*N/n_thread))
    for k in range(i_start,i_end):
        url = urls[k]
        print("Thread n°"+str(tid)+" processing url n°"+str(k+1)+"/"+str(N))
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('table',attrs={'id' : 'tabcotmar'})
        
        for line in table.find('tbody').find_all('tr'):
            location_title = line.find('td', attrs={'class' : 'tdcotcolspan'})
            if location_title == None:
                produit = line.find('td',attrs={'class' : 'tdcotl'})
                prix = line.find_all('td',attrs={'class' : 'tdcotr m12'})
                produits.append([produit.getText(),prix[0].getText(),
                                 prix[1].getText(),prix[2].getText(),
                                 prix[3].getText(),prix[4].getText(),
                                 prix[5].getText(),prix[6].getText(),
                                 prix[7].getText(),prix[8].getText(),
                                 prix[9].getText(),prix[10].getText(),
                                 prix[11].getText()])




class myThread (threading.Thread):
    def __init__(self, threadID,name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        getPrice(self.threadID)

threads = [myThread(i,"T"+str(i),i) for i in range(n_thread)]
print(threads)
for i in range(n_thread):
    threads[i].start()

for thread in threads:
    thread.join()

tableau = np.array(produits)
print("Creating csv file")
pd.DataFrame(tableau).to_csv("prix3.csv",header = ["Produit","Prix 1","Prix 2","Prix 3","Prix 4","Prix 5","Prix 6","Prix 7","Prix 8","Prix 9","Prix 10","Prix 11","Prix 12"],sep=";")
print("Done")