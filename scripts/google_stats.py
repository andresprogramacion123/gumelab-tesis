import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import *
import pandas as pd,numpy as np,re,sys,matplotlib.pyplot as plt
from urllib.parse import urlparse
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from estilo import *
d=pd.read_excel(os.path.join(DATOS,'google','DatosT_2023.xlsx'))
d['dom']=d['Sitios Web/ Fuente'].astype(str).map(lambda u: urlparse(u).netloc.lower().removeprefix('www.').removeprefix('m.'))
d['sirve']=d['Sirve: si /no'].astype(str).str.strip().str.lower().map({'si':1,'no':0})
PRENSA=r'elespectador|eltiempo|semana|elpais|eluniversal|latercera|elheraldo|kienyke|emol|hoyxhoy|caracol\.com\.co|noticias|lanacion|elcolombiano|infobae|bbc|cnn|elmundo|larepublica|las2orillas|razonpublica|eje21|radio|diario|publimetro|t13|biobio|cooperativa|elmostrador|folha|globo|uol|spiegel|zeit|faz|sueddeutsche|welt|tagesspiegel|stern|bild|taz|nzz|dw\.com|terra|estadao|veja|clarin|lun\.com|cambio|confidencial|vanguardia|pulzo|minuto30|wradio|bluradio|lafm|rcnradio|semana|portafolio|dinero|revista|fucsia|diners|elnuevosiglo|elsiglo|reuters|europapress|efe|abc\.es|elperiodico|20minutos|huffingtonpost|vice|time\.com|nytimes|washingtonpost|guardian|independent|mercurio|segundo|cooperativa|adnradio|elnuevodia|lanacion|nacion|prensa|news|zeitung|tribune|post|laopinion|colombia\.com|theclinic|soychile|eldinamo|lasegunda|elpilon|zonacero|protagonista|headtopics|redgol|\.as\.com|elfiltrador|enteratecali|zeleb|estereofonica|colombiamegusta|elheraldo|lun\.com|cronica|tiempo|correo|heraldo|informador|universo|opinion'
SECTOR=r'fotech|canaltrece|latinspots|produ|prensario|entretengo|tvynovelas|ecartelera|sensacine|filmaffinity|imdb|tvguia|tvn|13\.cl|mega\.cl|canal13|chilevision|teleseries|seriesadictos|espinof|vix|tvazteca|rcn|caracoltv\.com|telemundo|univision'
ACAD=r'\.gov|\.gob|minciencias|colciencias|fes\.de|ufrj|\.edu|scielo|repositor|redalyc|dialnet|academia\.edu|researchgate|bdigital|bibliotec|revistas|journals|uni-|universit|ojs'
STREAM=r'netflix|play\.caracoltv|verseries|ennetflix|cuevana|pelis|series(online|flix)|primevideo|amazon\.|hbo|justwatch|serieslan|repelis|gnula|pelisplus|tvserie'
SOCIAL=r'pinterest|facebook|twitter|instagram|tiktok|reddit|linkedin|tumblr|youtube|vimeo|taringa|quora|blogspot|wordpress|medium'
COMERCIO=r'mercadolibre|ebay|amazon\.com|olx|aliexpress|redbubble|etsy|tienda|shop|store'
FAN=r'pabloescobar|escobar|wiki|linkfang|fandom|ecured|biografia|famous|celebrity'
def tipo(x):
    for n,p in [('Plataformas y descargas',STREAM),('Redes y blogs',SOCIAL),('Comercio',COMERCIO),('Académico e institucional',ACAD),('Prensa',PRENSA),('Medios del sector TV',SECTOR),('Sitios de fans y enciclopedias',FAN)]:
        if re.search(p,x): return n
    return 'Otros'
d['tipo']=d.dom.map(tipo)
d['anio']=d['Año 2009 - 2021'].astype(str).str[:4].replace('2009','2009–12')
t=d.groupby('tipo').agg(resultados=('tipo','size'),dominios=('dom','nunique'),precision=('sirve','mean')).sort_values('resultados',ascending=False)
t['participacion']=(t.resultados/len(d)).round(3); t['precision']=t.precision.round(2); print(t.to_string()); t.to_csv('tab/google_tipos.csv')
print(d[d.tipo=='Otros'].dom.value_counts().head(30).to_dict())
top=d.groupby('dom').agg(n=('dom','size'),precision=('sirve','mean'),tipo=('tipo','first')).sort_values('n',ascending=False).head(15).round(2); top.to_csv('tab/google_top_dominios.csv'); print(top)
y=d.groupby('anio').agg(n=('anio','size'),precision=('sirve','mean')); y.to_csv('tab/google_anios.csv')
# figura
fig,ax=plt.subplots(1,2,figsize=(7.4,3.0),gridspec_kw={'width_ratios':[1.35,1]})
tt=t.sort_values('resultados')
ax[0].barh(tt.index,tt.resultados,color=C['g'],height=0.6)
for i,(n,p) in enumerate(zip(tt.resultados,tt.precision)): ax[0].text(n+8,i,f'{n}  (precisión {p:.2f})'.replace('.',','),va='center',fontsize=7)
ax[0].set_xlabel('Resultados'); ax[0].set_xlim(0,tt.resultados.max()*1.75); ax[0].grid(axis='y',visible=False)
ax[0].set_title('(a) Resultados por tipo de fuente',loc='left',fontsize=8.5)
ax[1].plot(y.index,y.precision,color=C['g'],marker='o',ms=4)
for x,(n,p) in enumerate(zip(y.n,y.precision)): ax[1].annotate(f'n={n}',(x,p),xytext=(0,6),textcoords='offset points',ha='center',fontsize=6.5,color=C['muted'])
ax[1].set_ylim(0,1); ax[1].set_ylabel('Precisión'); ax[1].yaxis.set_major_formatter(lambda v,_: f'{v:.1f}'.replace('.',','))
ax[1].tick_params(axis='x',rotation=60,labelsize=7); ax[1].set_title('(b) Precisión por rango de fechas',loc='left',fontsize=8.5)
plt.tight_layout(); fig.savefig('fig/google_fuentes.png')
