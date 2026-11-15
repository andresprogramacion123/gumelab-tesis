# GUMELAB · Recepción digital de telenovelas de la memoria

Código, datos públicos y resultados de la tesis de pregrado en Física de **Julián Andrés Montoya Carvajal** (Instituto de Física, Universidad de Antioquia), desarrollada en el componente de investigación digital del proyecto **GUMELAB** (*Transmisión de la historia a través de los medios de entretenimiento en América Latina*, Universidad Libre de Berlín). Asesor: Prof. Leonardo Augusto Pachón Contreras.

El trabajo recolecta, depura y analiza la conversación en Google, YouTube y X (antes Twitter) sobre cinco producciones: *Escobar, el patrón del mal* (EPM), *Narcos*, *Tres Caínes*, *Los 80* y *Dignidad*.

## Estructura

```
gumelab-tesis/
├── cuadernos/                      Cuadernos originales (Google Colab), sin salidas y sin claves
│   ├── 01_google/                  Motor de búsqueda con Google Custom Search y depuración
│   ├── 02_youtube/                 Flujo completo de la API de YouTube (pasos 01 a 15)
│   ├── 03_x/                       Preprocesamiento y banco de datos de X
│   ├── 04_exploracion_y_clasificacion/  LDA, análisis descriptivo, etiquetado y clasificación FP/CH/IM
│   └── 05_redes_mathematica/       Red bipartita hashtag–canal (Mathematica, caso La Quebradona)
├── colab/                          Cuadernos de Colab del capítulo 6: sentimiento (RoBERTuito) y NER (spaCy)
├── scripts/                        Análisis del capítulo 6 en Python (estadística, redes, emojis, NER)
├── datos/                          Datos públicos: criterios de búsqueda, resultados de Google e identificadores
├── resultados/
│   ├── tab/                        Tablas agregadas (CSV) del capítulo 6
│   └── fig/                        Figuras del capítulo 6
├── requirements.txt
└── LICENSE                         MIT (código)
```

## Flujo de trabajo

### 1. Recolección (cuadernos originales, Google Colab)

| Fuente | Cuadernos | Descripción |
|---|---|---|
| Google | `01_google/01_GoogleSearchEngine_v1` → `02_DataCleaning_Google` | Búsqueda combinatoria (criterio × país × rango de fechas × página) con punto de reanudación; `v2` reanuda desde el criterio 498 y excluye YouTube |
| YouTube | `02_youtube/01_Search` → `02_DataCleaning1` → `03_PlayListsItems`, `04_SearchCanales` → `05_DataCleaning2` → `06_Videos` → `07_Similaridad`, `08_SimilaridadLevenshtein` → `09_Filtro` → `10_VideosSI` → `11_HilosComentarios` → `12_RespuestasComentarios` → `13_ChannelPais` → `14_UnionDatos` → `15_BancoDatosYoutube` | Extracción de videos, comentarios y respuestas; filtro de relevancia por similitud coseno y Levenshtein |
| X | `03_x/01_PreprocesamientoTweets` → `02_BancoDatos_X` | Limpieza, lematización y unión de los bancos por serie |
| Exploración y clasificación | `04_exploracion_y_clasificacion/` | LDA con coherencia C_V, nubes de palabras y n-gramas, clasificación supervisada en Formación Política (FP), Conciencia Histórica (CH) e Imagen de la Memoria (IM) |

Los cuadernos se ejecutaron en Google Colab con Google Drive. Las rutas de Drive se dejaron como estaban; para reutilizarlos hay que ajustarlas. **Las claves de API se reemplazaron por `TU_CLAVE_DE_API`**: para ejecutar los cuadernos de extracción se necesita una clave propia de Google Cloud.

### 2. Análisis del capítulo 6 (scripts locales y Colab)

```bash
pip install -r requirements.txt
# Copiar los bancos de Excel a datos_privados/originales/ (ver "Datos")
python scripts/00_preparar_bancos.py        # Excel → pickle
python scripts/01_exportar_textos.py        # textos para Colab
#   colab/01_sentimiento_robertuito.ipynb  → sentimiento_gumelab.csv.gz
#   colab/02_ner_spacy.ipynb              → entidades_gumelab.csv
#   (copiar ambas salidas a datos_privados/derivados/)
python scripts/02_cargar_resultados_colab.py
python scripts/temporal.py         # picos de actividad (z-score)
python scripts/temporal_es.py      # serie temporal solo en español
python scripts/burst.py            # coeficiente de ráfagas B (Goh y Barabási, 2008)
python scripts/colas.py            # CCDF y exponente α por máxima verosimilitud (Clauset et al., 2009); Gini
python scripts/google_stats.py     # tipos de fuente y precisión de Google
python scripts/redes_x.py          # redes de menciones/retuits y bipartita hashtag–cuenta
python scripts/dibujo_redes.py EPM # figura de redes de una serie
python scripts/redes_yt.py         # red de respuestas de YouTube
python scripts/comunidades.py TresCaines   # mapa de comunidades con sentimiento
python scripts/actores.py          # transnacionalidad y alcance
python scripts/difusion.py         # emisores y amplificadores
python scripts/emojis.py && python scripts/fig_emojis.py   # emojis frente a sentimiento
python scripts/ner.py && python scripts/ner_fig.py         # referentes de la memoria
```

`emojis.py` necesita el *Emoji Sentiment Ranking* (Kralj Novak et al., 2015, licencia CC BY-SA 4.0): descargar `Emoji_Sentiment_Data_v1.0.csv` desde <https://www.clarin.si/repository/xmlui/handle/11356/1048> y guardarlo en `datos/`.

## Datos

### Incluidos en el repositorio (`datos/`)
- `criterios/`: criterios de búsqueda por serie (términos de contenido histórico × valoración general), definidos por el equipo de humanidades de GUMELAB.
- `google/DatosT_2023.xlsx`: 1.810 resultados de Google para EPM con la revisión de relevancia de las investigadoras. `google/pruebas_motor_v2_julio2022/`: corridas de prueba del motor v2.
- `consultas/consultas_x.txt`: consultas exactas usadas en X.
- `ids/`: identificadores de tuits (`tweet_id`) y de videos, comentarios y respuestas de YouTube por serie. Permiten reconstruir el corpus con las API (*rehidratación*). La columna `id_interno` de X es el identificador usado en los archivos derivados.

### No incluidos (`datos_privados/`, excluido por `.gitignore`)
Los bancos completos contienen el texto de comentarios y publicaciones junto con nombres de usuario de personas privadas. Por respeto a su privacidad y a los términos de uso de YouTube y X, que restringen la redistribución de su contenido, **no se publican**. Se conservan en el almacenamiento del proyecto y pueden solicitarse al autor o al equipo de GUMELAB para fines de investigación.

```
datos_privados/
├── originales/      Bancos de Excel: 5 de YouTube (RESULTS-BancoDatos2023-03-23_*.xlsx) y 5 de X (*_Banco_datos.xlsx)
├── derivados/       textos_gumelab.csv.gz, sentimiento_gumelab.csv.gz, entidades_gumelab.csv.gz, tablas_sensibles/
└── etiquetados/     Conjuntos etiquetados FP/CH/IM de X y YouTube
```

## Cómo citar
Montoya Carvajal, J. A. (2026). *[Título de la tesis]*. Trabajo de grado, Instituto de Física, Universidad de Antioquia.
