import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,sys,matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
from PIL import Image,ImageDraw,ImageFont
from scipy.stats import spearmanr
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
F=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',109)
def img(e):
    im=Image.new('RGBA',(160,136),(0,0,0,0)); ImageDraw.Draw(im).text((0,0),e,font=F,embedded_color=True)
    b=im.getbbox(); return np.asarray(im.crop(b)) if b else None
R=pd.read_csv('tab/emojis_sentimiento.csv',index_col=0)
m=R.dropna(subset=['s_ref']); rho=spearmanr(m.s_texto,m.s_ref)[0]
coma=lambda v,_=None: f'{v:.1f}'.replace('.',',')
# (1) dispersión
fig,ax=plt.subplots(figsize=(6.4,5.2))
ax.axhline(0,color='#c3c2b7',lw=0.8); ax.axvline(0,color='#c3c2b7',lw=0.8); ax.plot([-1,1],[-1,1],ls='--',color='#c3c2b7',lw=0.8)
ax.scatter(m.s_ref,m.s_texto,s=8,color='#8a8984',alpha=0.6,zorder=2)
top=m.sort_values('n',ascending=False).head(24)
for e,row in top.iterrows():
    a=img(e)
    if a is None: continue
    ab=AnnotationBbox(OffsetImage(a,zoom=0.11),(row.s_ref,row.s_texto),frameon=False,zorder=3); ax.add_artist(ab)
a,b=np.polyfit(m.s_ref,m.s_texto,1); xx=np.linspace(-0.6,0.9,10); ax.plot(xx,a*xx+b,color=C['acc'],lw=1.2)
ax.set_xlim(-0.6,0.95); ax.set_ylim(-0.75,0.7)
ax.set_xlabel('Sentimiento de referencia (Emoji Sentiment Ranking)'); ax.set_ylabel('Sentimiento del texto que acompaña al emoji (GUMELAB)')
ax.xaxis.set_major_formatter(coma); ax.yaxis.set_major_formatter(coma)
ax.text(0.02,0.97,f'{len(m)} emojis con n ≥ 30\nSpearman ρ = {rho:.2f}'.replace('.',','),transform=ax.transAxes,va='top',fontsize=8)
plt.tight_layout(); fig.savefig('fig/emojis_dispersion.png'); plt.close()
# (2) red bipartita emoji–polaridad
top=R.sort_values('n',ascending=False).head(20).sort_values('s_texto')
fig,ax=plt.subplots(figsize=(6.2,6.4)); ax.axis('off')
POL={'neg':('Negativo','#e34948',0.80),'neu':('Neutro','#8a8984',0.5),'pos':('Positivo','#2a78d6',0.20)}
ys=np.linspace(0.97,0.03,len(top))
for (e,row),y in zip(top.iterrows(),ys):
    for k,(lab,col,yp) in POL.items():
        w=row[k]*row.n; ax.plot([0.12,0.78],[y,yp],color=col,lw=0.15+7*w/ (top.n.max()*0.6),alpha=0.45,solid_capstyle='round',zorder=1)
    a=img(e); ax.add_artist(AnnotationBbox(OffsetImage(a,zoom=0.15),(0.08,y),frameon=False))
    ax.text(0.0,y,f'{int(row.n)}',ha='right',va='center',fontsize=6.5,color=C['muted'])
for k,(lab,col,yp) in POL.items():
    ax.scatter([0.8],[yp],s=900,color=col,zorder=3); ax.text(0.86,yp,lab,va='center',fontsize=9)
ax.set_xlim(-0.06,1.05); ax.set_ylim(0,1)
ax.text(0.08,1.0,'emoji (n)',ha='center',fontsize=7.5,color=C['muted'])
plt.tight_layout(); fig.savefig('fig/emojis_red.png'); plt.close()
print('ok')
