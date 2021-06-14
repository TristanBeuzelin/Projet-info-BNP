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
    urls.append("https://rnm.franceagrimer.fr"+produit.find('a',href = True)['href']+"&12MOIS")
print("Done")


#urls = urls[:2]
N = len(urls)

produits = []

def getHeader(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')
    table = soup.find('table',attrs = {'class':'tabcot'})
    head = table.find('thead')
    return ['Origine']+[i.getText() for i in head.find('tr').find_all('th')[:-1]]


n_thread = 10
def getPrice(tid):
    i_start = int(i*N/n_thread)
    i_end = min(N,int((i+1)*N/n_thread))
    for k in range(i_start,i_end):
        url = urls[k]
        print("Thread n°"+str(tid)+" processing url n°"+str(k+1)+"/"+str(N))
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('table',attrs={'id' : 'tabcotmar'})
        origine = ""
        for line in table.find('tbody').find_all('tr'):
            strong = line.find('strong')
            if strong != None:
                origine = strong.find('a').getText()
            else:
                produit = line.find('td',attrs={'class' : 'tdcotl'})
                prix_moy = line.find_all('td',attrs={'class' : 'tdcotr m12'})
               
                produits.append([origine,produit.getText()]+[i.getText() for i in prix_moy])




class myThread (threading.Thread):
    def __init__(self, threadID,name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        getPrice(self.threadID)

threads = [myThread(i,"T"+str(i),i) for i in range(n_thread)]
for i in range(n_thread):
    threads[i].start()

for thread in threads:
    thread.join()

tableau = np.array(produits)

print("Creating csv file")
pd.DataFrame(tableau).to_csv("prix.csv",header = getHeader(urls[0]),sep=";")
print("Done")
