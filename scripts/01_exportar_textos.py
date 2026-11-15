import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
"""Reúne comentarios, respuestas y tuits en un solo archivo para los cuadernos de Colab (sentimiento y NER)."""
import pandas as pd
from estilo import SER
out=[]
for s in SER:
    y=pd.read_pickle(os.path.join(PQ,f'yt_{s}.pkl'))
    c=y[y.idComentarioPrincipal!='nan'].drop_duplicates('idComentarioPrincipal')
    out.append(pd.DataFrame({'id':c.idComentarioPrincipal,'fuente':'YouTube','serie':s,'tipo':'comentario','fecha':c.FechaPublicacionComentarioPrincipal,'likes':c.LikesComentarioPrincipal,'texto':c.TextoComentarioPrincipal}))
    r=y[y.idComentarioRespuesta!='nan'].drop_duplicates('idComentarioRespuesta')
    out.append(pd.DataFrame({'id':r.idComentarioRespuesta,'fuente':'YouTube','serie':s,'tipo':'respuesta','fecha':r.FechaPublicacionComentarioRespuesta,'likes':r.LikesComentarioRespuesta,'texto':r.TextoComentarioRespuesta}))
    t=pd.read_pickle(os.path.join(PQ,f'tw_{s}.pkl')); t=t[~t.text.str.startswith(('QUERY','NEXT PAG'))]
    out.append(pd.DataFrame({'id':t['id'].astype(str),'fuente':'X','serie':s,'tipo':'tuit','fecha':t.created_at,'likes':t.like_count,'texto':t.text}))
d=pd.concat(out,ignore_index=True); d=d[d.texto.notna()&(d.texto!='nan')&(d.texto.str.strip()!='')].drop_duplicates(['fuente','id'])
d.to_csv(os.path.join(PRIV,'textos_gumelab.csv.gz'),index=False,compression='gzip'); print(len(d),'textos')
