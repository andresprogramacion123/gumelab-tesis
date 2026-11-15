import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,matplotlib.pyplot as plt,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
P=PQ+'/'
PAL=['#2a78d6','#eb6834','#1baf7a','#eda100','#e87ba4']
def ajuste(x):
    x=np.asarray(x,float); x=x[x>=1]; best=None
    cand=np.unique(np.quantile(x,np.linspace(0,0.95,60)).round())
    for xm in cand:
        t=x[x>=xm]
        if len(t)<50: continue
        a=1+len(t)/np.sum(np.log(t/(xm-0.5)))
        s=np.sort(t); emp=np.arange(1,len(s)+1)/len(s); teo=1-(s/xm)**(1-a)
        D=np.max(np.abs(emp-teo))
        if best is None or D<best[2]: best=(xm,a,D,len(t))
    return best
def datos(s):
    y=pd.read_pickle(P+f'yt_{s}.pkl'); t=pd.read_pickle(P+f'tw_{s}.pkl')
    v=y.drop_duplicates('idVideo'); c=y[y.idComentarioPrincipal!='nan'].drop_duplicates('idComentarioPrincipal')
    num=lambda z: pd.to_numeric(z,errors='coerce').dropna()
    return {'Vistas por video (YouTube)':num(v.VistasVideo),'Likes por comentario (YouTube)':num(c.LikesComentarioPrincipal),
            'Retuits por tuit (X)':num(t.retweet_count),'Tuits por cuenta (X)':t.author_id.value_counts()}
fig,ax=plt.subplots(2,2,figsize=(7.2,5.6)); ax=ax.ravel(); filas=[]
for i,s in enumerate(SER):
    D=datos(s)
    for k,(nom,x) in enumerate(D.items()):
        x=np.asarray(x,float); x=x[x>=1]
        if len(x)<20: continue
        xs=np.sort(x); ccdf=1-np.arange(len(xs))/len(xs)
        ax[k].loglog(xs,ccdf,color=PAL[i],lw=1.4,label=NOM[s])
        b=ajuste(x)
        filas.append(dict(Variable=nom,Serie=NOM[s],n=len(x),media=round(x.mean(),1),mediana=np.median(x),maximo=int(x.max()),
             xmin=b[0] if b else None,alpha=round(b[1],2) if b else None,KS=round(b[2],3) if b else None,n_cola=b[3] if b else None))
for k,nom in enumerate(D):
    ax[k].set_title(nom,fontsize=9,loc='left',fontweight='bold'); ax[k].set_ylabel('P(X ≥ x)'); ax[k].set_xlabel('x')
h,l=ax[0].get_legend_handles_labels(); fig.legend(h,l,loc='upper center',ncol=5,fontsize=7.5,bbox_to_anchor=(0.5,1.02))
plt.tight_layout(rect=(0,0,1,0.96)); fig.savefig('fig/colas_ccdf.png')
t=pd.DataFrame(filas); t.to_csv('tab/colas.csv',index=False); print(t.to_string())
# Gini y concentración en X
g=[]
for s in SER:
    c=np.sort(pd.read_pickle(P+f'tw_{s}.pkl').author_id.value_counts().values)[::-1]
    n=len(c); cs=np.cumsum(c)/c.sum(); top1=cs[max(int(n*0.01)-1,0)]; top10=cs[int(n*0.1)-1]
    a=np.sort(c); G=(2*np.sum(np.arange(1,n+1)*a)/(n*a.sum()))-(n+1)/n
    g.append(dict(Serie=NOM[s],cuentas=n,tuits=int(c.sum()),top1pct=round(top1,3),top10pct=round(top10,3),Gini=round(G,3),una_vez=round((c==1).mean(),3)))
print(pd.DataFrame(g).to_string()); pd.DataFrame(g).to_csv('tab/concentracion_x.csv',index=False)
