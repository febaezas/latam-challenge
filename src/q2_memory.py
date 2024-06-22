from typing import List, Tuple
from datetime import datetime
import pandas as pd
import json
import emoji
from ftime import abreDFt

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    # Por mejorar:
    #   - Se hace conteo de emojis sin filtrar repetidos en mismo tweet (enfasis de emocion)
    #     ni tampoco analisis de sentimiento de texto.

    # Defino columnas necesarias (para acotar necesidad de info cargada a lo necesario)
    col = ['date', 'renderedContent', 'mentionedUsers', 'user.username', 'user.displayname', 'user.id']
    col_output = ['emoji', 'q']
    BUF_SIZE = 15000
    # Configuracion de largo maximo por columna a imprimir
    pd.set_option("max_colwidth", 40)

    dfemoj = pd.DataFrame()
    # se cambia a apretura por chunks para acelerar la lectura
    chunks = pd.read_json(file_path, lines=True, chunksize = BUF_SIZE)
    i = 0
    
    for chunk in chunks:
        text = chunk['renderedContent'].str.cat(sep='\n')
        dfemoj = pd.concat([dfemoj, (pd.DataFrame(emoji.emoji_list(text)).value_counts('emoji')
         .rename_axis('emoji').rename('q').reset_index()
         .assign(Type=lambda x: x['emoji'].apply(emoji.demojize)))])
        #print(dfemoj)
    
    dffin = dfemoj.groupby(['emoji']).sum().sort_values(by=['q'], ascending=False).reset_index()

    salida= list(dffin[col_output].head(10).itertuples(index=False, name=None))
    return salida