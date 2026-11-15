import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,matplotlib.pyplot as plt,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
P=PQ+'/'
def yt_fechas(s):
    y=pd.read_pickle(P+f'yt_{s}.pkl')
    c=y[y.idComentarioPrincipal!='nan'].drop_duplicates('idComentarioPrincipal').FechaPublicacionComentarioPrincipal
    r=y[y.idComentarioRespuesta!='nan'].drop_duplicates('idComentarioRespuesta').FechaPublicacionComentarioRespuesta
    return pd.to_datetime(pd.concat([c,r]),errors='coerce',utc=True).dropna()
def tw_fechas(s):
    return pd.to_datetime(pd.read_pickle(P+f'tw_{s}.pkl').created_at,errors='coerce',utc=True).dropna()
def mensual(f): return f.dt.tz_localize(None).dt.to_period('M').value_counts().sort_index().asfreq('M',fill_value=0) if len(f) else pd.Series(dtype=int)
if __name__=="__main__":
    filas=[]
    fig,ax=plt.subplots(5,1,figsize=(7.2,9),sharex=True)
    for i,s in enumerate(SER):
        a=ax[i]
        for nom,fn,col in [('YouTube',yt_fechas,C['yt']),('X',tw_fechas,C['tw'])]:
            m=mensual(fn(s)); m=m[m.index>=pd.Period('2008-01','M')]
            full=m.reindex(pd.period_range(m.index.min(),m.index.max(),freq='M'),fill_value=0)
            x=full.index.to_timestamp(); a.plot(x,full.values,color=col,label=nom)
            mu,sd=full.mean(),full.std(); B=(sd-mu)/(sd+mu)
            z=(full-mu)/sd; pk=z[z>3].sort_values(ascending=False)
            for per,zz in pk.head(3).items():
                filas.append(dict(Serie=NOM[s],Fuente=nom,Mes=str(per),Docs=int(full[per]),z=round(zz,1)))
            filas.append(dict(Serie=NOM[s],Fuente=nom,Mes='—',Docs=int(full.sum()),z=np.nan,B=round(B,2),media=round(mu,1),max=int(full.max()),mes_max=str(full.idxmax())))
        a.set_yscale('symlog',linthresh=10); a.set_ylabel('Docs/mes'); a.set_title(NOM[s],loc='left',fontsize=9,fontweight='bold')
        for d,t in EVENTOS[s]:
            a.axvline(pd.Timestamp(d),color=C['muted'],lw=0.8,ls='--'); a.text(pd.Timestamp(d),a.get_ylim()[1]*0.6,' '+t,fontsize=7,color=C['muted'])
    fig.legend(*ax[0].get_legend_handles_labels(),loc='upper center',ncol=2,bbox_to_anchor=(0.5,1.01))
    ax[-1].set_xlim(pd.Timestamp('2008-01-01'),pd.Timestamp('2022-10-01'))
    fig.align_ylabels(); plt.tight_layout(rect=(0,0,1,0.985)); fig.savefig('fig/temporal_series.png')
    t=pd.DataFrame(filas); t.to_csv('tab/picos.csv',index=False); print(t.to_string())
