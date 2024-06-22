from typing import List, Tuple
import pandas as pd
import json
from ftime import abreDFt
import re as re

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    # Por mejorar:
    #   - Se hace conteo solo de menciones en tweets para medir impacto
    #     no considera citas para ver efecto cascada del tweet

    # Defino columnas necesarias (para acotar necesidad de info cargada a lo necesario)
    col = ['date', 'renderedContent', 'mentionedUsers', 'user.username', 'user.displayname', 'user.id']
    col_output = ['user', 'q']

    pd.set_option("max_colwidth", 45)

    # 14 s con %timeit
    # Se lee el archivo .json
    df = abreDFt(file_path, col)
    
    # Se selecciona columna con texto de tweets
    tweets = df['renderedContent'].str.cat(sep='\n')
    
    # Se arma un nuevo dataframe con las menciones extraidas por regex de los tweets y se agrupan contando la cantidad que se repiten
    dff = (pd.DataFrame(re.findall(r'(?<=@)\w+',tweets)).value_counts()
         .rename_axis('user').rename('q').reset_index()) 
    
    # Se devuelve la lista de tuplas 
    salida = list(dff[col_output].head(10).itertuples(index=False, name=None))
    #print(salida)
    return salida