import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,networkx as nx,sys,matplotlib.pyplot as plt
from networkx.algorithms.community import louvain_communities
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *; from redes_x import cargar,interaccion,bipartita
s=sys.argv[1] if len(sys.argv)>1 else 'EPM'
t=cargar(s); G=interaccion(t)
fig,ax=plt.subplots(1,2,figsize=(7.4,3.9))
# (a) red de interacción: núcleo por PageRank
pr=nx.pagerank(G,weight='weight'); top=sorted(pr,key=pr.get,reverse=True)[:300]
H=G.subgraph(top).copy(); H=H.subgraph(max(nx.weakly_connected_components(H),key=len)).copy()
U=H.to_undirected(); com=sorted(louvain_communities(U,weight='weight',seed=1),key=len,reverse=True)
PAL=['#2a78d6','#eb6834','#1baf7a','#6250d6']; col={}
for i,c in enumerate(com):
    for n in c: col[n]=PAL[i] if i<4 else '#c3c2b7'
pos=nx.kamada_kawai_layout(U)
sz=np.array([pr[n] for n in H]); sz=6+260*np.sqrt(sz/sz.max())
nx.draw_networkx_edges(H,pos,ax=ax[0],width=0.3,alpha=0.35,edge_color='#8a8984',arrows=False)
nx.draw_networkx_nodes(H,pos,ax=ax[0],node_size=sz,node_color=[col[n] for n in H],linewidths=0.4,edgecolors='white')
lista=[]
for i,n in enumerate(sorted(H,key=pr.get,reverse=True)[:8],1):
    ax[0].annotate(str(i),pos[n],fontsize=6.5,fontweight='bold',ha='center',va='center',color='white')
    lista.append(f'{i} @{n}')
ax[0].text(0.0,0.0,'\n'.join(lista),transform=ax[0].transAxes,fontsize=6.2,va='bottom',color='#0b0b0b')
ax[0].set_title('(a) Menciones y retuits entre cuentas\n(componente principal de las 300 cuentas\ncon mayor PageRank)',fontsize=8.5,loc='left'); ax[0].axis('off')
# (b) bipartita hashtag–cuenta (traducción de Julian.nb)
B,nc=bipartita(t)
tags=[h for h in nc.sort_values(ascending=False).index if h in B][:25]
cu=pd.Series({u:sum(1 for h in B[u] if h in tags) for u in set(v for h in tags for v in B[h])})
cu=cu[cu>=2].sort_values(ascending=False).head(110).index
prim=[u for h in tags for u in B[h] if B[h][u]['primero']]
S=B.subgraph(list(tags)+list(cu)+prim).copy(); S.remove_nodes_from([n for n in list(S) if S.degree(n)==0])
pos2=nx.spring_layout(S,seed=7,k=0.5,iterations=300)
ed=list(S.edges(data=True)); norm=[(u,v) for u,v,d in ed if not d['primero']]; red=[(u,v) for u,v,d in ed if d['primero']]
nx.draw_networkx_edges(S,pos2,edgelist=norm,ax=ax[1],width=0.3,alpha=0.35,edge_color='#8a8984')
nx.draw_networkx_edges(S,pos2,edgelist=red,ax=ax[1],width=1.4,edge_color='#e34948')
hs=[n for n in S if S.nodes[n]['tipo']=='hashtag']; us=[n for n in S if S.nodes[n]['tipo']=='cuenta']
nx.draw_networkx_nodes(S,pos2,nodelist=us,ax=ax[1],node_shape='^',node_size=14,node_color='#2a78d6',linewidths=0)
nx.draw_networkx_nodes(S,pos2,nodelist=hs,ax=ax[1],node_size=[20+180*nc[h]/nc[hs].max() for h in hs],node_color='#eda100',edgecolors='white',linewidths=0.5)
for h in hs[:12]: ax[1].annotate(h,pos2[h],fontsize=6,ha='center',va='bottom',xytext=(0,4),textcoords='offset points')
ax[1].set_title('(b) Red bipartita hashtag–cuenta\n(25 hashtags más compartidos)',fontsize=8.5,loc='left'); ax[1].axis('off')
from matplotlib.lines import Line2D
lg=[Line2D([],[],marker='o',ls='',color='#eda100',label='hashtag'),Line2D([],[],marker='^',ls='',color='#2a78d6',label='cuenta'),Line2D([],[],color='#e34948',lw=1.4,label='primer emisor')]
ax[1].legend(handles=lg,loc='lower left',fontsize=6.5)
plt.tight_layout(); fig.savefig(f'fig/redes_x_{s}.png'); print('ok',H.number_of_nodes(),S.number_of_nodes(),len(red))
