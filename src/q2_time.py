from typing import List, Tuple
from datetime import datetime
import pandas as pd
import json
import emoji

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    # Defino columnas necesarias (para acotar necesidad de info cargada a lo necesario)
    col = ['date', 'renderedContent', 'mentionedUsers', 'user.username', 'user.displayname', 'user.id']
    col_output = ['emoji', 'q']

    # Configuracion de largo maximo por columna a imprimir
    pd.set_option("max_colwidth", 40)

    # 14 s con %timeit
    # Se lee el archivo .json
    with open(file_path) as f:
        lines = f.read().splitlines()

    # Se crea un dataframe con el json leido
    df_inter = pd.DataFrame(lines)
    df_inter.columns = ['jsond']
    df_inter['jsond'].apply(json.loads)

    # aplico normlizacion JSON para aplanar JSON anidados (con prefijo del padre)
    df = pd.json_normalize(df_inter['jsond'].apply(json.loads))
    
    
    # Filtro columnas necesarias
    df = df[col]
    
    text = df['renderedContent'].str.cat(sep='\n')
    dff = (pd.DataFrame(emoji.emoji_list(text)).value_counts('emoji')
         .rename_axis('emoji').rename('q').reset_index()
         .assign(Type=lambda x: x['emoji'].apply(emoji.demojize)))


    # Se devuelve la lista de tuplas 
    salida= list(dff[col_output].head(10).itertuples(index=False, name=None))
    return salida