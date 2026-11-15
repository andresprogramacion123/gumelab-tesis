import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,sys,networkx as nx,re
from networkx.algorithms.community import louvain_communities
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *; from redes_x import cargar,interaccion
s_=sys.argv[1] if len(sys.argv)>1 else 'TresCaines'
CONTRA=r'#noen3caines|#noentrescaines|#notrescaines|apolog[ií]a|retir(en|ar) la pauta|anunciantes|v[ií]ctimas del paramilitar'
sent=pd.read_pickle(PRIV+'/sent.pkl'); sent=sent[sent.fuente=='X'][['id','p_neg','p_pos','pred']]
t=cargar(s_); t['id']=t['id'].astype(str); t=t.merge(sent,on='id',how='left')
t['contra']=t.text.str.lower().str.contains(CONTRA,regex=True)
G=interaccion(t); U=G.to_undirected()
com=sorted(louvain_communities(U,weight='weight',seed=1),key=len,reverse=True)
pr=nx.pagerank(G,weight='weight'); cu={n:i for i,c in enumerate(com) for n in c}
t['com']=t.u.map(cu)
filas=[]
for i,c in enumerate(com[:12]):
    g=t[t.com==i]; tags=g.tags.explode().value_counts().head(5).index.tolist()
    top=sorted(c,key=pr.get,reverse=True)[:4]
    filas.append(dict(com=i,cuentas=len(c),tuits=len(g),frac_contra=round(g.contra.mean(),3),
        neg=round((g.pred=='NEG').mean(),2),pos=round((g.pred=='POS').mean(),2),centrales=', '.join('@'+x for x in top),hashtags=' '.join(tags)))
d=pd.DataFrame(filas); pd.set_option('display.width',260,'display.max_colwidth',90); print(d.to_string())
print('tuits contra total',t.contra.sum(),'cuentas contra',t[t.contra].u.nunique())
cc=t[t.contra].com.value_counts(normalize=True).head(5); print('distribución de tuits contra por comunidad',cc.round(2).to_dict())
d.to_csv(f'tab/comunidades_{s_}.csv',index=False)
# ---- mapa de comunidades (grafo de comunidades) ----
import matplotlib.pyplot as plt, matplotlib.colors as mcolors
K=12; idx={n:i for i,c in enumerate(com[:K]) for n in c}
Q=nx.Graph()
for i in range(K): Q.add_node(i)
for a,b,w in G.edges(data='weight'):
    i,j=idx.get(a),idx.get(b)
    if i is None or j is None or i==j: continue
    Q.add_edge(i,j,weight=Q.get_edge_data(i,j,{'weight':0})['weight']+w)
d=d.set_index('com'); bal=(d.pos-d.neg)
cmap=mcolors.LinearSegmentedColormap.from_list('div',['#e34948','#e8e6e1','#2a78d6']); norm=mcolors.TwoSlopeNorm(0,-0.6,0.6)
NS={i:250+2000*d.cuentas[i]/d.cuentas.max() for i in Q}
pos=nx.spring_layout(Q,weight=None,seed=4,k=1.6)
fig,ax=plt.subplots(figsize=(7.2,5.6))
ws=np.array([w for *_,w in Q.edges(data='weight')]); 
nx.draw_networkx_edges(Q,pos,ax=ax,width=0.4+5*ws/ws.max(),edge_color='#c3c2b7',alpha=0.8)
nx.draw_networkx_nodes(Q,pos,ax=ax,node_size=[NS[i] for i in Q],node_color=[cmap(norm(bal[i])) for i in Q],edgecolors='#52514e',linewidths=0.6)
for i in Q:
    lab='\n'.join(d.centrales[i].split(', ')[:2]); ax.annotate(lab,pos[i],xytext=(0,-np.sqrt(NS[i])/2-3),textcoords='offset points',ha='center',va='top',fontsize=6.5)
    if d.frac_contra[i]>=0.04: ax.annotate(f'{d.frac_contra[i]*100:.0f} %',pos[i],ha='center',va='center',fontsize=7,fontweight='bold')
sm=plt.cm.ScalarMappable(cmap=cmap,norm=norm); cb=plt.colorbar(sm,ax=ax,fraction=0.035,pad=0.01)
cb.set_label('Balance de sentimiento (positivos − negativos)'); cb.ax.yaxis.set_major_formatter(lambda v,_: f'{v:.1f}'.replace('.',','))
ax.axis('off'); ax.margins(0.12); plt.tight_layout(); fig.savefig(f'fig/comunidades_{s_}.png'); print('figura ok')
