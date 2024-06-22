from typing import List, Tuple
import pandas as pd
import json
import re as re

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    # Por mejorar:
    #   - Se hace conteo solo de menciones en tweets para medir impacto
    #     no considera citas para ver efecto cascada del tweet

    # Defino columnas necesarias (para acotar necesidad de info cargada a lo necesario)
    col = ['date', 'renderedContent', 'mentionedUsers', 'user.username', 'user.displayname', 'user.id']
    col_output = ['user', 'q']

    BUF_SIZE = 15000
    
    # se cambia a apretura por chunks para acelerar la lectura (baja consumo de ram, era ideal principal pero tambien afecto tiempo de ejecucion)
    dff = pd.DataFrame()
    chunks = pd.read_json(file_path, lines=True, chunksize = BUF_SIZE)
    i = 0
    
    print('inicio iteracion')
    for chunk in chunks:
        tweets = chunk['renderedContent'].str.cat(sep='\n')
        dff = pd.concat([dff, (pd.DataFrame(re.findall(r'(?<=@)\w+',tweets)).value_counts()
         .rename_axis('user').rename('q').reset_index()) ])
        #print(dfemoj)
    
    dff = dff.groupby(['user']).sum().sort_values(by=['q'], ascending=False).reset_index()
    # _-----------------------------
    # Se devuelve la lista de tuplas 
    salida = list(dff[col_output].head(10).itertuples(index=False, name=None))
    #print(salida)
    return salida