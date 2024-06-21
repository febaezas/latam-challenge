import pandas as pd
import json

def abreDFt (file_path: str, col: list):
    with open(file_path) as f:
        lines = f.read().splitlines()

    # Se crea un dataframe con el json leido
    df_inter = pd.DataFrame(lines)
    df_inter.columns = ['jsond']
    df_inter['jsond'].apply(json.loads)

    # aplico normlizacion JSON para aplanar JSON anidados (con prefijo del padre)
    df = pd.json_normalize(df_inter['jsond'].apply(json.loads))
    
    # Filtro columnas necesarias
    return df[col]