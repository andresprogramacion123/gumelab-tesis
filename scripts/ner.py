import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
e=pd.read_csv(PRIV+'/entidades_gumelab.csv.gz',dtype={'id':str})
e['x']=e.entidad.str.lower().str.strip()
# (nombre canónico, categoría, regex sobre la entidad)  —el orden importa
CAN=[('Juana Uribe','Elenco y producción','juana uribe'),
 ('Pablo Escobar','Personaje histórico',r'^(pablo( emilio)?( escobar)?( gaviria)?|escobar( gaviria)?|pablito|el patr[oó]n)$'),
 ('Luis Carlos Galán','Personaje histórico',r'gal[aá]n'),('Guillermo Cano','Personaje histórico',r'guillermo cano'),
 ('Rodrigo Lara Bonilla','Personaje histórico',r'lara bonilla'),('Popeye','Personaje histórico',r'popeye|john jairo vel'),
 ('Hermanos Ochoa','Personaje histórico',r'^ochoa|hermanos ochoa'),('Virginia Vallejo','Personaje histórico',r'virginia vallejo'),
 ('Rodríguez Gacha','Personaje histórico',r'rodr[ií]guez gacha|el mexicano'),('Hermanos Rodríguez Orejuela','Personaje histórico',r'orejuela'),
 ('Pacho Herrera','Personaje histórico',r'pacho herrera'),('El Chapo','Personaje histórico',r'chapo'),
 ('Carlos Castaño','Personaje histórico',r'carlos casta[ñn]o|^casta[ñn]o$'),('Fidel Castaño','Personaje histórico',r'fidel'),
 ('Vicente Castaño','Personaje histórico',r'vicente'),('Jaime Garzón','Personaje histórico',r'garz[oó]n'),
 ('Augusto Pinochet','Personaje histórico',r'pinochet'),('Salvador Allende','Personaje histórico',r'allende'),
 ('Paul Schäfer','Personaje histórico',r'sch[aä]e?fer'),
 ('Álvaro Uribe','Político contemporáneo',r'^(álvaro |alvaro )?uribe( vélez| velez)?$'),('Gustavo Petro','Político contemporáneo',r'petro\b'),
 ('Juan Manuel Santos','Político contemporáneo',r'juan manuel santos|^santos$'),('Iván Duque','Político contemporáneo',r'duque'),
 ('Sebastián Piñera','Político contemporáneo',r'pi[ñn]era'),('Gabriel Boric','Político contemporáneo',r'boric'),('Michelle Bachelet','Político contemporáneo',r'bachelet'),
 ('Andrés Parra','Elenco y producción',r'andr[eé]s parra|^parra$'),('Wagner Moura','Elenco y producción',r'wagner|moura'),
 ('Diego Luna','Elenco y producción',r'diego luna'),('Pedro Pascal','Elenco y producción',r'pedro pascal'),
 ('Julián Román','Elenco y producción',r'juli[aá]n rom[aá]n'),('Gustavo Bolívar','Elenco y producción',r'gustavo bol[ií]var'),
 ('Daniel Muñoz','Elenco y producción',r'daniel mu[ñn]oz'),('Tamara Acosta','Elenco y producción',r'tamara acosta'),
 ('Antonia Zegers','Elenco y producción',r'antonia zegers'),('Angie Cepeda','Elenco y producción',r'angie cepeda'),
 ('Juan Herrera','Personaje de ficción',r'juan ?herrera'),('Félix Herrera','Personaje de ficción',r'^f[eé]lix'),('Claudia Herrera','Personaje de ficción',r'^claudia')]
def canon(x):
    for n,c,r in CAN:
        if re.search(r,x): return n,c
    return None,None
u=pd.Series(e.x.unique()); m=u.map(canon); mp=dict(zip(u,m))
e['canon']=e.x.map(lambda x: mp[x][0]); e['cat']=e.x.map(lambda x: mp[x][1])
# restricciones por serie (nombres ambiguos)
amb={'Fidel Castaño':['TresCaines'],'Vicente Castaño':['TresCaines'],'Félix Herrera':['Los80'],'Claudia Herrera':['Los80'],'Juan Herrera':['Los80']}
for k,v in amb.items(): e.loc[(e.canon==k)&(~e.serie.isin(v)),'canon']=None
c=e.dropna(subset=['canon']).drop_duplicates(['fuente','id','canon'])
c.to_pickle(PRIV+'/ner_canon.pkl')
# textos en español por serie (denominador)
idi=pd.read_pickle(PRIV+'/idioma.pkl'); sent=pd.read_pickle(PRIV+'/sent.pkl')[['fuente','id','serie','pred','p_pos','p_neg']]
den=sent.merge(idi,on=['fuente','id']); den=den[den.es==True]; N=den.groupby('serie').size()
t=c.groupby(['serie','canon','cat']).size().rename('textos').reset_index(); t['por_mil']=(1000*t.textos/t.serie.map(N)).round(1)
t=t.sort_values(['serie','textos'],ascending=[True,False]); t.to_csv('tab/ner_entidades.csv',index=False)
for s in SER: print('\n',s, t[t.serie==s].head(12)[['canon','cat','textos','por_mil']].to_string(index=False))
cat=c.drop_duplicates(['fuente','id','cat']).groupby(['serie','cat']).size().unstack(fill_value=0)
print((1000*cat.div(N,axis=0)).round(1))
