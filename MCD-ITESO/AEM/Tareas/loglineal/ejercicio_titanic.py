
import pandas as pd
import numpy as np

# Importar datos
data = pd.read_excel('Titanic.xls')
tabla = pd.crosstab(index=data['survived'], columns=data['pclass'], margins=True)

# Aplicar logaritmos y medias de logaritmos
tab_log = np.log(tabla.iloc[0:-1, 0:-1])
tab_log.loc['media_columnas'] = tab_log.mean(axis=0)
tab_log['media_filas'] = tab_log.mean(axis=1)

# Calcular mu, mu1, mu2
mu = tab_log.iloc[-1, -1]
mu1 = tab_log.iloc[:, -1]-mu
mu2 = tab_log.iloc[-1, :]-mu

# Tratar de recuperar la tabla de logaritmos
tab_rec = np.ones(np.shape(tab_log))*mu

for k in np.arange(np.shape(tab_log)[0]):
    tab_rec[k,:] = tab_rec[k,:]+mu2

for k in np.arange(np.shape(tab_log)[1]):
    tab_rec[:,k] = tab_rec[:,k]+mu1
tab_rec = tab_rec[0:-1,0:-1]

# Calcular tabla auxiliar (mu12)
tab_mu12 = pd.DataFrame(np.transpose(np.transpose(tab_log-mu-mu2)-mu1))
tab_mu12.iloc[:,-1] = mu1
tab_mu12.iloc[-1,:] = mu2

# Tabla recuperada modificada (mu+mu1+mu2+mu12)
tab_rec_mod = tab_rec+tab_mu12.iloc[0:-1,0:-1]
