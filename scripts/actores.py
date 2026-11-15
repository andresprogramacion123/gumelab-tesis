import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,sys,networkx as nx
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *; from redes_x import cargar
P=PQ+'/'
PAISES=[('Colombia','colombia|bogot|medell|\\bcali\\b|barranq|cartag|bucaram|pereira|manizal|antioquia'),
 ('Chile','chile|santiago|valpara|concepci|temuco|antofag|viña'),('Argentina','argentin|buenos aires|córdoba|rosario|mendoza|escobar|pilar|caba'),
 ('México','méxico|mexico|cdmx|guadalaj|monterrey'),('España','españa|espana|madrid|barcelona|valencia|sevilla|spain'),
 ('Estados Unidos','usa|miami|new york|estados unidos|united states|california|texas|florida'),
 ('Venezuela','venezuela|caracas'),('Perú','perú|peru|lima'),('Ecuador','ecuador|quito|guayaquil'),('Brasil','brasil|brazil|são paulo|rio de janeiro'),('Alemania','deutschland|germany|alemania|berlin')]
def pais(loc):
    loc=pd.Series(loc).astype(str); out=pd.Series('No identificable',index=loc.index)
    for p,r in reversed(PAISES): out[loc.str.contains(r,case=False,regex=True)]=p
    return out
filas=[];paises=[]
for s in SER:
    t=cargar(s).reset_index(drop=True); u=t.drop_duplicates('u').copy(); u['pais']=pais(u.author_location).values
    idn=u[u.pais!='No identificable']; vc=idn.pais.value_counts(normalize=True)
    H=-(vc*np.log(vc)).sum()  # entropía (diversidad de países)
    for p,v in vc.items(): paises.append(dict(Serie=NOM[s],pais=p,frac=v,cuentas=int((idn.pais==p).sum())))
    y=pd.read_pickle(P+f'yt_{s}.pkl').drop_duplicates('idVideo')
    vistas=pd.to_numeric(y.VistasVideo,errors='coerce').sum()
    fol=pd.to_numeric(u.followers_count,errors='coerce')
    filas.append(dict(Serie=NOM[s],cuentas=len(u),frac_identificable=round(len(idn)/len(u),2),paises=idn.pais.nunique(),
        pais_1=f'{vc.index[0]} ({vc.iloc[0]*100:.0f} %)',pais_2=f'{vc.index[1]} ({vc.iloc[1]*100:.0f} %)' if len(vc)>1 else '',
        frac_fuera_pais_origen=None,entropia=round(H,2),
        vistas_yt_M=round(vistas/1e6,1),seguidores_M=round(fol.sum()/1e6,1),seg_mediana=int(fol.median()),
        retuits=int(pd.to_numeric(t[t.rt.isna()].retweet_count,errors='coerce').sum()),likes=int(pd.to_numeric(t[t.rt.isna()].like_count,errors='coerce').sum())))
d=pd.DataFrame(filas); print(d.to_string()); d.to_csv('tab/alcance_transnacional.csv',index=False)
pd.DataFrame(paises).to_csv('tab/paises_x.csv',index=False)
