from typing import List, Tuple
from datetime import datetime
import pandas as pd
import json

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Por mejorar:
    #   - Se hace agrupacion por username, puede cambiar en tiempo, revisar hacerlo por id. 
    #     * por necesidad se puede usar para revisar impacto de nombre de cuenta mas que dueño
    
    # Defino columnas necesarias (para acotar necesidad de info cargada a lo necesario)
    col = ['date', 'renderedContent', 'mentionedUsers', 'user', 'username', 'user.id']
    col_output = ['date', 'username']
    BUF_SIZE = 15000
    # Configuracion de largo maximo por columna a imprimir

    # 14 s con %timeit
    # Se lee el archivo .json
    # Se lee Dataframe desde funcion propia para reutilizar codigo
    #df = abreDFt(file_path, col)
    jsonfile = open(file_path, 'r')

    dfdate = pd.DataFrame()
    dfuser = pd.DataFrame()
    chunks = pd.read_json(file_path, lines=True, chunksize = BUF_SIZE)
    chunk_results = []

    # Función para obtener el username del diccionario usuario
    def extract_username(user_dict):
        return user_dict.get('username', None)  # Devuelve None si 'username' no está presente

    # Leo por chunks el JSON
    for chunk in chunks:
        # Convertir el campo usuario en username usando la función extract_username
        chunk['username'] = chunk['user'].apply(extract_username)
        # Agrupo en df conteo de interacciones por dia del chunk para sacar fecha mas activa
        dfdate = pd.concat([dfdate, chunk['date'].dt.floor('d').value_counts().reset_index(name='count')])
        # Realizar el group by por fecha y username y contar interacciones
        grouped_data = chunk.groupby([chunk['date'].dt.floor('d'), 'username']).size().reset_index(name='q')

        # Agregar chunk a lista
        chunk_results.append(grouped_data)

    # Concatenar todos los resultados de los chunks en un DataFrame final
    dfuser = pd.concat(chunk_results, ignore_index=True)

    # Agrupo fechas para tener ranking de dias mas activos
    dfdate = dfdate.groupby(['date'])['count'].sum().sort_values(ascending=False).head(10).reset_index(name ='q2')#.sort_values(by='count', ascending=False)

    # HAgo merge en df de fechas y de usuarios para hacer el cruce dias activos / cantidad interacciones por usuario
    dff = dfdate.merge(dfuser, how='left', left_on='date', right_on='date').sort_values(by=['q2','q'],ascending=False).reset_index()
    dff.reset_index()
    
    # Objetno usuario con mayor cantidad de interacion por dia
    idx = dff.groupby(['date'])['q'].idxmax()
    dff = dff.loc[idx].sort_values(by=['q2'],ascending=False)
    dff = dff[col_output]

    # Convierto a formato fecha python
    dff['date'] = dff['date'].apply(lambda x: x.date())
    
    # Se devuelve la lista de tuplas / Revisar cambio formato de fecha timestamp a datetime.date
    salida = list(dff.itertuples(index=False, name=None))
    return salida

