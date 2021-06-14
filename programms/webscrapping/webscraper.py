import requests as rq
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

r = rq.get('https://rnm.franceagrimer.fr/prix?FRAISE&12MOIS')
input_fill = {'sellibnom': '500'}
r = rq.get('https://rnm.franceagrimer.fr/prix?FRAISE&12MOIS', data=input_fill)
"""
soup = BeautifulSoup(r.text, 'html.parser')
"""
"""
with open('test2.html', 'w') as data:
    data.write(soup.prettify())
"""
soup = BeautifulSoup(r.text, 'html.parser')
box = soup.find_all('td', attrs={'class', 'tdcotr m12'})

prices_list = []
for element in box:
    try:
        price = float(str(element)[24:-5])
        prices_list.append(str(element)[24:-5])
    except:
        continue

with open('test.txt', 'w') as data:
    data.write(''.join(str(price)+'\n' for price in prices_list))

