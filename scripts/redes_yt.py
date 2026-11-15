import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,networkx as nx,sys
from networkx.algorithms.community import louvain_communities,modularity
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
P=PQ+'/'
def red_yt(s):
    y=pd.read_pickle(P+f'yt_{s}.pkl')
    r=y[(y.idComentarioRespuesta!='nan')].drop_duplicates('idComentarioRespuesta')
    G=nx.DiGraph()
    for a,b in zip(r.NombreAutorComentarioRespuesta,r.NombreAutorComentarioPrincipal):
        if a in ('nan',None) or b in ('nan',None) or a==b: continue
        w=G.get_edge_data(a,b,{'weight':0})['weight']; G.add_edge(a,b,weight=w+1)
    return G,y
if __name__=='__main__':
    f=[]
    for s in SER:
        G,y=red_yt(s); U=G.to_undirected()
        com=louvain_communities(U,weight='weight',seed=1); Q=modularity(U,com,weight='weight')
        gc=max(nx.weakly_connected_components(G),key=len)
        kin=dict(G.in_degree()); top=sorted(kin,key=kin.get,reverse=True)[:3]
        f.append(dict(Serie=NOM[s],nodos=G.number_of_nodes(),aristas=G.number_of_edges(),comp_gigante=round(len(gc)/G.number_of_nodes(),2),
            reciprocidad=round(nx.reciprocity(G),3),agrupamiento=round(nx.average_clustering(U),3),modularidad=round(Q,2),
            kin_max=max(kin.values()),mas_respondidos='; '.join(f'{t} ({kin[t]})' for t in top)))
        print(f[-1]); nx.write_gexf(G,f'tab/red_respuestas_yt_{s}.gexf')
    pd.DataFrame(f).to_csv('tab/metricas_redes_yt.csv',index=False)
