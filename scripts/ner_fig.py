import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,sys,networkx as nx,matplotlib.pyplot as plt,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
c=pd.read_pickle(PRIV+'/ner_canon.pkl')
idi=pd.read_pickle(PRIV+'/idioma.pkl'); sent=pd.read_pickle(PRIV+'/sent.pkl')[['fuente','id','pred','p_pos','p_neg']]
c=c.merge(sent,on=['fuente','id']).merge(idi,on=['fuente','id']); c=c[(c.es==True)&(c.pred!='SOLO_EMOJI')]
c['bal']=c.p_pos-c.p_neg
print(pd.crosstab(c.serie,c.cat))
COL={'Personaje histórico':'#e34948','Político contemporáneo':'#6250d6','Elenco y producción':'#2a78d6','Personaje de ficción':'#1baf7a'}
# --- (1) sentimiento por entidad (todas las series), n>=80
g=c.groupby(['canon','cat']).agg(n=('bal','size'),bal=('bal','mean'),se=('bal',lambda x: x.std()/np.sqrt(len(x)))).reset_index()
g=g[g.n>=80].sort_values('bal'); g.to_csv('tab/ner_sentimiento.csv',index=False); print(g.round(3).to_string())
fig,ax=plt.subplots(figsize=(6.4,0.24*len(g)+1))
y=np.arange(len(g)); ax.axvline(0,color='#c3c2b7',lw=0.8)
ax.errorbar(g.bal,y,xerr=1.96*g.se,fmt='none',ecolor='#8a8984',lw=0.8)
ax.scatter(g.bal,y,s=28,c=g.cat.map(COL),zorder=3)
ax.set_yticks(y,[f'{a} ({n})' for a,n in zip(g.canon,g.n)],fontsize=7.5); ax.grid(axis='y',visible=False)
ax.set_xlabel('Balance de sentimiento de los textos que la mencionan (P+ − P−)'); ax.xaxis.set_major_formatter(lambda v,_: f'{v:.1f}'.replace('.',','))
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([],[],marker='o',ls='',color=v,label=k) for k,v in COL.items()],fontsize=7,loc='lower right')
plt.tight_layout(); fig.savefig('fig/ner_sentimiento.png'); plt.close()
# --- (2) red de coocurrencia
def red(series,ax,titulo,minw=5,excl=(),top=16):
    d=c[c.serie.isin(series)&~c.canon.isin(excl)]
    keep=d.canon.value_counts().head(top).index; d=d[d.canon.isin(keep)]
    G=nx.Graph(); cnt=d.groupby('canon').size(); cats=d.drop_duplicates('canon').set_index('canon').cat
    for _,grp in d.groupby(['fuente','id']).canon:
        for a,b in itertools.combinations(sorted(set(grp)),2):
            G.add_edge(a,b,weight=G.get_edge_data(a,b,{'weight':0})['weight']+1)
    G.remove_edges_from([(a,b) for a,b,w in G.edges(data='weight') if w<minw]); G.remove_nodes_from([n for n in list(G) if G.degree(n)==0])
    orden=sorted(G,key=lambda n:(list(COL).index(cats[n]),-cnt[n]))
    ang=np.linspace(0,2*np.pi,len(orden),endpoint=False)+np.pi/2
    pos={n:(np.cos(a),np.sin(a)) for n,a in zip(orden,ang)}
    w=np.array([w for *_,w in G.edges(data='weight')])
    nx.draw_networkx_edges(G,pos,ax=ax,width=0.3+4*np.log1p(w)/np.log1p(w.max()),edge_color='#8a8984',alpha=0.55)
    nx.draw_networkx_nodes(G,pos,ax=ax,node_size=[20+22*np.log1p(cnt[n])**1.5 for n in G],node_color=[COL[cats[n]] for n in G],edgecolors='white',linewidths=0.6)
    for n in G:
        x,y=pos[n]; ax.annotate(n,(x,y),xytext=(14*x,10*y),textcoords='offset points',ha='left' if x>0.15 else ('right' if x<-0.15 else 'center'),va='center',fontsize=6.3)
    ax.set_title(titulo,loc='left',fontsize=8.5); ax.axis('off'); ax.margins(0.35)
    return G
fig,ax=plt.subplots(1,2,figsize=(7.6,4.2))
red(['EPM'],ax[0],'(a) Escobar, el patrón del mal',minw=5)
red(['TresCaines'],ax[1],'(b) Tres Caínes',minw=4)
fig.legend(handles=[Line2D([],[],marker='o',ls='',color=v,label=k) for k,v in COL.items() if k!='Personaje de ficción'],loc='lower center',ncol=3,fontsize=7)
plt.tight_layout(rect=(0,0.05,1,1)); fig.savefig('fig/ner_red.png'); print('ok')
