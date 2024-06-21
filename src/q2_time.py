from typing import List, Tuple
from datetime import datetime
import pandas as pd
import json
import emoji
from ftime import abreDFt

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    # Por mejorar:
    #   - Se hace conteo de emojis sin filtrar repetidos en mismo tweet (enfasis de emocion)
    #     ni tampoco analisis de sentimiento de texto.
    
    # Defino columnas necesarias (para acotar necesidad de info cargada a lo necesario)
    col = ['date', 'renderedContent', 'mentionedUsers', 'user.username', 'user.displayname', 'user.id']
    col_output = ['emoji', 'q']

    # Configuracion de largo maximo por columna a imprimir
    pd.set_option("max_colwidth", 40)

    # 14 s con %timeit
    # Se lee el archivo .json
    df = abreDFt(file_path, col)
    
    # Se selecciona columna con texto de tweets
    text = df['renderedContent'].str.cat(sep='\n')

    # Extrae y cuenta cantidad de emojis en texto agrupando y sumando cantidad.
    dff = (pd.DataFrame(emoji.emoji_list(text)).value_counts('emoji')
         .rename_axis('emoji').rename('q').reset_index()
         .assign(Type=lambda x: x['emoji'].apply(emoji.demojize)))

    # Se devuelve la lista de tuplas 
    salida= list(dff[col_output].head(10).itertuples(index=False, name=None))
    return salida