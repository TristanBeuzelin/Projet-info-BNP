import pandas as pd 
import numpy as np 
from scipy.interpolate import interp1d

data = pd.read_csv("./prix.csv",sep=';', index_col = 0, engine = 'python')

data_p = data.to_numpy()

data_t = data_p[:,2:]

n_rows,n_cols = data_t.shape

data_new = np.zeros_like(data_t)



for i in range(n_rows):
    if np.count_nonzero(data_t[i] == ' \xa0') == n_cols-1:
        k = [j for j in range(n_cols) if data_t[i,j] != ' \xa0'][0]
        for j in range(n_cols):
            data_new[i,j] = eval(data_t[i,k])

    else:
        
        j_inx = [j for j in range(n_cols) if data_t[i,j] != ' \xa0']

        y = [data_t[i,j] for j in j_inx]

        inter = interp1d(j_inx, y, fill_value = 'extrapolate' , kind = 'linear')
        values = [round(float(inter(j)),2) for j in range(n_cols)]
        mini = min([v for v in values if v > 0])

        val = np.array([max(mini,v) for v in values])
       
            
        data_new[i] = val

data_p[:,2:] = data_new

pd.DataFrame(data_p).to_csv("price_filled.csv",sep=";",header = ["Origine","Produit","Prix 1","Prix 2","Prix 3","Prix 4","Prix 5","Prix 6","Prix 7","Prix 8","Prix 9","Prix 10","Prix 11","Prix 12"])

