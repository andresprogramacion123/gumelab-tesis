import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
"""Carga las salidas de Colab (sentimiento) y estima el idioma de cada texto (heurística de palabras funcionales)."""
import pandas as pd, re
s=pd.read_csv(os.path.join(PRIV,'sentimiento_gumelab.csv.gz'),dtype={'id':str})
s['mes']=pd.to_datetime(s.fecha,errors='coerce',utc=True,format='ISO8601').dt.tz_localize(None).dt.to_period('M')
s.to_pickle(os.path.join(PRIV,'sent.pkl'))
t=pd.read_csv(os.path.join(PRIV,'textos_gumelab.csv.gz'),dtype={'id':str},usecols=['id','fuente','texto'])
ES=re.compile(r'\b(?:que|de|la|el|en|los|las|por|para|con|una|es|muy|pero|como|más|serie|mejor)\b',re.I)
t['es']=t.texto.astype(str).str.contains(ES)
t[['fuente','id','es']].to_pickle(os.path.join(PRIV,'idioma.pkl'))
print(t.groupby('fuente').es.mean())
