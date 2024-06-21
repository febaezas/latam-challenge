from typing import List, Tuple
from datetime import datetime
import pandas as pd
import json

import itertools
import multiprocessing as mp

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Por mejorar:
    #   - Se hace agrupacion por username, puede cambiar en tiempo, revisar hacerlo por id. 
    #     * por necesidad se puede usar para revisar impacto de nombre de cuenta mas que dueño
    
    # Defino columnas necesarias (para acotar necesidad de info cargada a lo necesario)
    col = ['date', 'renderedContent', 'mentionedUsers', 'user', 'username', 'user.id']
    col_output = ['date', 'user.username']
    BUF_SIZE = 15000
    # Configuracion de largo maximo por columna a imprimir
    pd.set_option("max_colwidth", 40)

    # 14 s con %timeit
    # Se lee el archivo .json
    # Se lee Dataframe desde funcion propia para reutilizar codigo
    #df = abreDFt(file_path, col)

    # df['user.username'] = df['user.username'].astype(str)
    
    # Columna a tipo fecha para hacer calculos.
    # df['date'] = pd.to_datetime(df['date'])

    # Obtenog top 10 fechas con mayor interaccion
    # df_fecha = (df['date'].dt.floor('d').value_counts().reset_index(name='count'))
    
    # # Agrupo por fecha / usuario para sacar interaccion por usuario/fecha
    # df_usr = df.groupby([df['date'].dt.floor('d'), 'user.username']).size().reset_index(name='q')

    # # Hago join entre fechas y ususarios con mayor interaccion
    # dff = pd.merge(df_fecha.head(10), df_usr, how="left", on=["date", "date"]).sort_values(by=['count', 'q'],ascending=False).reset_index()
    
    # # Filtro el usuario con mayor interaccion en cada fecha
    # idx = dff.groupby(['date'])['q'].idxmax()
    # dff = dff.loc[idx].sort_values(by=['count'],ascending=False)
    # dff = dff[col_output]
    
    # # Se devuelve la lista de tuplas / Revisar cambio formato de fecha timestamp a datetime.date
    # salida = list(dff.itertuples(index=False, name=None))
    # return salida

