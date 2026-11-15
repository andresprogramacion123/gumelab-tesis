"""Rutas del repositorio. Ajusta ORIGINALES a la carpeta donde están los bancos de Excel."""
import os
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ORIGINALES = os.path.join(RAIZ, 'datos_privados', 'originales')    # bancos de Excel de YouTube y X
PRIV = os.path.join(RAIZ, 'datos_privados', 'derivados')            # textos, sentimiento, entidades
PQ = os.path.join(PRIV, 'pq')                                        # bancos convertidos a pickle
DATOS = os.path.join(RAIZ, 'datos')                                  # datos públicos (criterios, Google, ids)
RES = os.path.join(RAIZ, 'resultados')                               # tablas (tab/) y figuras (fig/)
for d in (PQ, os.path.join(RES, 'tab'), os.path.join(RES, 'fig')):
    os.makedirs(d, exist_ok=True)
os.chdir(RES)   # las rutas relativas 'tab/...' y 'fig/...' quedan dentro de resultados/
