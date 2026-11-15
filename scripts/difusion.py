import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *; from redes_x import cargar
f=[];tops=[]
for s in SER:
    t=cargar(s); o=t[t.rt.isna()].copy(); o['rtc']=pd.to_numeric(o.retweet_count,errors='coerce').fillna(0)
    a=o.groupby('u').rtc.sum().sort_values(ascending=False)   # retuits globales recibidos por cuenta (publicaciones originales)
    n=len(a); top1=a.head(max(1,int(n*0.01))).sum()/a.sum(); top10c=a.head(10).sum()/a.sum()
    amp=t[t.rt.notna()].u.value_counts()   # amplificadores dentro del corpus
    fol=pd.to_numeric(t.drop_duplicates('u').set_index('u').followers_count,errors='coerce')
    f.append(dict(Serie=NOM[s],originales=len(o),retuits_recibidos=int(a.sum()),cuentas_con_retuits=int((a>0).sum()),
        frac_top1pct=round(top1,2),frac_top10=round(top10c,2),rt_en_corpus=int(t.rt.notna().sum()),amplificadores=len(amp),
        frac_amp_top1pct=round(amp.head(max(1,int(len(amp)*0.01))).sum()/amp.sum(),2)))
    for u,v in a.head(10).items(): tops.append(dict(Serie=NOM[s],cuenta='@'+u,retuits=int(v),seguidores=int(fol.get(u,np.nan)) if pd.notna(fol.get(u,np.nan)) else None))
d=pd.DataFrame(f); print(d.to_string()); d.to_csv('tab/difusion.csv',index=False)
tp=pd.DataFrame(tops); print(tp.groupby('Serie').head(6).to_string()); tp.to_csv('tab/difusores_top.csv',index=False)
