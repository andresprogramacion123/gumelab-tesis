import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,sys
from scipy.stats import spearmanr,pearsonr
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
s=pd.read_pickle(PRIV+'/sent.pkl')
s=s.merge(pd.read_pickle(PRIV+'/idioma.pkl'),on=['fuente','id'],how='left')
SOLO_ES=True
if SOLO_ES: s=s[s.es==True]
s['emojis']=s.emojis.fillna('')
p=s[(s.n_emojis>0)&(s.pred!='SOLO_EMOJI')].copy()
p['lista']=p.emojis.str.split().map(lambda l: sorted(set(l)))
e=p[['fuente','serie','pred','p_neg','p_neu','p_pos','lista']].explode('lista').rename(columns={'lista':'emoji'})
def resumen(g):
    n=len(g); return pd.Series({'n':n,'s_texto':(g.p_pos-g.p_neg).mean(),'pos':(g.pred=='POS').mean(),'neu':(g.pred=='NEU').mean(),'neg':(g.pred=='NEG').mean()})
R=e.groupby('emoji').apply(resumen).query('n>=30').sort_values('n',ascending=False)
esr=pd.read_csv(os.path.join(DATOS,'Emoji_Sentiment_Data_v1.0.csv')); esr['s_ref']=(esr.Positive-esr.Negative)/esr.Occurrences
esr['emoji']=esr.Emoji.str.replace('️','')
R=R.join(esr.set_index('emoji')[['s_ref','Occurrences','Unicode name']],how='left')
m=R.dropna(subset=['s_ref'])
rho,pv=spearmanr(m.s_texto,m.s_ref); r,pr=pearsonr(m.s_texto,m.s_ref)
print(f'emojis con n>=30: {len(R)}; en ESR: {len(m)}; Spearman rho={rho:.3f} (p={pv:.1e}); Pearson r={r:.3f}')
# ponderado por fuente
for f in ['YouTube','X']:
    Rf=e[e.fuente==f].groupby('emoji').apply(resumen).query('n>=30').join(esr.set_index('emoji').s_ref).dropna()
    print(f, len(Rf), 'rho=%.3f'%spearmanr(Rf.s_texto,Rf.s_ref)[0])
R.round(3).to_csv('tab/emojis_sentimiento.csv')
print(R.head(25).round(3).to_string())
# textos con vs sin emoji
s['con_emoji']=s.n_emojis>0
print(pd.crosstab([s.fuente,s.con_emoji],s.pred,normalize='index').round(3))
print('solo emoji:',(s.pred=='SOLO_EMOJI').sum())
