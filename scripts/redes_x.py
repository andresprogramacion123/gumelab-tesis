import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,networkx as nx,re,sys,json
from networkx.algorithms.community import louvain_communities,modularity
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
P=PQ+'/'
def cargar(s):
    t=pd.read_pickle(P+f'tw_{s}.pkl'); t=t[~t.text.str.startswith(('QUERY','NEXT PAG'))]
    t=t[t.account_username.notna()&(t.account_username!='nan')].copy()
    t['u']=t.account_username.str.lower(); t['fecha']=pd.to_datetime(t.created_at,errors='coerce',utc=True)
    t['tags']=t.text.str.lower().str.findall(r'#\w+'); t['ments']=t.text.str.lower().str.findall(r'@(\w{2,15})')
    t['rt']=t.text.str.extract(r'^RT @(\w+)',expand=False).str.lower(); return t
def interaccion(t):
    G=nx.DiGraph()
    for u,ms,rt in zip(t.u,t.ments,t.rt):
        for m in sorted(set(ms)):
            if m!=u:
                w=G.get_edge_data(u,m,{'weight':0})['weight']; G.add_edge(u,m,weight=w+1)
    return G
def bipartita(t,min_cuentas=2):
    e=t[['u','tags','fecha']].explode('tags').dropna(subset=['tags']).drop_duplicates(['u','tags'])
    nc=e.groupby('tags').u.nunique(); keep=nc[nc>=min_cuentas].index; e=e[e.tags.isin(keep)]
    prim=e.sort_values('fecha').drop_duplicates('tags')[['tags','u']]  # primer emisor
    B=nx.Graph()
    B.add_nodes_from(e.u.unique(),tipo='cuenta'); B.add_nodes_from(e.tags.unique(),tipo='hashtag')
    pr=set(zip(prim.u,prim.tags))
    for u,h in zip(e.u,e.tags): B.add_edge(u,h,primero=(u,h) in pr)
    return B,nc
if __name__=='__main__':
    filas=[]
    for s in SER:
        t=cargar(s); G=interaccion(t); U=G.to_undirected()
        com=louvain_communities(U,weight='weight',seed=1); Q=modularity(U,com,weight='weight')
        kin=np.array([d for _,d in G.in_degree()]); 
        B,nc=bipartita(t); nh=sum(1 for _,d in B.nodes(data=True) if d['tipo']=='hashtag')
        pr=nx.pagerank(G,weight='weight'); top=sorted(pr,key=pr.get,reverse=True)[:8]
        gc=max(nx.weakly_connected_components(G),key=len)
        filas.append(dict(Serie=NOM[s],tuits=len(t),nodos=G.number_of_nodes(),aristas=G.number_of_edges(),densidad=f'{nx.density(G):.1e}',
          comp_gigante=round(len(gc)/G.number_of_nodes(),2),agrupamiento=round(nx.average_clustering(U),3),reciprocidad=round(nx.reciprocity(G),3),
          comunidades=len(com),modularidad=round(Q,2),kin_max=int(kin.max()),hashtags_compartidos=nh,top_pagerank=', '.join('@'+x for x in top)))
        nx.write_gexf(G,f'tab/red_interaccion_{s}.gexf'); nx.write_gexf(B,f'tab/red_bipartita_{s}.gexf')
        print(filas[-1])
    pd.DataFrame(filas).to_csv('tab/metricas_redes_x.csv',index=False)
