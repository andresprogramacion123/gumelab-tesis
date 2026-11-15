import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
# Serie temporal con textos en español y comparación con el total (para marcar artefactos)
import pandas as pd,numpy as np,matplotlib.pyplot as plt,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
s=pd.read_pickle(PRIV+'/sent.pkl').merge(pd.read_pickle(PRIV+'/idioma.pkl'),on=['fuente','id'])
s=s[s.mes>=pd.Period('2008-01','M')]
fig,ax=plt.subplots(5,1,figsize=(7.2,9),sharex=True); filas=[]
for i,se in enumerate(SER):
    a=ax[i]
    for f,col in [('YouTube',C['yt']),('X',C['tw'])]:
        g=s[(s.fuente==f)&(s.serie==se)]
        tot=g.mes.value_counts().sort_index(); es=g[g.es==True].mes.value_counts()
        idx=pd.period_range(tot.index.min(),tot.index.max(),freq='M'); tot=tot.reindex(idx,fill_value=0); es=es.reindex(idx,fill_value=0)
        x=idx.to_timestamp()
        a.plot(x,es.values,color=col,label=f'{f} (español)')
        if f=='YouTube': a.plot(x,tot.values,color=col,lw=0.8,ls=':',label='YouTube (todos los idiomas)')
        mu,sd=es.mean(),es.std(); z=(es-mu)/sd
        for per,zz in z[z>3].sort_values(ascending=False).head(3).items():
            gm=g[(g.mes==per)]; filas.append(dict(Serie=NOM[se],Fuente=f,Mes=str(per),docs=int(tot[per]),docs_es=int(es[per]),z_es=round(zz,1),frac_es=round(gm.es.mean(),2)))
    a.set_yscale('symlog',linthresh=10); a.set_ylabel('Docs/mes'); a.set_title(NOM[se],loc='left',fontsize=9,fontweight='bold')
    for d,t in EVENTOS[se]:
        a.axvline(pd.Timestamp(d),color=C['muted'],lw=0.8,ls='--'); a.text(pd.Timestamp(d),a.get_ylim()[1]*0.6,' '+t,fontsize=7,color=C['muted'])
fig.legend(*ax[1].get_legend_handles_labels(),loc='upper center',ncol=3,bbox_to_anchor=(0.5,1.01),fontsize=8)
ax[-1].set_xlim(pd.Timestamp('2008-01-01'),pd.Timestamp('2022-10-01'))
fig.align_ylabels(); plt.tight_layout(rect=(0,0,1,0.985)); fig.savefig('fig/temporal_series.png')
t=pd.DataFrame(filas); t.to_csv('tab/picos_es.csv',index=False); print(t.to_string())
