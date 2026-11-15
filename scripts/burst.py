import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *; from temporal import yt_fechas,tw_fechas
f=[]
for s in SER:
    for nom,fn in [('YouTube',yt_fechas),('X',tw_fechas)]:
        x=fn(s).sort_values(); t=((x-x.iloc[0]).dt.total_seconds()/3600).values  # horas
        tau=np.diff(t); tau=tau[tau>0]
        mu,sd=tau.mean(),tau.std(); B=(sd-mu)/(sd+mu)
        f.append(dict(Serie=NOM[s],Fuente=nom,n=len(t),tau_media_h=round(mu,2),tau_sd_h=round(sd,1),B=round(B,2)))
d=pd.DataFrame(f); print(d.to_string()); d.to_csv('tab/burstiness.csv',index=False)
