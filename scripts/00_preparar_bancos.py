import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
"""Convierte los bancos de Excel (YouTube y X) a pickle para acelerar los análisis."""
import pandas as pd, glob
YT={'22_02_55':'Dignidad','22_17_52':'Los80','22_31_55':'TresCaines','23_00_25':'Narcos','23_17_15':'EPM'}
for k,s in YT.items():
    f=glob.glob(os.path.join(ORIGINALES,f'RESULTS-BancoDatos2023-03-23_{k}*.xlsx'))[0]
    d=pd.read_excel(f); d['Serie']=s
    d.astype({c:str for c in d.columns if d[c].dtype==object}).to_pickle(os.path.join(PQ,f'yt_{s}.pkl')); print('YouTube',s,d.shape)
TW={'Escobar_Patron_del_mal':'EPM','Narcos':'Narcos','Tres_ca*':'TresCaines','Los_80':'Los80','Dignity':'Dignidad'}
for k,s in TW.items():
    d=pd.read_excel(glob.glob(os.path.join(ORIGINALES,f'{k}_Banco_datos.xlsx'))[0]); d['SerieN']=s
    d.astype({c:str for c in d.columns if d[c].dtype==object}).to_pickle(os.path.join(PQ,f'tw_{s}.pkl')); print('X',s,d.shape)
